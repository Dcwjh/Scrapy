# Scrapy
这里通过抓取简单网站简单介绍一些Scrapy的用法
* 参考[官方文档](https://doc.scrapy.org/en/latest/)
 
 ## 抓取[http://quotes.toscrape.com/](http://quotes.toscrape.com/)网站
 
 
### 1. 抓取流程
a.  抓取第一页<br/>
b.  获取内容<br/>
c.  翻页爬取<br/>
d.  保存爬取内容<br/>

### 2. Scrapy基本用法

> which scrapy #命令可以查看scrapy的路径<br/>
> scrapy startproject quotetutorial(项目名称) #创建一个项目<br/>
> cd quotetutorial <br/>
> ls<br/>
> scrapy genspider quotes quotes.toscrape.com #爬取网站<br/>
> ls<br/>
> cd spiders  #爬取的主要代码在这里面<br/>
 
 
 #### 3.1 抓取第一页 <br/><br/>
 * quotetutorial/spider/quotes.py
 ```python
# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.tosrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
      return response.text
 ```
 <br/>
 
* quotetutorial/spiders/items.py
```python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
 ```
 > scrapy crawl quotes<br/>
 
  #### 3.2 抓取内容 <br/><br/>
 * quotetutorial/quotes.py
 ```python
# -*- coding: utf-8 -*-
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.tosrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tag = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tag'] = tag
            yield item
 ```
 <br/>
 
* quotetutorial/items.py
```python
class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tag =  scrapy.Field()
 ```
 ## 简单介绍Scrapy shell交互
 
 > scrapy shell quotes.toscrape.com # shell交互命令<br/>
 > response<br/>
 > quotes = response.css('quote')<br/>
 > qutoes # css  selector一种选择器 <br/>
 > qutoes[0]  # 输出第一个元素<br/>
 > quotes[0].css('.text')<br/>
 > quotes[0].css('.text::text')<br/>
 > quotes[0].css('.text::text').extract() # 返回一个列表<br/> 
 > text = quote.css('.text::text').extract_first() # 返回第一个元素<br/>
 
 #### 3.3 翻页抓取 <br/><br/>
  
 * quotetutorial/quotes.py
 ```python
 class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.tosrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tag = quote.css('.tags .tag::text').extract()
            item['text'] = text
            item['author'] = author
            item['tag'] = tag
            yield (item)

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)
```
 #### 3.4 保存内容 <br/><br/>
 
 ##### 保存为文件形式
 
 > :scrapy crawl quotes -o quotes.json   #.csv  .jl  .json  .marshal  .pickle   .xml<br/>
 > :scrapy crawl quotes -o quotes.
 
 
 
 * pipelines.py
 ##### 保存到数据库
 
 ```python
 class MongoPipleline(object):

    def __init__(self):
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['quotestutorial']

    def process_item(self,item,spider):
        self.db['quotes'].insert(dict(item))  # 字典形式
        return item

    def close_spider(self):
        self.client.close()
```
 ##### 数据处理
```python
class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + "..."
            return item
        else:
            return DropItem("Missing Text")
```
