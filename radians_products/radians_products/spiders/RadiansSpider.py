import scrapy
from bs4 import BeautifulSoup
import re
import ast
import string
from radians_products.items import RadiansProductsItem

class RadiansSpider(scrapy.Spider):
    name = 'Radiansspider'
    allowed_domains = ['www.radians.com', 'images.salsify.com/']
    # have to manually change the pagination
    start_urls = ['https://www.radians.com/industrial-safety/eye-protection/safety-goggles']


    def __init__(self):
        self.declare_xpath()

    def declare_xpath(self):


        self.getAllItemsXpath = '//*[@id="products"]/li/a/@href'
        self.getAllSubItemsXpath = '//*[@id="main-content"]/div/template/option/text()'
        self.TitleXpath = '//*[@id="main-content"]/div/div[has-class("product")]/div[has-class("product-overview")]/h1/text()'
        self.SkuXpath = ''
        self.DescriptionXpath = '//*[@id="main-content"]/div/div[has-class("product")]/div[has-class("product-overview")]/p/text()'
        self.VariationsXpath = '/html/body/main/div/template[1]/@data-products'
        self.Parent_skuXpath = '/html/body/main/div/template[1]/@id'
        self.ImagesXpath = '//*[@id="main-content"]/div/template/figure/span/img/@data-flickity-lazyload-src'
        self.FeaturesXpath = ''
        self.SpecsXpath = ''
        self.WarningXpath = '//*[@id="main-content"]/div/div[has-class("product")]/div[has-class("product-prop65")]/p/b/text()'
        self.CancerXpath = '//*[@id="main-content"]/div/div[has-class("product")]/div[has-class("product-prop65")]/p/text()'
        self.Prop65LinkXpath = '//*[@id="main-content"]/div/div[has-class("product")]/div[has-class("product-prop65")]/p/a/@href'

    def parse(self, response):
        for href in response.xpath(self.getAllItemsXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url=url, callback=self.parse_main_item, dont_filter=True)

        print(url)


    def parse_main_item(self, response):
        item = RadiansProductsItem()

        Title = response.xpath(self.TitleXpath).extract()
        Title = self.cleanText(self.parseText(self.listToStr(Title)))

        Description = response.xpath(self.DescriptionXpath).extract()
        Description = self.cleanText(self.parseText(self.listToStr(Description)))
        Variations = response.xpath(self.VariationsXpath).extract_first()
        Parent_sku = response.xpath(self.Parent_skuXpath ).extract_first()
        image_urls = [response.xpath(self.ImagesXpath).extract_first()]
        # needed to replace https:/// with https:// or image downloader wouldn't work invalid domain
        image_urls = [image_urls[0].replace('https:///', 'https://')]
        print(image_urls)
        var_list = ast.literal_eval(Variations)
        print(var_list[0])
        # print(var_list[0].rstrip('OGogxXsmlSML23456'))
        item['Title'] = Title
        item['Description'] = Description
        item['image_urls'] = image_urls

        item['image_name'] = Title
        item['Variations'] = Variations
        item['Parent_sku'] = Parent_sku
        item['Warning'] = ' WARNING: Cancer and reproductive harm. California ' \
                          'residents click here: https://www.radians.com/prop-65-warning'

        return item


    def listToStr(self, MyList):
        dumm = ""
        MyList = [i.encode("ascii", "ignore") for i in MyList]
        for i in MyList: dumm = "{0}{1}".format(dumm, i)
        return dumm

    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        # print(soup)

        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0", ' ', soup.get_text()).strip()

    def cleanText(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        print(text)
        text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+", ' ', text).strip()

        # remove non ascii characters



        # strip off the quotes using a variable and f-string
        text = text.lstrip(r'b')
        text = re.sub(r"(?:')", '', text).strip()
        text = re.sub(r".*(?:')", '', text).strip()
        text = re.sub(r'(?:")', '', text).strip()
        text = re.sub(r'.*(?:")', '', text).strip()
        return text
