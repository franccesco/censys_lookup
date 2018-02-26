import unittest
from modules import censys
from os import getenv
from dotenv import load_dotenv, find_dotenv


class CensysTest(unittest.TestCase):
    """Testing for censys.py module"""

    def setUp(self):
        """Load variables and API keys"""
        load_dotenv(find_dotenv())
        self.ipaddr = getenv('IPADDR')
        self.ip_info = censys.CensysLookup(self.ipaddr)

    def test_get_openports(self):
        """Check if port list is correctly retrieved."""
        portlist = self.ip_info.get_openports()
        self.assertTrue(portlist)


unittest.main()
