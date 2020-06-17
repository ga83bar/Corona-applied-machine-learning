from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random
import time
import cloudscraper
import json
import os
from utils import iso_3166_list


class ProxyRandomizer:
    
    def __init__(self):
        self.refresh() 

    def refresh(self):
        self.proxies = []
        self.last_refresh = time.time()
        self.count_uses = 0
        # Retrieve latest proxies
        proxies_req = Request('http://free-proxy-list.net//')

        proxies_req.add_header('User-Agent',"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
        proxies_doc = urlopen(proxies_req).read().decode('utf8')

        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Save proxies in the array
        for row in proxies_table.tbody.find_all('tr'):
            self.proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
            })
        
    # Retrieve a random index proxy (we need the index to delete it if not working)
    def random_proxy(self):
        # if the proxy is used too much or too old refresh
        if self.count_uses > 100 or time.time() - self.last_refresh > 60*5 or len(self.proxies) == 0:
            self.refresh()
        self.count_uses += 1
        index = random.randint(0, len(self.proxies) - 1)
        proxy = self.proxies[index]
        self.proxies.remove(proxy)
        return proxy


def get_all_sb_country_urls():
    url_list = list()
    for country_code in iso_3166_list:
        url_list.append('https://socialblade.com/youtube/top/country/' + country_code)
    return url_list


def main():

    scraper = cloudscraper.create_scraper()
    country_url_list = get_all_sb_country_urls()
    html_rsp = scraper.get(country_url_list[0]).text
    soup = BeautifulSoup(html_rsp, 'html.parser')
    channel_list = list()
    for link in soup.find_all('a'):
        url = link.get('href')
        if '/youtube/user/' in url:
            channel_list.append(url)
    for el in channel_list:
        print(el + '\n')
    print(len(channel_list))

    with open(os.path.join('C:\\tmp\\crawl', 'country.txt'), 'w') as f:
        json.dump(html_rsp, f)


if __name__ == '__main__':
    main()