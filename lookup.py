import requests
import os

# importing dotenv
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class CensysLookup():
    """Requests only useful values from Censys API."""

    def __init__(self):

        # getting variables from dotenv
        self.API_URL = 'https://censys.io/api/v1'
        self.API_ID = os.getenv('API_ID')
        self.SECRET = os.getenv('SECRET')

    def view_ip(self, ip):
        """Request raw data from Censys and decode JSON response."""
        ip_info = requests.get('{}/view/ipv4/{}'.format(self.API_URL, ip),
                               auth=(self.API_ID, self.SECRET))

        # If 200 (OK) then proceeds
        if ip_info.status_code == 200:

            # converting request data into JSON data to avoid repetition
            ip_info = ip_info.json()

            # print ip address, ports, location, and other goods.
            print('IP address:\n\t[+] {}'.format(ip_info['ip']))

            print('Open Ports:')
            for port in ip_info['ports']:
                print('\t[+] {}'.format(port))

            print('Location:\n\t[+] {}'.format(ip_info['location']['country']))


# initialize and ask for an IP
lookup = CensysLookup()
ip = input('IP > ')
lookup.view_ip(ip)
