# -*- coding: utf-8 -*-
import scrapy

from quotetutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote') #通过css选择器获取quote
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()#通过css选择器获取text的内容（第一个）
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract() #获取所有内容
            # 提取item的内容
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        # 翻页
        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        # callback=self.parse参数表示递归调用自己
        yield scrapy.Request(url=url, callback=self.parse)