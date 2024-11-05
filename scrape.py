import scrapy

class LazadaSpider(scrapy.Spider):
    name = "lazada"
    start_urls = [
        'https://www.lazada.vn'
    ]
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            })
    def parse(self, response):
        yield {
            "res": response.css('a').get()
        }

        next_page = response.css('a.ant-pagination-item-link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)