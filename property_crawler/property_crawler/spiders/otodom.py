import scrapy
from utils.utils import get_data_from_json_file


class PropertyCrawler(scrapy.Spider):
    name = "property"
    settings = get_data_from_json_file("settings.json")
    start_urls = settings["crawled_urls"]

    def parse(self, response):
        for post in response.css('div.offer-item-details'):
            yield {
                'title': post.css('.offer-item-title  ::text').get(),
                'link': post.css('.offer-item-header a::attr(href)').extract()[0],
                'location': post.css('.offer-item-header p::text').get(),
                'price': post.css('.offer-item-price ::text').get().strip(),
                'rooms': post.css('.offer-item-rooms ::text').get(),
                'house_area': post.css('.offer-item-area ::text')[0].get(),
                # 'land_area' : post.css('.offer-item-area ::text')[1].get(),
                'property_type': post.css('.hidden-xs ::text')[0].get().split()[0]
            }
        after = response.css('div.after-offers')
        next_page = after.css('.pager-next a::attr(href)').extract()[0]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
