# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
import json, re, random, requests
from scrapy.utils.project import get_project_settings
from collections import OrderedDict

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class zaraSpider(Spider):
    name = "zara"
    start_urls = ['https://www.zara.com/tr/tr/kadin-ayakkabilar-bilekte-botlar-l1259.html?v1=1074517',
                  'https://www.zara.com/tr/tr/erkek-ayakkabilar-botlar-l781.html?v1=1079358']
    # domain1 = 'https://www.lowes.com/'

    use_selenium = False
    count = 0
    pageIndex = 1
    totalpage= None
    # custom_settings = {
     #    'COOKIES_ENABLED': False
	# }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback= self.parse, meta={"next_count": 1})

    def parse(self, response):
        urls = response.xpath('//div[@class="product-info-item product-info-item-name"]/a/@href').extract()
        for url in urls:
            yield Request(url, self.parse_product)
    def parse_product(self, response):
        item = OrderedDict()
        item['title'] = response.xpath('//h1[@class="product-name"]/text()').extract_first()
        item['url'] = response.url
        json_data = json.loads(re.findall('window.zara.dataLayer = (.*?)};', response.body)[0] + '}')
        item['price'] = float(json_data['product']['price'])/100.0
        item['product code'] = response.xpath('//span[@data-qa-qualifier="product-reference"]/text()').extract_first()
        urls = response.xpath('//a[@class="_seoImg main-image"]/@href').extract()
        images = []
        for imag in urls:
            img = response.urljoin(imag)
            if '/w/560/' in img:
                img = img.replace('/w/560/', '/w/1920/')
                images.append(img)

        item['image urls'] = ','.join(images)
        item['color'] = response.xpath('//p[@class="product-color"]/span[@class="_colorName"]/text()').extract_first()
        yield item

