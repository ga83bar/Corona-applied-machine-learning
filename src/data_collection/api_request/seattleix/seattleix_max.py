import requests
import csv
from bs4 import BeautifulSoup

source = requests.get('https://www.seattleix.net/statistics/agg_max_daily.txt').text

soup = BeautifulSoup(source,'lxml')

result = soup.p.text

result = result.split('\n')


with open('seattleix_max.csv','w') as result_file:
    csv.writer = csv.writer(result_file,delimiter='\t')
    for line in result:
        csv.writer.writerow(line.split('\t'))
    

