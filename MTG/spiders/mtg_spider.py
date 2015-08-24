import scrapy
import re
import json
from MTG.items import MtgCard

class MTGSpider(scrapy.Spider):
    name = "MTG"
    allowed_domains = ["mtgstocks.com"]
    allowed_sets = [1, 110, 111, 221, 223, 227, 232, 235, 239, 243, 247, 249]
    start_urls = ["http://www.mtgstocks.com/sets/"+str(i) for i in allowed_sets]

    #def parse(self, response):
    #    for href in response.xpath('//li[@class="list"]/a/@href'):
    #        url = response.urljoin(href.extract())
    #        yield scrapy.Request(url, callback=self.parse_single_set)

    def parse(self, response):
        for card in response.xpath('//table[@class="table table-striped table-condensed"]//tr'):
            if not (card.xpath('td[@class="right"]/text()').extract()[0] == "N/A"):
                url = response.urljoin(card.xpath('td/a/@href').extract()[0])
                yield scrapy.Request(url, callback=self.parse_single_card)

    def parse_single_card(self, response):
        card = MtgCard()
        card["name"] = response.xpath('//h2/a/text()').extract()[0]
        card["set"] = response.xpath('//h5/a/text()').extract()[0]
        card["currentValue"] = response.xpath('//div[@class="priceheader average"]/text()').extract()[0]
        card["rarety"] = response.xpath('//div[@class="container"]//h2/text()').extract()[0].replace(u'\xa0',u'')

        # Extract the java script responsible for selecting data from the MTG-stocks price history
        javaScript = response.xpath('//script[@type="text/javascript"]/text()')[0].extract()
        # Extract the json string inside this script
        codeLineMatch = re.search(r'var options = [^;]*;', javaScript)
        jsonMatch = re.search(r'\{.*\}', codeLineMatch.group())
        # Turn the json string into actual json
        jsonData = json.loads(jsonMatch.group())
        # Take the first series of data i.e. the average price
        card["priceHistory"] = jsonData["series"][0]["data"]

        yield card
