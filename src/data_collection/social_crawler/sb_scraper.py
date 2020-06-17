import cloudscraper
from bs4 import BeautifulSoup
from utils import iso_3166_list
import json
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor


class SBScraper:

    def __init__(self):
        pass

    @staticmethod
    def get_all_country_urls(proxies=None):
        scraper = cloudscraper.create_scraper()
        url_list = list()
        for country_code in iso_3166_list:
            url_list.append('https://socialblade.com/youtube/top/country/' + country_code)
        return url_list

    def get_channels_by_country(self, url, proxies=None):
        iso_code = url.split('/')[-1]  # Get the iso code which is always last on sb country urls.
        html_rsp = self._get_url(url, proxies=proxies)
        channel_list = self._extract_channels_from_sb_country(html_rsp)
        # TODO: Catch scraper error and modify dict accordingly
        return {iso_code: channel_list}

    def get_channel_data(self, url, proxies=None):
        html_rsp = SBScraper._get_url(url, proxies=proxies)
        viewer_data = self._extract_channel_data(html_rsp)
        return viewer_data

    @staticmethod
    def _get_url(url, proxies=None):
        scraper = cloudscraper.create_scraper()
        html_rsp = scraper.get(url, proxies=proxies).text
        return html_rsp

    @staticmethod
    def _extract_channels_from_sb_country(html_rsp):
        soup = BeautifulSoup(html_rsp, 'html.parser')
        channel_list = list()
        for link in soup.find_all('a'):
            url = link.get('href')
            if '/youtube/user/' in url:
                channel_list.append('https://socialblade.com' + url + '/monthly')  # Get the detailed statistics page.
        return channel_list

    @staticmethod
    def _extract_channel_data(html_rsp):
        soup = BeautifulSoup(html_rsp, 'html.parser')
        script_list = list()
        for script in soup.find_all('script'):
            SBScraper._parse_js(script)
            script_list.append(str(script))
        print(script_list)
        return str(soup)

    @staticmethod
    def _parse_js(script):
        print(str(script))
        return
        parser = Parser()
        tree = parser.parse(script)
        fields = {getattr(node.left, 'value', ''): getattr(node.right, 'value', '')
                  for node in nodevisitor.visit(tree)
                  if isinstance(node, ast.Assign)}


def main():
    sb_scraper = SBScraper()
    country_url_list = sb_scraper.get_all_country_urls()
    country_dict = sb_scraper.get_channels_by_country(country_url_list[0])
    data = sb_scraper.get_channel_data(country_dict['af'][0])
    with open('C:\\tmp\\crawl\\channel.txt', 'w') as f:
        json.dump(data, f)
    print(country_dict)


if __name__ == '__main__':
    main()
