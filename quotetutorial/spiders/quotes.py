# -*- coding: utf-8 -*-
import scrapy

from quotetutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.tosrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tag = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tag'] = tag
            yield item

        next = response.css('.pager .next a::attr(href)').exreact_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
