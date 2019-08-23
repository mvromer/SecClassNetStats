# This script is specific to my local Windows 10 (1903) machine. It requires the following
# additional things configured locally to run:
#
#   * Wireshark installed (for dumpcap)
#   * Tor browser bundle installed
#   * Firefox installed
#   * geckodriver in the path
#   * tbselenium package installed (this will pull in selenium)
#     * tbselenuium needed patching in order to run on Windows. See win-tbselenium.patch.
#

import argparse
import os
import pprint
import signal
import subprocess
import sys
import time

from contextlib import contextmanager
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tbselenium.tbdriver import TorBrowserDriver

# These are specific to my system setup.
DUMPCAP_PATH = r"C:\Program Files\Wireshark\dumpcap.exe"
EDITCAP_PATH = r"C:\Program Files\Wireshark\editcap.exe"
TOR_BUNDLE_PATH = r"E:\Tor Browser"
TOR_SOCKS_PORT = 9150

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument( "-i", "--interface",
        type=int,
        default=0,
        help="Select interface number to use for capturing." )

    parser.add_argument( "-p", "--capture-prefix",
        type=str,
        default="std",
        help="Set capture file name prefix." )

    parser.add_argument( "-t", "--use-tor",
        action="store_true",
        help="Use Tor browser driver" )

    return parser.parse_args()

@contextmanager
def quit_on_exit( driver ):
    try:
        yield driver
    finally:
        driver.quit()

def build_driver( use_tor ):
    return (TorBrowserDriver( TOR_BUNDLE_PATH, socks_port=TOR_SOCKS_PORT ) if use_tor
        else quit_on_exit( webdriver.Firefox() ))

def run_captures( site_name, url, title_pattern, number_trials, capture_prefix, interface, use_tor ):
    capture_folder = Path( "." ) / "caps"
    capture_folder.mkdir( parents=True, exist_ok=True )
    capture_folder_str = capture_folder.resolve()

    for trial in range( number_trials ):
        with build_driver( use_tor ) as driver:
            capture_file_name = Path( capture_folder_str ) / f"{capture_prefix}-{site_name}-run{trial}.pcapng"
            dsb_file_name = Path( capture_folder_str ) / f"{capture_prefix}-{site_name}-run{trial}-dsb.pcapng"

            dumpcap_args = [
                DUMPCAP_PATH,
                "-i", str( interface ),
                "-w", str( capture_file_name.resolve() )
            ]

            #print( str( capture_file_name.resolve() ) )

            popen_kwargs = dict(
                args=dumpcap_args,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            with subprocess.Popen( **popen_kwargs ) as dumpcap:
                # Dirty hack that hopefully lets dumpcap spin up before we navigate to the target
                # website. I was noticing that without this sleep no cap files were created. It
                # turned out that even though it's possible to have Python wait until the dumpcap
                # process is running, there's no guarantee that dumpcap has gotten to a point where
                # it's actually capturing packet data by the time script execution continues and the
                # web driver transitions to the target URL.
                time.sleep( 3 )
                driver.get( url )
                WebDriverWait( driver, timeout=500 ).until( EC.title_contains( title_pattern ) )
                # Another dirty hack to give dumpcap a bit of time to finish capturing packets
                # before we kill it in the most undignified manner of process deaths. We tried
                # playing nice by sending the CTRL+C signal to it on Windows, but dumpcap gleefully
                # ignored and continued running. Unfortunate decision on its part.
                time.sleep( 3 )
                dumpcap.terminate()

            editcap_args = [
                EDITCAP_PATH,
                "--inject-secrets",
                "tls,{0}".format( os.getenv( "SSLKEYLOGFILE" ) ),
                str( capture_file_name.resolve() ),
                str( dsb_file_name.resolve() )
            ]

            subprocess.run( editcap_args )

def main():
    cl = parse_command_line()

    sites = [
        # dict(
        #     site_name="wiki-cat",
        #     url="https://en.wikipedia.org/wiki/Cat",
        #     title_pattern="Wikipedia"
        # ),
        # dict(
        #     site_name="wiki-dog",
        #     url="https://en.wikipedia.org/wiki/Dog",
        #     title_pattern="Wikipedia"
        # ),
        # dict(
        #     site_name="wiki-egress",
        #     url="https://en.wikipedia.org/wiki/Egress_filtering",
        #     title_pattern="Wikipedia"
        # ),
        # dict(
        #     site_name="mit",
        #     url="http://web.mit.edu/",
        #     title_pattern="MIT"
        # ),
        # dict(
        #     site_name="unm",
        #     url="http://www.unm.edu/",
        #     title_pattern="New Mexico"
        # ),
        # dict(
        #     site_name="cmu",
        #     url="https://www.cmu.edu/",
        #     title_pattern="Homepage"
        # ),
        # dict(
        #     site_name="berkeley",
        #     url="https://www.berkeley.edu/",
        #     title_pattern="Home"
        # ),
        # dict(
        #     site_name="ut",
        #     url="https://www.utexas.edu/",
        #     title_pattern="University"
        # ),
        # dict(
        #     site_name="asu",
        #     url="https://www.asu.edu/",
        #     title_pattern="Arizona"
        # ),
        dict(
            site_name="utd",
            url="https://www.utdallas.edu/",
            title_pattern="University"
        )
    ]

    capture_prefix = "tor" if cl.use_tor else cl.capture_prefix

    pprint.pprint( cl )
    print( capture_prefix )
    #sys.exit( 0 )

    for site in sites:
        run_captures( **site,
            number_trials=10,
            capture_prefix=capture_prefix,
            interface=cl.interface,
            use_tor=cl.use_tor )

    sys.exit( 0 )

if __name__ == "__main__":
    main()
