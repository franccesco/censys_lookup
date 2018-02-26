#!/usr/bin/env python3

import argparse
from sys import exit
from modules import censys
from os import path
from dotenv import load_dotenv, find_dotenv

# colorama initialization
from colorama import init
from termcolor import colored
init()


# define spacing
def space():
    print(' - ', end='')


# importing dotenv keys
# remember to rename dotenv_example to .env and set your keys
if path.isfile('.env'):
    load_dotenv(find_dotenv())
else:
    print('Set up .env credentials to continue.')
    print('Check out dotenv_example for more info.')
    exit(1)

# program CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help="Host to analize.")
args = parser.parse_args()

if __name__ == '__main__':

    # requesting Censys data about the host
    censys_lookup = censys.CensysLookup(args.host)

    # ASN Information
    asn_info = censys_lookup.asn()
    for key, value in asn_info.items():
        print('{}:\n - {}'.format(key, value))

    # open ports
    open_ports = censys_lookup.get_openports()
    print("Open ports:")
    for port in open_ports:
        space()
        print(colored(port, 'green'))

    # big red alert if heartbleed is found
    heartbleed_status = censys_lookup.check_heartbleed()
    print('Heartbleed: ')
    if heartbleed_status == 'No data available.':
        space()
        print(colored(heartbleed_status, 'white', 'on_grey'))
    elif heartbleed_status is True:
        space()
        print(colored('443/HTTPS VULNERABLE'), )
    elif heartbleed_status is False:
        space()
        print(colored('443/https not vulnerable.', 'green'))
