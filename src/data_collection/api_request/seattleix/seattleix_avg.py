import requests
import csv
from bs4 import BeautifulSoup

URL = 'https://www.seattleix.net/statistics/agg_avg_daily.txt'
source = requests.get(URL).text
soup = BeautifulSoup(source, 'lxml')

result = soup.p.text

result = result.split('\n')

# test = result[0].split('\t')

with open('seattleix_avg.csv', 'w') as result_file:
    csv.writer = csv.writer(result_file, delimiter='\t')
    for line in result:
        csv.writer.writerow(line.split('\t'))
    