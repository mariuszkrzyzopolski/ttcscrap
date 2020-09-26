import scrapy
import re


def clean_result(data):
    non_decimal = re.compile(r'[^\d.]+')
    data = non_decimal.sub('', data)
    return data


def check_if_suggested_price(list):
    original_item_list = list.css('span.gold-amount::text').getall()
    item_list = []
    len_of_list = len(original_item_list)
    for item in original_item_list:
        item_list.append(clean_result(item))
    if len_of_list == 7:
        data = {
            'Min': item_list[0],
            'Average': item_list[1],
            'Max': item_list[2],
            'Suggested-Min': item_list[3],
            'Suggested-Max': item_list[4],
            'No-Listings': item_list[5],
            'No-Items': item_list[6]
        }
    elif len_of_list == 6:
        data = {
            'Min': item_list[0],
            'Average': item_list[1],
            'Max': item_list[2],
            'Suggested-Min': item_list[3],
            'Suggested-Max': item_list[4],
            'No-Listings': item_list[5]
        }
    elif len_of_list == 5:
        data = {
            'Min': item_list[0],
            'Average': item_list[1],
            'Max': item_list[2],
            'No-Listings': item_list[3],
            'No-Items': item_list[4]
        }
    elif len_of_list == 4:
        data = {
            'Min': item_list[0],
            'Average': item_list[1],
            'Max': item_list[2],
            'No-Listings': item_list[3],
        }
    return data


class TtcSpider(scrapy.Spider):
    name = "TTC"
    download_delay = 7.0
    page_number = 252
    start_urls = ['https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=PriceCheck&page=252']

    def parse(self, response):
        rows = response.xpath('//tbody/tr[not(@class)]')

        for row in rows:
            yield {
                'Quality': row.css('div').xpath('@class').get(),
                'Name': row.css('div::text').get(),
                'Level': clean_result(row.css(':nth-child(3) ::text')[1].get()),
                'Price': check_if_suggested_price(row)
            }

        next_page = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=PriceCheck&page=' + \
                    str(TtcSpider.page_number)

        if TtcSpider.page_number <= 5000:
            TtcSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
