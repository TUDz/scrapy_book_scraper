import scrapy 

class Books(scrapy.Spider):
    NEXT_PAGE_PATTERN = '//ul[@class="pager"]//a[starts-with(text(), "next")]/@href'
    LINKS_BOOK_PATTERN = '//article[@class="product_pod"]//h3/a/@href'
    CATEGORY_PATTERN = '//ul[@class="breadcrumb"]/li[3]/a/text()'
    BOOK_TITLE_PATTERN = '//article[@class="product_page"]//h1/text()'
    BOOK_PRICE_PATTERN = '//article[@class="product_page"]//p[@class="price_color"]/text()'
    IN_STOCK_PATTERN = '//table[contains(@class, "table-striped")]//tr[6]//td/text()'

    name = 'books'
    start_urls = [
            'http://books.toscrape.com/',
        ]

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'FEED_URI': 'books.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }


    def parse(self, response):
        links_to_books = response.xpath(self.LINKS_BOOK_PATTERN).getall()

        for link in links_to_books:
            yield response.follow(link, callback=self.parse_book_content, cb_kwargs={'url': response.urljoin(link)})
    
        next_page_link = response.xpath(self.NEXT_PAGE_PATTERN).get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_book_content(self, response, **kwargs):
        link = kwargs['url']
        category = response.xpath(self.CATEGORY_PATTERN).get()
        book_title = response.xpath(self.BOOK_TITLE_PATTERN).get()
        book_price = response.xpath(self.BOOK_PRICE_PATTERN).get()
        in_stock = response.xpath(self.IN_STOCK_PATTERN).get()

        yield {
            'book_title': book_title,
            'category': category,
            'book_price': book_price,
            'in_stock': in_stock,
            'link': link
        }