#!/usr/bin/env python3

import ipaddress
import logging
import pymongo
import sys

from bson.objectid import ObjectId
from ipwhois import IPWhois

# Some info on how data is stored within the local MongoDB database.
#
# Each document in the networks collection contains the following fields:
#
#   start_address - First address in the network stored in integer form.
#   end_address - Last address in the network stored in integer form.
#   cidr - CIDR describing the address range of the network.
#   hosts - List of host addresses found in the original scan that belong to this network.
#   whois_id - Id of the whois record that referenced this network.
#
# Each document in the whois collection contains the following fields:
#
#   type - Either 'rdap' or 'whois' to signify to type of lookup used to obtain the record.
#   raw - Raw record returned from the lookup.
#
# Each document in the failed_lookups collection contains the following fields:
#
#   ip - Textual IP address that failed either a RDAP or WHOIS lookup.
#
# Each document in the orphaned_ips collection contains the following fields:
#
#   ip - Textual IP address whose successful lookup had no CIDR information.
#   whois_id - Id of the whois record retrieved via the associated IP address.
#
class Fields:
    ID = "_id"

    START_ADDRESS = "start_address"
    END_ADDRESS = "end_address"
    CIDR = "cidr"
    HOSTS = "hosts"
    WHOIS_ID = "whois_id"

    TYPE = "type"
    RAW = "raw"

    IP = "ip"

class RecordType:
    RDAP = "rdap"
    WHOIS = "whois"

def setup_logging():
    log_format = "[%(asctime)s.%(msecs)d] %(levelname)s: %(message)s"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig( level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler( filename="process.log", mode="w" )
        ],
        format=log_format,
        datefmt=datetime_format )

def read_command_line():
    # Check for the results file on the command line.
    try:
        return sys.argv[1]
    except:
        logging.error( "Usage: %s <results file>", sys.argv[0] )

def get_security_database():
    # Open up connection to local MongoDB database.
    logging.info( "Opening local MongoDB connection." )
    client = pymongo.MongoClient()
    db = client.security_class

    # Lookups are done by taking an IP address and finding the network that contains the IP address.
    # For this reason, create a compound index on start_address and end_address to make these
    # queries more efficient.
    #
    logging.info( "Creating indexes on networks collection." )
    db.networks.create_index( [
        (Fields.START_ADDRESS, pymongo.ASCENDING),
        (Fields.END_ADDRESS, pymongo.ASCENDING)
    ] )

    return (client, db)

def try_add_ip_to_existing_network( db, ip_addr ):
    # Does this IP address belong to a network we've previously seen? If so, add it to the network's
    # list of hosts.
    ip_str = str( ip_addr )
    ip_number = int( ip_addr )

    update = {
        "$addToSet": {
            Fields.HOSTS: ip_str
        }
    }

    query = {
        Fields.START_ADDRESS: { "$lte": ip_number },
        Fields.END_ADDRESS: { "$gte": ip_number }
    }

    result = db.networks.find_one_and_update( query, update )
    if result:
        logging.info( "Network found. Added IP address %s to network %s.", ip_str, result[Fields.CIDR] )

    return result is not None

def lookup_ip( ip_addr ):
    whois = IPWhois( str( ip_addr ) )
    cidrs = []

    # There's a bug in ipwhois where even though it can pick a default list of lookup methods it
    # will still throw an exception if the first one fails. We get around this by explicitly giving
    # the lookup methods we want.
    asn_methods = ["dns", "http", "whois"]

    # First try RDAP lookup, and if that fails, fall back to legacy WHOIS.
    record = lookup_rdap( whois, asn_methods, cidrs )
    if record:
        return (record, RecordType.RDAP, cidrs)

    record = lookup_whois( whois, asn_methods, cidrs )
    if record:
        return (record, RecordType.WHOIS, cidrs)

    return (None, None, [])

