import scrapy


class LefigaroSpider(scrapy.Spider):
    name = 'lefigaro'
    #allowed_domains = ['sport24.lefigaro.fr']
    start_urls = ['https://sport24.lefigaro.fr/football/ligue-1/24/2020/calendrier-resultats?journee=1']

    def parse(self, response):
        """Main function that parses the pages"""

        matchs = response.xpath('//div[@class="s24ls-bloc__body"]').extract()
        sum_matchs = len(matchs)

        status  = response.xpath('//span[@class="s24ls-bloc__status"]/text()').extract()
        teams   = response.xpath('//span[@class="s24ls-bloc__team"]/text()').extract()
        results = response.xpath('//span[@class="s24ls-bloc__result"]/text()').extract()

        print(status[5])

        tab = [sum_matchs]

        for i in range (0, sum_matchs) :
            print(i)
            #tab[i]["status"]  = status[i-1]
            #tab[i]["team1"]   = teams[i-1]
            #tab[i]["team2"]   = teams[i]
            #tab[i]["result1"] = results[i-1]
            #tab[i]["result2"] = results[i]

            #print("status": , "team1": teams[i-1], "team1": teams[i], "result1": results[i-1], "result2": results[i])
