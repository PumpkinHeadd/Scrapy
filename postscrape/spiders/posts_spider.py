import scrapy

class PostsSpider(scrapy.Spider):
    name = "posts"
    
    start_urls = [
        "https://www.zyte.com/blog/"
    ]

    
    def parse(self, response):
        for post in response.css('div.oxy-post'):#On parse la page
            yield {
                'title': post.css('.oxy-post-wrap a::text').get(),
                'date': post.css('.oxy-post-image div::text')[1].get(),
                'author': post.css('.oxy-post-wrap div div div::text')[0].get()
            }

        #On récupère le lien de la prochaine page
        next_page = response.css('a.next::attr(href)').get()
        #On s'assure que le lien existe
        if next_page is not None:
            #On rejoint la nouvelle page
            next_page = response.urljoin(next_page)
            #On fait un appel récursif pour scrape la page suivante
            yield scrapy.Request(next_page, callback=self.parse)