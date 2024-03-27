from playwright.sync_api import Playwright, sync_playwright, expect
import os
import re
import sys
import csv
import datetime
import json
from bs4 import BeautifulSoup
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
    coupon: int
    coupon_text: str


def find_coupon(bs):
    divs = bs.find_all('div')
    for div in divs:
        if div.get('data-csa-c-coupon'):
            coupon_text = div.text.strip()
            m = re.search(r' (202\d.*から.*まで)', coupon_text)
            if m is not None:
                coupon_text = m.group(1)
            labels = bs.find_all('label')
            for label in labels:
                if label.get('id') is not None:
                    if label.get('id').find('coupon') >= 0:
                        m = re.search(r'(\d+%?)\s*OFF', label.text)
                        if m is None:
                            return None, None
                        return m.group(1), coupon_text
    return None, None


def find_price(page):
    price = 0
    div = page.locator("#corePrice_feature_div")
    if div is not None:
        price = div.locator(".a-price-whole").inner_text()
        return price.replace(',', '')

def find_timesale(page):
    div = page.locator('#dealBadge_feature_div')
    return div.inner_text()


def save_html(asin, html):
    with open(f'work/{asin}.html', mode='w') as f:
        f.write(html)

def extract_price(asin, html):
    save_html(asin, html)
    bs = BeautifulSoup(html, features="html.parser")
    title_id = bs.find(id='title')
    if title_id is None:
        print('No title', file=sys.stderr)
        print(res.text, file=sys.stderr)
    title = title_id.text.strip()
    landing_image = bs.find('img', id='landingImage')
    if landing_image is not None:
        image_url = landing_image.attrs['src']
    else:
        unrolled_image = bs.find('div', id='unrolledImgNo0')
        if unrolled_image is not None:
            img = unrolled_image.find('img')
            if img is not None:
                image_url = img.attrs['src']
    div = bs.find(id="corePrice_feature_div")
    if div is None or div.find('span', class_='a-price-whole') is None:
        div = bs.find(id='corePriceDisplay_desktop_feature_div')
        if div is None:
            div = bs.find(id='tp_price_block_total_price_ww')
            if div is None:
                print('ERROR', file=sys.stderr)
                print('no tp_price_block_total_price_ww found', file=sys.stderr)
                return

    currency = 'JPY'
    price_span = div.find('span', class_='a-price-whole')
    if price_span is None:
        print(div, file=sys.stderr)

    price = div.find('span', class_='a-price-whole').text.replace(',', '')

    seller_a = bs.find('a', id='sellerProfileTriggerId')
    if seller_a is not None:
        seller = seller_a.text
    else:
        seller = ''

    coupon, coupon_text = find_coupon(bs)
    #print(f"coupon: {coupon}, {coupon_text}", file=sys.stderr)
    if coupon is not None:
        if coupon.find('%') >= 0:
            coupon = int(coupon.replace('%', ''))
            coupon = int(int(price) * coupon / 100)
        else:
            coupon = int(coupon)
    else:
        coupon = 0
    if coupon_text is None:
        coupon_text = ""

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
            seller,
            coupon,
            coupon_text
        )


def run(playwright: Playwright, asins):
    proxy = {}
    if os.environ.get('HTTP_PROXY', None) is not None:
        proxy['server'] = os.environ['HTTP_PROXY']
        if os.environ.get('PROXY_USERNAME', None) is not None:
            proxy['username'] = os.environ['PROXY_USERNAME']
        if os.environ.get('PROXY_PASSWORD', None) is not None:
            proxy['password'] = os.environ['PROXY_PASSWORD']
    else:
        proxy = None
    browser = playwright.chromium.launch(headless=True, proxy=proxy)
    #browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    context.set_default_timeout(120000)
    page = context.new_page()
    for asin in asins:
        url = 'https://www.amazon.co.jp/dp/' + asin + '/'
        print(url, file=sys.stderr)
        page.goto(url)
        page.wait_for_load_state()
        #print(json.dumps(asdict(extract_price(asin, page.content())), ensure_ascii=False))
        item = extract_price(asin, page.content())
        if item is not None:
            print(json.dumps(asdict(item), ensure_ascii=False))

def main():
    item_ids = []

    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['enabled'] == "true":
            #if row['asin'] == "B0CHVXW6FV":
            #if row['asin'] == "B0B6ZQJXW8":
                item_ids.append(row['asin'])

    #asins = ['B0CJFQ7RTX','B08P6ZSXWZ','B09HBCY5BF','B0BXSKY533','B0C5CBV6L3','B0C5CBV6L3']
    #item_ids = ['B0CJFQ7RTX']
    with sync_playwright() as playwright:
        run(playwright, item_ids)

main()

