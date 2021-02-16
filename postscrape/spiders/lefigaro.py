import scrapy
import json


class LefigaroSpider(scrapy.Spider):
    name = 'lefigaro'
    #allowed_domains = ['sport24.lefigaro.fr']
    start_urls = ['https://sport24.lefigaro.fr/football/ligue-1/24/2020/calendrier-resultats?journee=1']

    def parse(self, response):
        """Main function that parses the pages"""

        matchs = response.xpath('//div[@class="s24ls-bloc__body"]').extract()
        sum_matchs = len(matchs)

        status  = response.xpath('//span[@class="s24ls-bloc__status"]/text()').extract() # OK
        teams   = response.xpath('//span[@class="s24ls-bloc__team"]/text()').extract() # OK
        results = response.xpath('//i[@class="s24ls-bloc__result"]/text()').extract()

        print(teams)

        tab = [sum_matchs]

        j = k = 0

        for i in range (0, sum_matchs) :
            line = {} # ligne courante = dictionnaire

            line["status"]  = status[i].strip()

            line["team1"]   = teams[j]
            line["team2"]   = teams[j+1]
            j += 2

            line["result1"] = results[k]
            line["result2"] = results[k+2]
            k += 3

            print(json.dumps(line))
