#!/usr/bin/env python3

import requests
import argparse
import re
from sys import exit, stdout
from os import path, getenv

# importing dotenv
# remember to rename dotenv_example to .env and set your keys
from dotenv import load_dotenv, find_dotenv
if path.isfile('.env'):
    load_dotenv(find_dotenv())
else:
    print('Set up .env credentials to continue.')
    print('Check out dotenv_example for more info.')
    exit(1)


class CensysLookup():
    """Requests only useful values from Censys API."""

    def __init__(self):

        # getting variables from dotenv
        self.API_URL = 'https://censys.io/api/v1'
        self.API_ID = getenv('API_ID')
        self.SECRET = getenv('SECRET')

    def view_ip(self, ip):
        """Request raw data from Censys and decode JSON response."""
        ip_info = requests.get('{}/view/ipv4/{}'.format(self.API_URL, ip),
                               auth=(self.API_ID, self.SECRET))

        # If 200 (OK) then proceeds
        if ip_info.status_code == 200:

            # converting request data into JSON data to avoid repetition
            ip_info = ip_info.json()

            # print ip address, location, and other goods.
            print('IP address:\n{}\n'.format(ip_info['ip']))

            print('Open Ports:')
            for port in ip_info['protocols']:

                # print each protocol information
                if 'http' in port:
                    print(port, end=': ')

                    # using regex to strip '\http' from string leaving
                    # only the protocol number
                    http_port = re.search('\d*', port)
                    http_port = http_port.group()

                    # try extracting http info, if not, https.
                    try:
                        http_server = ip_info[http_port]['http']['get']['metadata']['description']
                        print(http_server)
                    except KeyError:
                        # if https, print heartbleed status
                        heartbleed_vuln = ip_info[http_port]['https']['heartbleed']['heartbleed_vulnerable']
                        if heartbleed_vuln:
                            print('Heartbleed vulnerable.')
                        else:
                            print('Heartbleed not vulnerable.')

                elif 'ftp' in port:
                    print(port, end=': ')

                    ftp_port = re.search('\d*', port)
                    ftp_port = ftp_port.group(0)

                    try:
                        ftp_server = ip_info[ftp_port]['ftp']['banner']['metadata']['description']
                        print(ftp_server)
                    except KeyError:
                        print('Key not found.')
                else:
                    print('{}'.format(port))

            print('\nLocation:\n{}'.format(ip_info['location']['country']))
            print()


# program arguments
parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help="Host to analize.")
args = parser.parse_args()

if __name__ == '__main__':
    censys_lookup = CensysLookup()
    censys_lookup.view_ip(args.host)
