#!/usr/bin/env python3

import argparse
from sys import exit
from modules import censys
from os import path

# importing dotenv
# remember to rename dotenv_example to .env and set your keys
from dotenv import load_dotenv, find_dotenv
if path.isfile('.env'):
    load_dotenv(find_dotenv())
else:
    print('Set up .env credentials to continue.')
    print('Check out dotenv_example for more info.')
    exit(1)

# program arguments
parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help="Host to analize.")
args = parser.parse_args()

if __name__ == '__main__':

    # checking ports, heartbleed and other goodies from Censys
    censys_lookup = censys.CensysLookup(args.host)

    print('Information for: {}'.format(args.host))

    print('\nAutonomous System:')
    print('=======================')
    asn_info = censys_lookup.asn()
    for key, value in asn_info.items():
        print('{}: {}'.format(key, value))

    open_ports = censys_lookup.get_openports()
    print('\n{} ports found:'.format(len(open_ports)))
    print('=======================')
    for port in open_ports:
        print(port.capitalize())

    print('\nAdditional Information:')
    print('=======================')
    heartbleed_status = censys_lookup.check_heartbleed()
    print('Heartbleed vulnerable: {}'.format(heartbleed_status))
