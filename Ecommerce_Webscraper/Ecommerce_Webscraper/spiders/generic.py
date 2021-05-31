import scrapy
import re

def field_validator(field):
    if field:
        field = field
    else:
        field = 'n/a'

    return field

class GenericSpider(scrapy.Spider):
    name = 'generic'
    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    # ]

    def readFile(fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

    start_urls = readFile('urls.txt')

    def parse(self, response):
        # yield {
        #     'text': response.css('title::text').getall(),
        # }
        title = re.sub(r'\s+', ' ', (str(response.css('title::text').get()).strip()))
        product_url = response.url
        brand = response.xpath(
            '//div[@class="sub-title"]/a/text()').extract_first()
        # price = response.xpath('//div[contains(@class, "price")]').extract()
        rawprice = '.'.join(response.css('price::text').extract())
        cleanprice = rawprice.replace('-','00').replace('\n', '').replace(' ','')
        price = cleanprice[:-1]
        description = re.sub(r'\s+', ' ', (str(response.xpath('//div[@id="description"]').get()).strip()))

        # if(description == "None"):
        #     description = re.sub(r'\s+', ' ', (str(response.xpath('//div[has-class("description"])').get()).strip()))


        # rating1 = response.xpath(
        #     '//div[@class="container"]/i/following-sibling::span/text()'
        # ).extract_first()
        # rating2 = response.xpath(
        #     '//div[@class="container"]/following-sibling::footer/text()'
        # ).extract_first()
        # rating = rating1 + ': ' + rating2
        # rating = rating.replace(',', '.')
        # image_urls = response.xpath(
        #     '//div[@id="thumbs-slide"]/a/@href').extract()
        # description = response.xpath(
        #     '//div[@class="description"]').extract()
        # description = ""
        # divs = response.xpath('//div')
        # for div in divs:
        #     if(("description" in str(div.get())) or ("product-single__description" in str(div.get()))):
        #         description = div.get()

        # Validate fields
        title = field_validator(title)
        product_url = field_validator(product_url)
        brand = field_validator(brand)
        price = field_validator(price)
        # rating = field_validator(rating)
        # image_urls = field_validator(image_urls)
        description = field_validator(description)

        yield {
            'title': title,
            # 'product_url': product_url,
            # 'brand': brand,
            # 'price': price,
            # 'rating': rating,
            # 'image_urls': image_urls,
            # 'description': description
        }

    

        

    
