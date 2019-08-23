import argparse
import ipaddress
import pprint
import pymongo
import sys

import matplotlib.pyplot as plt
import numpy as np

class HostStats():
    def __init__( self ):
        self.number_orphaned_hosts = None

    @classmethod
    def build( cls, db ):
        stats = HostStats()
        stats.number_orphaned_hosts = db.orphaned_ips.count_documents( {} )
        return stats

    def __str__( self ):
        return "\n".join( [
            f"==============",
            f"| Host Stats |",
            f"==============",
            f"    Number orphaned IP addresses: {self.number_orphaned_hosts}"
        ] )

class LookupStats:
    def __init__( self ):
        self.number_lookups_issued = None
        self.number_lookups_succeed = None
        self.number_lookups_failed = None
        self.number_rdap_records = None
        self.number_legacy_records = None
        self.number_records_missing_cidrs = None

    @classmethod
    def build( cls, db ):
        stats = LookupStats()

        number_lookups_succeed = db.whois.count_documents( {} )
        number_lookups_failed = db.failed_lookups.count_documents( {} )

        stats.number_lookups_issued = number_lookups_failed + number_lookups_succeed
        stats.number_lookups_succeed = number_lookups_succeed
        stats.number_lookups_failed = number_lookups_failed
        stats.number_rdap_records = db.whois.count_documents( { "type": "rdap" } )
        stats.number_legacy_records = db.whois.count_documents( { "type": "whois" } )

        # This is really the same as our orphaned IP count.
        stats.number_records_missing_cidrs = db.orphaned_ips.count_documents( {} )
        return stats

    def __str__( self ):
        return "\n".join( [
            f"================",
            f"| Lookup Stats |",
            f"================",
            f"    Number lookups issued: {self.number_lookups_issued}",
            f"    Number lookups succeded: {self.number_lookups_succeed}",
            f"    Number lookups failed: {self.number_lookups_failed}",
            f"    Number RDAP records: {self.number_rdap_records}",
            f"    Number legacy WHOIS records: {self.number_legacy_records}",
            f"    Number records missing CIRDs: {self.number_records_missing_cidrs}"
        ] )

class NetworkMetrics:
    def __init__( self, number_valid_hosts, network_size ):
        self.number_valid_hosts = number_valid_hosts
        self.network_size = network_size
        self.percent_valid_hosts = number_valid_hosts / network_size * 100.0

class PrefixMetrics:
    def __init__( self ):
        self.number_networks = 0
        self.number_valid_hosts = 0
        self.percent_valid_hosts = 0.0

class NetworkStats:
    def __init__( self ):
        self.networks = {}
        self.prefixes = {}

    @classmethod
    def build( cls, db ):
        stats = NetworkStats()

        network_agg = [
            {
                "$project": {
                    "_id": False,
                    "cidr": True,
                    "number_hosts": { "$size": "$hosts" },
                    "network_size": {
                        "$add": [
                            1,
                            {
                                "$subtract": [ "$end_address", "$start_address" ]
                            }
                        ]
                    }
                }
            }
        ]

        # Compute network counts.
        for network in db.networks.aggregate( network_agg ):
            cidr = ipaddress.ip_network( network["cidr"] )
            number_hosts = network["number_hosts"]
            network_size = network["network_size"]
            stats.networks[cidr] = NetworkMetrics( number_hosts, network_size )

            prefix = stats.prefixes.setdefault( cidr.prefixlen, PrefixMetrics() )
            prefix.number_networks += 1
            prefix.number_valid_hosts += number_hosts

            # Incrementally compute the percentage of valid hosts by prefix. Each percentage will
            # be off by a factor equal to the number of networks found for the corresponding prefix
            # length, but we'll correct for that after this loop completes. This is done to help
            # minimize floating point round off errors, especially for networks with large IP ranges
            # and large number of valid hosts with them (e.g., /10 networks).
            prefix.percent_valid_hosts += (number_hosts / network_size)

        # Compute percentages for prefix length metrics.
        for prefix in stats.prefixes.values():
            prefix.percent_valid_hosts /= prefix.number_networks
            prefix.percent_valid_hosts *= 100.0

        return stats

    def __str__( self ):
        s = [
            f"================",
            f"| Network Stats |",
            f"================",
            f"    Number networks found from lookups: {len( self.networks )}",
            f"    Per network statistics:",
        ]

        # for cidr, metrics in self.networks.items():
        #     s.append( f"        {str( cidr )}:" )
        #     s.append( f"            Network size: {metrics.network_size}" )
        #     s.append( f"            Number valid hosts: {metrics.number_valid_hosts}" )
        #     s.append( f"            Percent valid hosts: {metrics.percent_valid_hosts:.2}%" )

        # s.append( f"    Per prefix length statistics:" )

        # for prefix, metrics in self.prefixes.items():
        #     s.append( f"        {prefix}:" )
        #     s.append( f"            Number networks: {metrics.number_networks}" )
        #     s.append( f"            Number valid hosts: {metrics.number_valid_hosts}" )
        #     s.append( f"            Percent valid hosts: {metrics.percent_valid_hosts:.2}%" )

        return "\n".join( s )

