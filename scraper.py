import requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import time

# フェッチする間隔(秒)
DOWNLOAD_DELAY = 2
# フェッチし始めるページ
START_PAGE = 99
# フェッチし終えるページ
END_PAGE = 10000
CSV = 'offers.csv'
# https://www.indeed.com/q-usa-jobs.html にアクセスして, 開発者ツールのNetworkから Request HeaderのCookieをコピペする
cookie = 'CTK=1hk9cifucj5le800; RF="TFTzyBUJoNr6YttPP3kyivpZ6-9J49o-Uk3iY6QNQqKE2fh7FyVgtZ_oS5kJHIG15wzdhT5eKkA="; _gcl_au=1.1.1177260853.1705417197; _ga=GA1.2.889599877.1705417197; _gid=GA1.2.697592064.1705417197; gonetap=1; LC="co=JP"; g_state={"i_l":0}; SOCK="ZpgM3-XixJsxSUwuLtQlA06KxlE="; SHOE="kqL7UHjQjvp5CClA32zkkW5VEX2usEjIIuxVrqyI2NPBnJ8uqC4Yom5mMC4BEocFq8rmL0Dv-vhvOiGnC49Nu28VqevYz8Byv3urk9K01z-LVCW5NnuY09QVnth3MxDYPPABTRhZxoBSOgK4h5KGWIw="; CO=US; LOCALE=en; LOCALE=en; CO=US; indeed_rcc="LOCALE:LV:CTK:CO:RQ"; hpnode=1; INDEED_CSRF_TOKEN=P5ixlkSLo0DQplTANNNFtNwV7TBD6U4u; SHARED_INDEED_CSRF_TOKEN=FlymSnovi0G2372dtOm2fpcWNo8TIyw1; _cfuvid=ro1aW0wsrxaiyHmSB0Peq3BDahSvtynXDPeWmgOi0cE-1705430379856-0-604800000; ENC_CSRF=fw5fXFelrWF0erOzzOOfr32ZKzlexgAK; MICRO_CONTENT_CSRF_TOKEN=JoKrQSckdrcJQ4yBxRMmIbRbiFkxgfGH; ROJC=805262b92b93fd47:a80d0326ed1aa105:a9e0c1a2a96ea8cd:e70742734ff93c90:963e2bdae5f274f3:b44b68ba82b4a85e:702081574bd9e77e:59365ed90bebbfb7:4100f66ddcfe3fc6:6962ff22d345874c; RCLK=jk=4100f66ddcfe3fc6&tk=1hkaadolnm8q6800&from=web&rd=VwIPTVJ1cTn5AN7Q-tSqGRXGNe2wB2UYx73qSczFnGU&qd=RnZhMybXSk4M3QtTVGXWockrjDKDT-GtKl1oFxXP-J3LGKXOSIyPdeGVunb77-PKmT2Ed1S7UDq8pegV_mUPVg&ts=1705448497847&sal=1; __cf_bm=Yfyj7Z0XPI6jXOe6Cujyi_Atw43JTnk6VG_0_0_G9M8-1705452432-1-AekC+0C3gx5E7xy9Sp2/3xRWnrQL6VFNmekAmVpw/La4YMs1nx16JU59v+RY6dL50qSSyyzqsYXl3ly1cgU7Zis=; PPID=eyJraWQiOiI5ZTkwNTFjZS1lNDUxLTQ2NmEtYWFkZC1jODE3ZDg4ZjIyYjYiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiI0YzM3MzI3MzY0MjRmYTIwIiwibGFzdF9hdXRoX3RpbWUiOjE3MDU0MTczMTY1ODksImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdXRoIjoiZ29vZ2xlIiwiY3JlYXRlZCI6MTcwNDg1NTQ5NzAwMCwiaXNzIjoiaHR0cHM6XC9cL3NlY3VyZS5pbmRlZWQuY29tIiwibGFzdF9hdXRoX2xldmVsIjoiU1RST05HIiwibG9nX3RzIjoxNzA1NDE3MzE2NTg5LCJhdWQiOiJjMWFiOGYwNGYiLCJyZW1fbWUiOnRydWUsImV4cCI6MTcwNTQ1NDIzMiwiaWF0IjoxNzA1NDUyNDMyLCJlbWFpbCI6ImhhcmluZWtvMDkyN0BnbWFpbC5jb20ifQ.rmvWKjKjKCD7FnhMvgR7YhW41OfKkyrdK3KSx3PpIbRQ6i0BYved7VJwcxkm4_P-7Pa2G46USdyHxAnC5lzZqg; LV="LA=1705452898:LV=1705448497:CV=1705452898:TS=1705417195"; RQ="q=usa&l=&ts=1705452898329&pts=1705448505953:q=us&l=&ts=1705419147442"; _gat=1; JSESSIONID=C6150E06D41B6DE3DAA2BCFCD16993C3'
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

def offer_to_df(offer: Offer, index: int):
    return pd.DataFrame({
        "i": [index],
        "url": [offer.url],
        'job_name': [offer.job_name],
        'salary': [offer.salary],
        'description': [offer.description.replace("\n", " ")]
    })

index = pd.read_csv(CSV).index.stop

for page in range(START_PAGE, END_PAGE):
    urls = fetch_offer_urls(page)
    for url in urls:
        offer = fetch_offer(url)
        print((offer.job_name, offer.salary))
        index += 1
        df = offer_to_df(offer, index)
        df.to_csv(CSV, mode='a', header=False, index=False)
        time.sleep(DOWNLOAD_DELAY)

# f = open('indeed.html', 'w', encoding='UTF-8') 
# f.write(html)
# f.close()