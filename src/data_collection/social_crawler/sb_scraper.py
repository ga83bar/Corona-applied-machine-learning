import cloudscraper
from bs4 import BeautifulSoup
import json
import js2xml
import requests
import random


class SBScraper:

    def __init__(self):
        pass

    def get_all_country_urls(self, proxies=None):
        html_rsp = self._get_url('https://socialblade.com/youtube/top/100', proxies=proxies)
        if not html_rsp:
            return False
        country_id_list = self._extract_country_ids(html_rsp)
        url_list = list()
        for country_id in country_id_list:
            url_list.append('https://socialblade.com/youtube/top/country/' + country_id)
        return url_list

    def get_channels_by_country(self, url, proxies=None):
        country_id = url.split('/')[-1]  # The country id iso code is always last on sb country urls.
        html_rsp = self._get_url(url, proxies=proxies)
        if not html_rsp:
            return False
        channel_list = self._extract_channels_from_sb_country(html_rsp)
        return {country_id: channel_list}

    def get_channel_data(self, url, proxies=None):
        html_rsp = self._get_url(url, proxies=proxies)
        if not html_rsp:
            return False
        data_dict = self._extract_channel_data(html_rsp)
        return data_dict

    @staticmethod
    def _get_url(url, proxies=None):
        scraper = cloudscraper.create_scraper()
        # TODO: catch all network related errors.
        try:
            html_rsp = scraper.get(url, proxies=proxies).text
            return html_rsp
        except requests.exceptions.ProxyError as e:
            print('Error in SBScraper._get_url with url {} and proxy {}.'.format(url, proxies))
            print('Error message was: {}'.format(e))
            return False

    @staticmethod
    def _extract_country_ids(html_rsp):
        soup = BeautifulSoup(html_rsp, 'html.parser')
        country_id_list = list()
        for option in soup.find_all('option'):
            c_id = option.get('value')
            # Only country ids have len 2 on this website. Filter out non values to avoid errors.
            if c_id is not None and len(c_id) == 2 and c_id not in country_id_list:
                country_id_list.append(c_id)
        return country_id_list

    @staticmethod
    def _extract_channels_from_sb_country(html_rsp):
        soup = BeautifulSoup(html_rsp, 'html.parser')
        channel_list = list()
        for link in soup.find_all('a'):
            url = link.get('href')
            if '/youtube/user/' in url:
                channel_list.append('https://socialblade.com' + url + '/monthly')  # Get the detailed statistics page.
        return channel_list

    def _extract_channel_data(self, html_rsp):
        soup = BeautifulSoup(html_rsp, 'html.parser')
        script = self._filter_scripts(soup.find_all('script'))
        data_dict = self._parse_js(script)
        return data_dict

    @staticmethod
    def _filter_scripts(scripts):
        for script in scripts:
            if script.contents and len(script.contents[0]) > 1000:  # Target script is the only one with > 1000 chars.
                return script.contents[0]

    def _parse_js(self, script):
        parsed = js2xml.parse(script)
        # Find all highchart identifiers and their data in the xml'ified js tree.
        categories = [c.xpath('./../../../../arguments/string')
                      for c in parsed.xpath("//identifier[@name='Highcharts']")]
        data = [d.xpath("./array/array/number/@value") for d in parsed.xpath("//property[@name='data']")]
        # Remove empty arrays from bad relative paths, access string content, strip unnecessary parts.
        categories = self._process_categories(categories)
        data = self._process_data(data)
        return dict(zip(categories, data))

    @staticmethod
    def _process_categories(categories):
        categories = [c[0].text for c in categories if c and 'graph' in c[0].text]
        for bad_str in ['graph-youtube-', '-container']:
            categories = [c.replace(bad_str, '') for c in categories]
        return categories

    @staticmethod
    def _process_data(data):
        for array in data:
            # Check if time is inverted. If so, reverse array while keeping the time/data structure.
            if array[0] > array[2]:
                buff_1 = array[::2][::-1]
                buff_2 = array[1::2][::-1]
                array[::2] = buff_1
                array[1::2] = buff_2
        return data


def main():
    sb_scraper = SBScraper()
    country_url_list = sb_scraper.get_all_country_urls()
    print(country_url_list)
    for _ in range(10):
        i = random.randint(0, len(country_url_list) - 1)
        country_dict = sb_scraper.get_channels_by_country(country_url_list[i])
        key = list(country_dict.keys())[0]
        j = random.randint(0, len(country_dict[key]) - 1)
        print(country_dict)
        data = sb_scraper.get_channel_data(country_dict[key][j])
        for key, val in data.items():
            print(key, val)
    with open('C:\\tmp\\crawl\\channel.txt', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
