import datetime
import requests
import bs4
arp_st = "https://ucsol.ru/tamozhennoe-oformlenie/v-" + \
         "aeroportakh-uslugi-tamozhennogo-brokera/"

def validator(method, data):
    if method == 'POST':
        if len(data) == 0:
            return 400, "No content"
        if len(data) != 6:
            return 400, "Incorrect data. Current schema: {'id', 'departure'," \
                        " 'arrival', 'flight_time', 'airport', 'plane'}"
    for key in data.keys():
        if key in ['id', 'departure', 'arrival', 'flight_time',
                   'airport', 'plane']:
            if key == 'id':
                if not isinstance(data.get('id'), int):
                    return 400, "Incorrect data. Supported type for id is int"
            if key == 'departure':
                try:
                    datetime.datetime.strptime(data['departure'],
                                               '%a, %d %b %Y %H:%M:%S GMT')
                except ValueError:
                    return 400, "Incorrect data. Supported type " \
                                "for departure and arrival is str like " \
                                "'Tue, 12 Jun 2012 14:03:10 GMT'"
            if key == 'arrival':
                try:
                    datetime.datetime.strptime(data['arrival'],
                                               '%a, %d %b %Y %H:%M:%S GMT')
                except ValueError:
                    return 400, "Incorrect data. Supported type " \
                                "for departure and arrival is str like " \
                                "'Tue, 12 Jun 2012 14:03:10 GMT'"
            if key == 'flight_time':
                try:
                    datetime.datetime.strptime(data['flight_time'],
                                               '%H:%M GMT')
                except ValueError:
                    return 400, "Incorrect data. Supported type for " \
                                "flight_time is str like '%H:%M GMT'"
            if key == 'airport':
                arp = data['airport']
                if len(arp) != 3 or not arp.isupper():
                    return 400, """Incorrect data.
                    Supported type for airport is str in IATA format"""
                if arp[0] == 'A':
                    req = requests.request(
                        method="GET", url = arp_st +
                                            "kody-vsekh-aeroportov-mira-iata")
                    s = bs4.BeautifulSoup(req.text, 'html.parser')
                    lst = [y.text[1:4] for y in s.findAll('tr')]
                    if arp not in lst:
                        return 400, "Incorrect data. Current airport not found"
                else:
                    req = requests.request(method="GET",
                        url = arp_st + f"""/airport-codes
                        -{arp[0].lower()}a-{arp[0].lower()}z""")
                    s = bs4.BeautifulSoup(req.text, 'html.parser')
                    lst = [y.text[1:4] for y in s.findAll('tr')]
                    if arp not in lst:
                        return 400, "Incorrect data. Current airport not found"
        else:
            return 400, "Incorrect data. Current schema: {'id','departure'," \
                        " 'arrival', 'flight_time', 'airport', 'plane'}"
    return 200, 'OK'