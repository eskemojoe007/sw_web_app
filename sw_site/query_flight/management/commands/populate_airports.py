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

        airport_codes = {'code':[],'title':[]}
        for option in options:

            if (not option['value'] == '') and (not option.text.strip().startswith('[')):
                airport_codes['code'].append(option['value'].strip())
                airport_codes['title'].append( option.text.strip().split(' - ')[0])
                # airport_codes[option['value']] = option.text.strip().split(' - ')[0]

        return pd.DataFrame(airport_codes).drop_duplicates()

    def _get_all_airports(self,url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat',proxies=None):
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

        return df

    def _merge_airport_info(self,sw_df,airports_df):
        return pd.merge(sw_df,airports_df,left_on='code',right_on='IATA').drop_duplicates()

        # df_to_airport = df_all[['code','title','Latitude','Longitude','Tz database time zone',]]

    def _add_missing_sw(self,merged_df):

        def app_row(row):
            if len(Airport.objects.filter(abrev = row['code'])) ==0:
                print('Creating {} - {}'.format(row['title'],row['code']))
                Airport.objects.create(
                    title=row['title'],abrev=row['code'],sw_airport=True,latitude=row['Latitude'],
                    longitude=row['Longitude'], timezone=row['Tz database time zone'])
            else:
                print('Already There {} - {}'.format(row['title'],row['code']))

        merged_df.apply(app_row,axis=1)
        # Airport.objects.create(title='Atlanta',abrev='ATL',sw_airport=True,
        #             lattitude=33.6407,longitude=-84.4277)

    def handle(self, *args, **options):
        proxies = {
            'http': 'http://PITC-Zscaler-Americas-Alpharetta3PR.proxy.corporate.ge.com:80',
            'https': 'http://PITC-Zscaler-Americas-Alpharetta3PR.proxy.corporate.ge.com:80'}
        # self._get_all_airports(proxies=proxies)
        # self._get_sw_airports(proxies=proxies)

        self._add_missing_sw(self._merge_airport_info(self._get_sw_airports(proxies=proxies),self._get_all_airports(proxies=proxies)))
