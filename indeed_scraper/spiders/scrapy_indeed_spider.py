import scrapy
from scrapy.http.request import Request
from indeed_scraper.items import Offer


class ScrapyIndeedSpiderSpider(scrapy.Spider):
    name = "scrapy_indeed_spider"
    allowed_domains = ["www.indeed.com"]
    start_urls = ["https://www.indeed.com/q-usa-jobs.html?vjk=6962ff22d345874c"]
    
    def start_requests(self):
        user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/45.0.2454.85 Safari/537.36')
        cookie = 'CTK=1hk9cifucj5le800; RF="TFTzyBUJoNr6YttPP3kyivpZ6-9J49o-Uk3iY6QNQqKE2fh7FyVgtZ_oS5kJHIG15wzdhT5eKkA="; INDEED_CSRF_TOKEN=F47fsYCbgwwLQPmh6yVj8oi7NfKieHSZ; _gcl_au=1.1.1177260853.1705417197; _ga=GA1.2.889599877.1705417197; _gid=GA1.2.697592064.1705417197; SURF=UoajWBY3mykZzbIUiic10iB3aquUmpKY; gonetap=1; SHARED_INDEED_CSRF_TOKEN=F47fsYCbgwwLQPmh6yVj8oi7NfKieHSZ; LC="co=JP"; _cfuvid=Y9B3MY_urilUJMdG5G6SfhPDLadryTN58oo6v50zVps-1705417298938-0-604800000; g_state={"i_l":0}; SOCK="ZpgM3-XixJsxSUwuLtQlA06KxlE="; SHOE="kqL7UHjQjvp5CClA32zkkW5VEX2usEjIIuxVrqyI2NPBnJ8uqC4Yom5mMC4BEocFq8rmL0Dv-vhvOiGnC49Nu28VqevYz8Byv3urk9K01z-LVCW5NnuY09QVnth3MxDYPPABTRhZxoBSOgK4h5KGWIw="; ENC_CSRF=mtrB5PlvLKPBhHMWUNdnrL02uicaujcS; CO=US; LOCALE=en; MICRO_CONTENT_CSRF_TOKEN=f9DkSsGEUC5OkrJT7RPbUdecEwBFySl6; CSRF=L0eyOdCrNRRaIkxX4qRr9K7gMzoeuDNr; LOCALE=en; CO=US; indeed_rcc="LOCALE:LV:CTK:CO:RQ"; hpnode=1; PPID=eyJraWQiOiI5ZTkwNTFjZS1lNDUxLTQ2NmEtYWFkZC1jODE3ZDg4ZjIyYjYiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0YzM3MzI3MzY0MjRmYTIwIiwibGFzdF9hdXRoX3RpbWUiOjE3MDU0MTczMTY1ODksImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoIjoiZ29vZ2xlIiwiY3JlYXRlZCI6MTcwNDg1NTQ5NzAwMCwiaXNzIjoiaHR0cHM6XC9cL3NlY3VyZS5pbmRlZWQuY29tIiwibGFzdF9hdXRoX2xldmVsIjoiU1RST05HIiwibG9nX3RzIjoxNzA1NDE3MzE2NTg5LCJhdWQiOiJjMWFiOGYwNGYiLCJyZW1fbWUiOnRydWUsImV4cCI6MTcwNTQyMDkzMiwiaWF0IjoxNzA1NDE5MTMyLCJlbWFpbCI6ImhhcmluZWtvMDkyN0BnbWFpbC5jb20ifQ.6vtP0AV60XBRGCvCgHmN3TdgzA4dB-3u0apId3ZseVt9cFbnvydlIGlq_0IcsIj_YmX5l93s0mbE4JvAPjfDtA; RCLK=jk=6962ff22d345874c&tk=1hk9f1f30j5m9803&from=web&rd=VwIPTVJ1cTn5AN7Q-tSqGRXGNe2wB2UYx73qSczFnGU&qd=RnZhMybXSk4M3QtTVGXWoRamP4jh4XPbw3LNA8ctyAiVSaXBPADMDvY05rlBff_T5wYwWVlpB-P3rhI6v27_QQ&ts=1705419783264&sal=0; LV="LA=1705420433:LV=1705417195:CV=1705420433:TS=1705417195"; __cf_bm=QcOWBK5XVa0vWPytKr5rZ_nxOfWmh84.sRpEyNE0eB8-1705420434-1-AYkIrhVsWFzpsJGr+KQTFcEB3uzNA3fPzXNvLLaM+731B/qqNDvkI/4/UnKasrrQbGlXorrR6lzvNjTPQE7mAj8=; _gat=1; RQ="q=usa&l=&ts=1705420435902:q=us&l=&ts=1705419147442"; JSESSIONID=5EB5DBE0C5A1C3846B23BBD5B7EA90E2'

        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': user_agent, 'Cookie': cookie}, callback=self.parse)

    # レスポンスに対するパース処理
    def parse(self, response):
        for offer in response.css('.slider_item'):
            yield Offer(
                url = offer.css('.jcs-JobTitle').extract_first().strip()
            )
            return