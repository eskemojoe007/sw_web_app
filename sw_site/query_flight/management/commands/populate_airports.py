from django.core.management.base import BaseCommand
from query_flight.models import Airport
import requests
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd


def get_verify(proxies):
    if proxies is None:
        return None
    else:
        return False

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'use this to reach out to the web and get the sw airports'

    def _get_sw_airports(self,url='https://www.southwest.com/flight/search-flight.html',proxies=None):
        verify = get_verify(proxies)
        request_obj = requests.get(url,proxies=proxies,verify=verify)

        soup = BeautifulSoup(request_obj.content,'html.parser')

        options = soup.find(attrs={'class':'stationInput','id':'originAirport'}).findAll('option')

        airport_codes = {}
        for option in options:

            if (not option['value'] == '') and (not option.text.strip().startswith('[')):
                airport_codes[option['value']] = option.text.strip().split(' - ')[0]

        return airport_codes

    def _get_all_aiports(self,url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat',proxies=None):
        verify = get_verify(proxies)
        response = requests.get(url,proxies=proxies,verify=verify)

        df = pd.read_csv(StringIO(response.text),index_col=0,
            names=['Airport ID',
            'Name',
            'City',
            'Country',
            'IATA',
            'ICAO',
            'Latitude',
            'Longitude',
            'Altitude',
            'Timezone',
            'DST',
            'Tz database time zone',
            'Type',
            'Source'], na_values=['\\N'])

        print(df)


    def handle(self, *args, **options):
        proxies = {
            'http': 'http://PITC-Zscaler-Americas-Alpharetta3PR.proxy.corporate.ge.com:80',
            'https': 'http://PITC-Zscaler-Americas-Alpharetta3PR.proxy.corporate.ge.com:80'}
        self._get_all_aiports(proxies=proxies)
