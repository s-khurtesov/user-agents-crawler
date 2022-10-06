# -*- coding: utf-8 -*-
import scrapy


class WhatismybrowserSpider(scrapy.Spider):
    name = 'whatismybrowser'
    allowed_domains = ['developers.whatismybrowser.com']

    def start_requests(self):
        # Only chrome, firefox, opera, safari and internet explorer are supported
        # More browsers could be found at:
        # https://developers.whatismybrowser.com/useragents/explore/software_name/
        common_browsers_links = [
            'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/opera/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/edge/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/internet-explorer/',
        ]
        max_page = getattr(self, 'max_page', 10)

        for link in common_browsers_links:
            for page in range(1, max_page + 1):
                page_link = f'{link}/{page}'
                yield scrapy.http.Request(page_link)

    def parse(self, response, **kwargs):
        ua_elems = response.xpath(
            './/table[contains(@class, "table-useragents")]/tbody'
            '/tr[td[contains(text(), "Computer")] and td[contains(text(), "Very common")]]'
            '/td/a'
        )
        for ua_elem in ua_elems:
            try:
                ua = ua_elem.xpath('./text()').extract_first().strip()
                self.logger.debug('[UserAgent] %s', ua)
                yield {'user_agent_string': ua.strip('"')}
            except Exception as e:
                self.logger.exception(e)
