import scrapy
import json

class LefigaroSpider(scrapy.Spider):
    name = 'lefigaro'
    #allowed_domains = ['sport24.lefigaro.fr']
    start_urls = [
        'https://sport24.lefigaro.fr/football/ligue-1/24/2020/calendrier-resultats',
    ]

    def buildStartUrls(self, response):
        """Fonction chargée de récupérer les URL des résultats sportifs de toute une saison"""

        # Le dernier nb matché correspond à la dernière journée en cours de la compétition
        max = response.xpath('//h1//span/text()').re(r"[1-9][0-9]?")
        start_url = self.start_urls[0]
        self.start_urls = []

        for i in range(1, int(max[-1])) :
            self.start_urls.append(start_url + '?journee='+ str(i))

    def parse(self, response):
        """Main function that parses the pages"""

        self.buildStartUrls(response)

        results1 = response.xpath('//div[@class="s24ls-bloc__body"]//div//i[1]/text()').extract()
        results2 = response.xpath('//div[@class="s24ls-bloc__body"]//div//i[3]/text()').extract()

        teams1   = response.xpath('//div[@class="s24ls-bloc__body"]//div[2]//span/text()').extract()
        teams2   = response.xpath('//div[@class="s24ls-bloc__body"]//div[4]//span/text()').extract()

        status   = response.xpath('//span[@class="s24ls-bloc__status"]/text()').extract() # OK

        print(json.dumps(results1))
        print(json.dumps(self.start_urls))

        # Pages * enregistrements par page
        tab = [len(status)]
        for i in range (0, len(status)) :
            line = {} # ligne courante = dictionnaire

            line["status"]  = status[i].strip()

            line["team1"]   = teams1[i]
            line["team2"]   = teams2[i]

            line["result1"] = results1[i]
            line["result2"] = results2[i]

            print(json.dumps(line))
