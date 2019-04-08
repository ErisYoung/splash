# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import quote
from scrapysplash.items import ScrapysplashItem

KEYWORDS=['iPad']
MAX_PAGE=100

class TaobaoSpiderSpider(scrapy.Spider):
    name = 'taobao_spider'
    allowed_domains = ['www.taobao.com']
    base_url="https://s.taobao.com/search?q="

    lua_script = """
    function main(splash, args)
      splash.images_enabled = false
      assert(splash:go(args.url))
      assert(splash:wait(args.wait))
      local image1=splash:png()
      js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()", args.page)
      splash:evaljs(js)
      assert(splash:wait(args.wait))
      local image2=splash:png()
      return {html=splash:html(),ima1=image1,ima2=image2}
    end
    """

    def start_requests(self):
        for keyword in self.settings.get("KEYWORDS"):
            for page in range(1,self.settings.get("MAX_PAGE")+1):
                url=self.base_url+quote(keyword)
                yield SplashRequest(url=url,callback=self.parse,encoding="execute",args={
                    'lua_source':self.lua_script,'page':page,'wait':5
                })

    def parse(self, response):
        products = response.xpath(
            '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
        for product in products:
            item = ScrapysplashItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(
                product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            yield item


