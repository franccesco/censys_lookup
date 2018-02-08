"""Requests only useful values from Censys API."""

import requests
from os import getenv


class CensysLookup():

    def __init__(self, ip):

        # getting variableqs from dotenv
        self.API_URL = 'https://censys.io/api/v1'
        self.API_ID = getenv('API_ID')
        self.SECRET = getenv('SECRET')
        try:
            self.ip_info = requests.get('{}/view/ipv4/{}'.format(self.API_URL,
                                                                 ip),
                                        auth=(self.API_ID, self.SECRET))
        except requests.exceptions.ChunkedEncodingError:
            return "Connection error."

        # If 200 (OK) then proceeds
        if self.ip_info.status_code == 200:
            self.ip_info = self.ip_info.json()

    def get_openports(self):
        """Request raw data from Censys and decode JSON response."""
        port_list = self.ip_info['protocols']
        return port_list

    def check_heartbleed(self):
        """Check if host service is heartbleed vulnerable."""
        heartbleed_status = (self.ip_info['443']
                                         ['https']
                                         ['heartbleed']
                                         ['heartbleed_vulnerable'])
        return heartbleed_status

    def asn(self):
        """Returns ASN information."""
        asn_info = {'Name': self.ip_info['autonomous_system']['organization'],
                    'CIDR': self.ip_info['autonomous_system']['routed_prefix'],
                    'ASN': self.ip_info['autonomous_system']['asn']}
        return asn_info
