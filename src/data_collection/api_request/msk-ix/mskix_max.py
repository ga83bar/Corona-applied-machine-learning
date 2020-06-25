import requests
import csv
from bs4 import BeautifulSoup

url = 'https://www.msk-ix.ru/data/json/traffic/ix.all/yearly/?0.615278690833298'

source = requests.get(url)

result_dict = source.json()
# print(result_dict['AVERAGE'][0])

with open('mskix_max.csv','w') as file_max:
    csv.writer = csv.writer(file_max)
    for line in result_dict['MAX']:
        csv.writer.writerow(line)
