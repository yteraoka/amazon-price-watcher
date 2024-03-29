import csv
import datetime
import json
import os
import sys
import time
from amazon_paapi import AmazonApi
from dataclasses import dataclass, asdict

@dataclass
class AmazonItem:
    """Amazon Item"""
    timestamp: str
    asin: str
    name: str
    merchant_name: str
    currency: str
    price: float
    savings_amount: float
    highest_price: float
    lowest_price: float
    url: str
    image_url_large: str
    image_url_medium: str

amazon = AmazonApi(os.environ['KEY'], os.environ['SECRET'], os.environ['TAG'], os.environ['COUNTRY'], throttling=5)

#item_ids = ['B08P6ZSXWZ']

def main():
    item_ids = []
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_ids.append(row['asin'])

    n = len(item_ids)
    i = 0
    while i < n:
        items = amazon.get_items(item_ids[i:i+10])
        for item in items:
            i = AmazonItem(
                datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                item.asin,
                item.item_info.title.display_value,
                item.offers.listings[0].merchant_info.name,
                item.offers.listings[0].price.currency,
                item.offers.listings[0].price.amount,
                item.offers.listings[0].price.savings.amount if item.offers.listings[0].price.savings is not None else 0.0,
                item.offers.summaries[0].highest_price.amount,
                item.offers.summaries[0].lowest_price.amount,
                item.detail_page_url,
                item.images.primary.large.url,
                item.images.primary.medium.url
                )
            print(json.dumps(asdict(i), ensure_ascii=False))
        i = i + 10
        time.sleep(10)

main()
