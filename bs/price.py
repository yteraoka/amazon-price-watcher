import csv
import datetime
import json
import requests
import sys
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from urllib.parse import quote, urlparse
from dataclasses import dataclass, asdict

@dataclass
class Item:
    timestamp: str
    asin: str
    name: str
    price: int
    currency: str
    image_url: str
    merchant_name: str

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
headers = {
    'User-Agent': user_agent
}

s = requests.Session()
retries = Retry(total=5, status_forcelist=[429, 500, 502, 503, 504], status=3, connect=3, read=2, backoff_factor=1)
s.mount('https://', HTTPAdapter(max_retries=retries))

def getItem(asin):
    url = 'https://www.amazon.co.jp/dp/{}'.format(asin)
    print(url, file=sys.stderr)
    res = s.get(url, headers=headers, timeout=(5.0, 10.0))
    if res.status_code != 200:
        raise Exception("Unexpected status code {}, url {}".format(res.status_code, url))
    bs = BeautifulSoup(res.text, features="html.parser")
    title_id = bs.find(id='title')
    if title_id is None:
        print('No title', file=sys.stderr)
        print(res.text, file=sys.stderr)
    title = title_id.text.strip()
    image_url = bs.find('img', id='landingImage').attrs['src']
    div = bs.find(id="corePrice_feature_div")
    if div is None or div.find('span', class_='a-price-whole') is None:
        div = bs.find(id='corePriceDisplay_desktop_feature_div')
        if div is None:
            div = bs.find(id='tp_price_block_total_price_ww')
            if div is None:
                print('ERROR', file=sys.stderr)
                print('no tp_price_block_total_price_ww found', file=sys.stderr)

    currency = 'JPY'
    #currency_span = div.find('span', class_='a-price-symbol')
    #if currency_span is not None:
    #    if currency_span.text == '￥':
    #        currency = 'JPY'
    #    else:
    #        print('unknown currency {}'.format(currency_span.text), file=sys.stderr)
    #else:
    #    print('no a-price-symbol', file=sys.stderr)
    #    currency = 'JPY'

    price_span = div.find('span', class_='a-price-whole')
    if price_span is None:
        print(div, file=sys.stderr)

    price = div.find('span', class_='a-price-whole').text.replace(',', '')

    seller_a = bs.find('a', id='sellerProfileTriggerId')
    if seller_a is not None:
        seller = seller_a.text
    else:
        seller = ''

    if seller == '':
        div = bs.find('div', class_='offer-display-feature-text', attrs={'offer-display-feature-name': 'desktop-merchant-info'})
        if div is not None:
            seller = div.text.strip()

    return Item(
            datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            asin,
            title,
            int(price),
            currency,
            image_url,
            seller
        )

def main():
    item_ids = []

    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_ids.append(row['asin'])

    for asin in item_ids:
        item = getItem(asin)
        print(json.dumps(asdict(item), ensure_ascii=False))

main()
