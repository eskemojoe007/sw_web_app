# Imports
from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from pandas import to_timedelta,to_datetime
from django.utils import timezone
from .models import Flight, Layover, Airport, Search




class SW_Sel_Search():
    def __init__(self,browser=None,**kwargs):
        if browser is None:
            browser = self.get_browser()
        self.browser = browser

        # Set all the kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.search = Search.objects.create()

    def get_browser(self):
        chrome_options = Options()
        chrome_options.set_headless(True)
        chrome_driver = os.path.join('query_flight','static','query_flight',"chromedriver.exe")
        return webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)


    def get_sw_url(self):
        payload = {
            'adultPassengersCount':1,
            'departureDate':self.departureDate,
            'departureTimeOfDay':'ALL_DAY',
            'destinationAirportCode':self.destinationAirportCode,
            'fareType':'USD',
            'int':'HOMEQBOMAIR',
            'leapfrogRequest':True,
            'originationAirportCode':self.originationAirportCode,
            'passengerType':'ADULT',
            'promoCode':'',
            'returnAirportCode':'',
            'returnDate':'',
            'returnTimeOfDay':'ALL_DAY',
            'seniorPassengersCount':0,
            'tripType':'oneway'}
        params = urllib.parse.urlencode(payload)
        url = "https://www.southwest.com/air/booking/select.html?"
        return url + params


    def get_result_soup(self,url=None,browser=None,timeout=30):
        if browser is None:
            browser = self.browser
        if url is None:
            url = self.get_sw_url()

        browser.get(url)
        try:
            # webdriver might be too fast. Tell it to slow down.
            wait = WebDriverWait(browser, timeout)
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "currency_dollars")))
        except TimeoutError:
            pass
        return BeautifulSoup(browser.page_source,'html.parser')

    def save_all_flights(self,**kwargs):

        soup = self.get_result_soup(**kwargs)
        outbound_table = soup.findAll('ul')[2]
        outbounds = outbound_table.findAll('li',attrs={'class':'air-booking-select-detail'})

        # outbound = outbounds[1]
        for outbound in outbounds:
            # print(self.get_row_flight_numbers(outbound))
            # print(self.get_row_stops(outbound))
            # print(self.get_row_time(outbound,'origination'))
            # print(self.get_row_time(outbound,'destination'))
            # print(self.get_row_total_time(outbound))
            # print(self.get_layover_cities_times(outbound))
            # print(self.get_row_prices(outbound))


            origin_airport = Airport.objects.get(pk=self.originationAirportCode)
            destination_airport = Airport.objects.get(pk=self.destinationAirportCode)
            depart_time = self.get_row_time(outbound,'origination')
            depart_date_time = '{} {}'.format(self.departureDate, depart_time)
            arrive_time = self.get_row_time(outbound,'destination')
            if arrive_time.endswith('Next'):
                adder = to_timedelta('1d')
                arrive_time = arrive_time.replace('Next','')
            else:
                adder = timezone.timedelta(0)

            arrival_date = to_datetime(self.departureDate) + adder


            arrive_date_time = '{} {}'.format(arrival_date.strftime('%Y-%m-%d'), arrive_time)
            prices = self.get_row_prices(outbound)

            # print(origin_airport)
            # print(destination_airport)
            # print(origin_airport.get_tz_obj().localize(to_datetime(depart_date_time)))
            # print(destination_airport.get_tz_obj().localize(to_datetime(arrive_date_time)))

            f = Flight.objects.create(
                origin_airport=origin_airport,
                destination_airport = destination_airport,
                depart_time = origin_airport.get_tz_obj().localize(to_datetime(depart_date_time)),
                arrive_time = destination_airport.get_tz_obj().localize(to_datetime(arrive_date_time)),
                wanna_get_away = prices.get('Wanna Get Away'),
                anytime = prices.get('Anytime'),
                business_select = prices.get('Business Select'),
                search = self.search
                )

            layovers,duration,change_planes = self.get_layover_cities_times(outbound)
            for layover,duration,change_plane in zip(layovers,duration,change_planes):

                l = Layover.objects.create(
                    airport = Airport.objects.get(pk=layover),
                    flight = f,
                    change_planes = change_plane,
                    time = duration.total_seconds()
                )
            # Flight.object.create(
            #     origin_airport = Airport.objects.get(pk=self.originationAirportCode),
            #     destination_airport = Airport.objects.get(pk=self.destinationAirportCode),
            #     depart_time =
            # )




    def get_row_flight_numbers(self,row_soup):
        # Returns a list of all the flight numbers for the given flight.
        fns_raw = row_soup.find('button',attrs={'class':'flight-numbers--flight-number'}).find('span',{'class':'actionable--text'}).text
        return list(map(str.strip,fns_raw.replace("#","").strip().split('/')))

    def get_row_stops(self,row_soup):
        stops_raw = row_soup.find('div',{'class':'select-detail--flight-stops-badge'}).text.strip()

        if 'nonstop' in stops_raw.lower():
            return 0
        else:
            return int(stops_raw.lower().replace('stops','').replace('stop','').strip())

    def get_row_time(self,row_soup,key):
        return row_soup.find('div',{'type':key}).text.strip().split(' ',2)[1]

    def get_row_total_time(self,row_soup):
        return to_timedelta(row_soup.find('span', {'class':'flight-stops--duration-time'}).text.strip())

    def get_layover_cities_times(self,row_soup):
        stops_raw = row_soup.findAll('div',{'class':'flight-stops--item-text'})

        layovers = []
        duration = []
        change_planes = []
        for stop_raw in stops_raw:
            if 'flight-stops--item_plane-change' in stop_raw.parent['class']:
                change_planes.append(True)
            else:
                change_planes.append(False)
            layovers.append(stop_raw.find('button').find('span',{'class':'actionable--text'}).text.strip())
            duration.append(to_timedelta(stop_raw.find('span',{'class':'flight-stops--item-description'}).text.strip()))
        return layovers,duration,change_planes

    def get_row_prices(self,row_soup):
        # return list(map(lambda x: x.text,row_soup.findAll('span',{'class':'fare-button--value-total'})))
        fare_boxes = row_soup.find('div',{'class':'select-detail--fares'}).findAll('div',{'class':'select-detail--fare'})
        fares = {'Business Select':None,'Anytime':None,'Wanna Get Away':None}
        for fare_box in fare_boxes:
            if not 'fare-button_disabled' in fare_box['class']:
                b = fare_box.find('button',{'class':'fare-button--button'})
                label = b['aria-label']
                for fare_type in fares.keys():
                    if label.startswith(fare_type):
                        fares[fare_type] = float(b.find('span',{'class':'fare-button--value-total'}).text.strip())
        return fares