# All of these are static and based on the results obtained from zmap.
class ProbeStats:
    def __init__( self ):
        # zmap reported this as 0.35%
        self.hit_rate = 0.0035
        self.avg_send_rate = 70400
        self.avg_receive_rate = 249

    @classmethod
    def build( cls ):
        return ProbeStats()

    def __str__( self ):
        return "\n".join( [
            f"==============",
            f"| Probe Stats |",
            f"==============",
            f"    Hit rate (percentage): {self.hit_rate * 100:.2}%",
            f"    Average send rate (p/s): {self.avg_send_rate}",
            f"    Average receive rate (p/s): {self.avg_receive_rate}"
        ] )

def plot_lookup_donut( lookup_stats ):
    fig, ax = plt.subplots( figsize=(6,3), subplot_kw=dict( aspect="equal" ) )

    labels = [
        "RDAP: {}".format( lookup_stats.number_rdap_records ),
        "Legacy WHOIS: {}".format( lookup_stats.number_legacy_records )
    ]

    data = [
        lookup_stats.number_rdap_records,
        lookup_stats.number_legacy_records
    ]

    wedges, texts = ax.pie( data, wedgeprops=dict( width=0.35 ), startangle=-30 )

    bbox_props = dict( boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72 )
    kw = dict( arrowprops=dict( arrowstyle="-" ), bbox=bbox_props, zorder=0, va="center" )

    for i, p in enumerate( wedges ):
        ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
        y = np.sin( np.deg2rad( ang ) )
        x = np.cos( np.deg2rad( ang ) )
        horizontal_alignment = { -1: "right", 1: "left" }[int( np.sign(x) )]
        connectionStyle = "angle,angleA=0,angleB={}".format( ang )
        kw["arrowprops"].update( { "connectionstyle": connectionStyle } )
        ax.annotate( labels[i], xy=(x, y), xytext=(1.35 * np.sign( x ), 1.4 * y),
            horizontalalignment=horizontal_alignment, **kw )

    ax.set_title( "Successful WHOIS Lookups" )
    plt.show()

def main():
    client = pymongo.MongoClient()
    db = client.security_class

    host_stats = HostStats.build( db )
    lookup_stats = LookupStats.build( db )
    network_stats = NetworkStats.build( db )
    probe_stats = ProbeStats.build()

    #print( host_stats )
    #print( lookup_stats )
    ##print( network_stats )
    #print( probe_stats )

    #plot_lookup_donut( lookup_stats )

    sorted_networks = sorted( network_stats.networks.items(),
        key=lambda x: x[1].number_valid_hosts,
        reverse=True )
    for sn in sorted_networks[0:10]:
        print( f"{str( sn[0] )} & {sn[1].number_valid_hosts}" )

    sorted_prefixes = sorted( network_stats.prefixes.items(),
        key=lambda x: x[1].number_valid_hosts,
        reverse=True )
    for sn in sorted_prefixes[0:10]:
        print( f"/{str( sn[0] )} & {sn[1].number_valid_hosts} \\\\" )

    sys.exit( 0 )

if __name__ == "__main__":
    main()
