import scrapy
import json
import dateparser
import sys
import re

class LefigaroSpider(scrapy.Spider):
    name = 'lefigaro'
    start_urls = []

    def __init__(self, category='', base_url = 'https://sport24.lefigaro.fr/football/ligue-1/24/2020/calendrier-resultats', days = '1', **kwargs):
        """ Fonction init utile pour scraper plusieurs jours (passés en argument) ou un autre sport du même site """
        if int(days) > 1 :
            for i in range(1, int(days)) :
                self.start_urls.append(base_url + '?journee=' + str(i))
        else :
            self.start_urls.append(base_url + '?journee=' + days)


        print(self.start_urls)
        print("Initialisation effectuée")

        super().__init__(**kwargs)

    def parse(self, response):
        """Main function that parses the pages"""
        print("Parsing en cours")

        # Extraction des jours de compétition de la page
        parsedDays = self.cleanup(response.xpath('//div[@class="s24ls__slice"]//div//div[@class="s24ls-h3__content"]/text()').extract())

        #print(parsedDays)
        #print(dateparser.parse('samedi 22 août 2020').date())
        #print("taille" + str(len(parsedDays)))

        results1 = response.xpath('//div[@class="s24ls-bloc__body"]//div//i[1]/text()').extract()
        results2 = response.xpath('//div[@class="s24ls-bloc__body"]//div//i[3]/text()').extract()

        teams1   = response.xpath('//div[@class="s24ls-bloc__body"]//div[2]//span/text()').extract()
        teams2   = response.xpath('//div[@class="s24ls-bloc__body"]//div[4]//span/text()').extract()

        status   = response.xpath('//span[@class="s24ls-bloc__status"]/text()').extract() # OK

        date   = [None] * len(results1) # On remplit de valeurs vides notre tableau du jour

        # Accumulateur pour insérer la date ensuite (assez bizarre comme fonctionnement mais nécessaire au vu de la structure du site à scraper)
        k = 0

        # On parcourt les jours
        for i in range(0, len(parsedDays)) :
            # On convertit la date littérale française en date normalisée
            parsedDate = str(dateparser.parse(parsedDays[i]).date())

            # On récupère le nb de matchs de ce jour
            matchs = response.xpath('//div[@class="s24ls__slice"]['+ str(i+2) +']//div[@class="s24ls-bloc__body"]').extract()

            #print("Parsing : ", parsedDate)
            #print("Nb matchs du jour : ", len(matchs))

            # On boucle et on complète notre tableau
            for j in range(0, len(matchs)) :
                date[k] = parsedDate
                k += 1

        #print(date)

        # On génère du JSON pour la sortie
        for i in range (0, len(results1)) :
            yield {
                "team1": teams1[i],
                "team2": teams2[i],
                "results1": results1[i],
                "results2": results2[i],
                "status": status[i].strip(),
                "day": date[i],
            }

    def cleanup(self, list) :
        """Removes \n & \t in list of strings"""
        res = []
        for sub in list:
            res.append(sub.replace("\n", "").strip())

        return res
