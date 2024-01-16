import requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import time

# フェッチする間隔(秒)
DOWNLOAD_DELAY = 3
# フェッチし始めるページ
START_PAGE = 0
# フェッチし終えるページ
END_PAGE = 1
# IndeedにアクセスしてRequest HeaderのCookieをコピペする
cookie = 'CTK=1hk9cifucj5le800; RF="TFTzyBUJoNr6YttPP3kyivpZ6-9J49o-Uk3iY6QNQqKE2fh7FyVgtZ_oS5kJHIG15wzdhT5eKkA="; INDEED_CSRF_TOKEN=F47fsYCbgwwLQPmh6yVj8oi7NfKieHSZ; _gcl_au=1.1.1177260853.1705417197; _ga=GA1.2.889599877.1705417197; _gid=GA1.2.697592064.1705417197; SURF=UoajWBY3mykZzbIUiic10iB3aquUmpKY; gonetap=1; SHARED_INDEED_CSRF_TOKEN=F47fsYCbgwwLQPmh6yVj8oi7NfKieHSZ; LC="co=JP"; _cfuvid=Y9B3MY_urilUJMdG5G6SfhPDLadryTN58oo6v50zVps-1705417298938-0-604800000; g_state={"i_l":0}; SOCK="ZpgM3-XixJsxSUwuLtQlA06KxlE="; SHOE="kqL7UHjQjvp5CClA32zkkW5VEX2usEjIIuxVrqyI2NPBnJ8uqC4Yom5mMC4BEocFq8rmL0Dv-vhvOiGnC49Nu28VqevYz8Byv3urk9K01z-LVCW5NnuY09QVnth3MxDYPPABTRhZxoBSOgK4h5KGWIw="; ENC_CSRF=mtrB5PlvLKPBhHMWUNdnrL02uicaujcS; CO=US; LOCALE=en; MICRO_CONTENT_CSRF_TOKEN=f9DkSsGEUC5OkrJT7RPbUdecEwBFySl6; CSRF=L0eyOdCrNRRaIkxX4qRr9K7gMzoeuDNr; LOCALE=en; CO=US; indeed_rcc="LOCALE:LV:CTK:CO:RQ"; hpnode=1; ROJC=a80d0326ed1aa105:a9e0c1a2a96ea8cd:e70742734ff93c90:963e2bdae5f274f3:b44b68ba82b4a85e:702081574bd9e77e:59365ed90bebbfb7:805262b92b93fd47:4100f66ddcfe3fc6:6962ff22d345874c; PPID=eyJraWQiOiI5ZTkwNTFjZS1lNDUxLTQ2NmEtYWFkZC1jODE3ZDg4ZjIyYjYiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0YzM3MzI3MzY0MjRmYTIwIiwibGFzdF9hdXRoX3RpbWUiOjE3MDU0MTczMTY1ODksImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoIjoiZ29vZ2xlIiwiY3JlYXRlZCI6MTcwNDg1NTQ5NzAwMCwiaXNzIjoiaHR0cHM6XC9cL3NlY3VyZS5pbmRlZWQuY29tIiwibGFzdF9hdXRoX2xldmVsIjoiU1RST05HIiwibG9nX3RzIjoxNzA1NDE3MzE2NTg5LCJhdWQiOiJjMWFiOGYwNGYiLCJyZW1fbWUiOnRydWUsImV4cCI6MTcwNTQzMDMwMCwiaWF0IjoxNzA1NDI4NTAwLCJlbWFpbCI6ImhhcmluZWtvMDkyN0BnbWFpbC5jb20ifQ.NIjUhk89BTEsfkHi5ljM3ihHimV05dRUpl8mpsdVWaLYQr0_xn7-RMjNHF9SKvNH1NnLaUYKBa-gPMyk0_FX7Q; __cf_bm=R.QRnAv8Vys3KYdJoAn.UvN5AQ4IX_Gro30s2CFDltY-1705428648-1-AT4QXY+9cJv6k/OdSsCndVEpst4Hhdblw48kJrBKTPC5Hm5NXxwgVOIzYZfyOb2RDM+y1qvVHPPgE6+1mmXeIjg=; _gat=1; LV="LA=1705428653:LV=1705423640:CV=1705428653:TS=1705417195"; RQ="q=usa&l=&ts=1705428653585&pts=1705425280579:q=us&l=&ts=1705419147442"; JSESSIONID=B7D1863BFC14D35CA5FB00F4C10057A8'
domain = "https://www.indeed.com"
dummy_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

class Offer():
    def __init__(self, url, job_name, salary, description):
        self.url = url
        self.job_name = job_name
        self.salary = salary
        self.description = description

    def __str__(self):
     return '(' + str(self.url) + ', ' + str(self.job_name) + ', ' + str(self.salary) + ', ' + str(self.description) + ')'

# 求人一覧ページから, 求人ページのURLを取得する
def fetch_offer_urls(page: int):
    url = domain + "/jobs?q=usa&vjk=0724fe195abde816&start=" + str(page * 10)
    res = requests.get(url, headers={"User-Agent": dummy_user_agent, "Cookie": cookie})
    soup = BeautifulSoup(res.text, 'html.parser')
    offer_urls = []
    for offer in soup.select('.jcs-JobTitle'):
        offer_urls.append(offer.get('href'))
    return offer_urls
    
def fetch_offer(offer_url: str):
    query_params = urllib.parse.parse_qs(offer_url)
    jk = query_params['/rc/clk?jk'][0]
    url = domain + "/viewjob?jk=" + jk
    res = requests.get(url, headers={"User-Agent": dummy_user_agent, "Cookie": cookie})
    soup = BeautifulSoup(res.text, 'html.parser')
    maybe_salary = soup.select_one('.css-2iqe2o')
    
    return Offer(
        url=url,
        job_name=soup.select_one('.jobsearch-JobInfoHeader-title').string,
        salary= maybe_salary.string if maybe_salary != None else "",
        description=soup.select_one('#jobDescriptionText').text
    )

def offer_to_df(offer: Offer):
    return pd.DataFrame({
        "url": [offer.url],
        'job_name': [offer.job_name],
        'salary': [offer.salary],
        'description': [offer.description.replace("\n", "")]
    })

for page in range(START_PAGE, END_PAGE):
    urls = fetch_offer_urls(page)
    for url in urls:
        offer = fetch_offer(url)
        print((offer.job_name, offer.salary))
        df = offer_to_df(offer)
        df.to_csv('offers.csv', mode='a', header=False)
        time.sleep(DOWNLOAD_DELAY)

# f = open('indeed.html', 'w', encoding='UTF-8') 
# f.write(html)
# f.close()