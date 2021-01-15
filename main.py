import os

from property_crawler.property_crawler.spiders.otodom import PropertyCrawler
from scrapy.crawler import CrawlerProcess
from property_data_parser.map import MapGenerator
from property_data_parser.offers import OfferParser


process = CrawlerProcess(settings={"FEEDS": {
    "offers.json": {
        "format": "json"},
},
})

offer_parser = OfferParser('offers.json')

if __name__ == '__main__':

    # process.crawl(PropertyCrawler)
    # process.start()
    # offer_parser.save_as_json('parsed.json')
    map_generator = MapGenerator(data_file="parsed.json", map_file='data.html')
    map_generator.add_markers_to_map()
    map_generator.generate_map()

    # os.remove("offers.json")
