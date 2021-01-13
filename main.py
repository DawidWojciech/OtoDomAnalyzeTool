from property_crawler.property_crawler.spiders.otodom import PropertyCrawler
from scrapy.crawler import CrawlerProcess
from property_data_parser.map import MapGenerator


process = CrawlerProcess(settings={"FEEDS": {
    "items.json": {
        "format": "json"},
},
})

if __name__ == '__main__':

    process.crawl(PropertyCrawler)
    process.start()

    map_generator = MapGenerator(data_file='items.json', map_file='data.html')
    map_generator.generate_markers()
    map_generator.generate_map()