def lookup_rdap( whois, asn_methods, cidrs ):
    try:
        logging.info( "Querying RDAP." )
        result = whois.lookup_rdap( asn_methods=asn_methods )

        if not result["network"]["cidr"]:
            logging.warning( "No CIDRs found in RDAP result. Attempting legacy WHOIS lookup." )
            return None

        new_cidrs = result["network"]["cidr"]
        logging.info( "Found new network CIDRs: %s", new_cidrs )
        cidrs += new_cidrs.split( ", " )
        return result
    except:
        logging.warning( "Error performing RDAP lookup. Attempting legacy WHOIS lookup." )
        return None

def lookup_whois( whois, asn_methods, cidrs ):
    try:
        logging.info( "Querying legacy WHOIS" )
        result = whois.lookup_whois( asn_methods=asn_methods )

        new_cidrs = []
        for net in result["nets"]:
            if net["cidr"]:
                new_cidrs += net["cidr"].split( ", " )

        if not new_cidrs:
            logging.warning( "No CIDRs found in legacy WHOIS. Returning record only." )
            return result

        logging.info( "Found new network CIDRs: %s", ", ".join( new_cidrs ) )
        cidrs += new_cidrs.split( ", " )
        return result
    except:
        logging.warning( "Error performing legacy WHOIS lookup." )
        return None

def add_whois_document( db, record, record_type ):
    return db.whois.insert_one( {
        Fields.TYPE: record_type,
        Fields.RAW: record
    } ).inserted_id

def add_network_document( db, ip_net, whois_id, initial_host ):
    net_doc = {
        Fields.START_ADDRESS: int( ip_net[0] ),
        Fields.END_ADDRESS: int( ip_net[-1] ),
        Fields.CIDR: str( ip_net ),
        Fields.HOSTS: [],
        Fields.WHOIS_ID: str( whois_id )
    }

    if initial_host:
        net_doc[Fields.HOSTS].append( str( initial_host ) )

    return db.networks.insert_one( net_doc ).inserted_id

def add_failed_lookup_document( db, ip_addr ):
    db.failed_lookups.insert_one( {
        Fields.IP: str( ip_addr )
    } )

def add_orphaned_ip_document( db, ip_addr, whois_id ):
    db.orphaned_ips.insert_one( {
        Fields.IP: str( ip_addr ),
        Fields.WHOIS_ID: str( whois_id )
    } )

def main():
    setup_logging()
    results_file_name = read_command_line()

    if not results_file_name:
        sys.exit( 1 )

    client, db = get_security_database()

    with open( results_file_name ) as results_file:
        for line in results_file:
            ip_addr = ipaddress.ip_address( line.strip() )
            logging.info( "Processing IP address %s.", ip_addr )

            try:
                if not try_add_ip_to_existing_network( db, ip_addr ):
                    logging.info( "Querying RDAP/WHOIS database to determine network for %s.", ip_addr )
                    record, record_type, cidrs = lookup_ip( ip_addr )

                    if record:
                        logging.info( "Adding WHOIS record for %s.", ip_addr )
                        whois_id = add_whois_document( db, record, record_type )
                        logging.info( "Added WHOIS record for %s with ID %s.", ip_addr, whois_id )

                        orphaned = not cidrs
                        if orphaned:
                            logging.info( "No CIDRs found for WHOIS record %s. Adding orphaned IP record for IP address %s.",
                                whois_id, ip_addr )
                            add_orphaned_ip_document( db, ip_addr, whois_id )

                        for cidr in cidrs:
                            ip_net = ipaddress.ip_network( cidr )
                            initial_host = ip_addr if ip_addr in ip_net else None

                            logging.info( "Adding network record for %s with WHOIS record %s and initial host %s.",
                                ip_net, whois_id, initial_host )
                            net_id = add_network_document( db, ip_net, whois_id, initial_host )
                            logging.info( "Added network record for %s with ID %s.", ip_net, net_id )
                    else:
                        logging.warning( "Adding failed lookup record for IP %s", ip_addr )
                        add_failed_lookup_document( db, ip_addr )
            except:
                logging.exception( "Unexpected error while processing IP address %s. Adding failed lookup record.", ip_addr )
                add_failed_lookup_document( db, ip_addr )

if __name__ == "__main__":
    main()
