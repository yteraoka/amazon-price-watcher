import json
import os
import requests
import sys
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from urllib.parse import quote, urlparse

s = requests.Session()
retries = Retry(
    total=5,
    status_forcelist=[429, 500, 502, 503, 504],
    status=3,
    connect=3,
    read=2,
    backoff_factor=1,
    allowed_methods=['POST']
)
s.mount('https://', HTTPAdapter(max_retries=retries))

def read_file(path):
    data = {}
    with open(path) as f:
        for line in f:
            obj = json.loads(line)
            data[obj['asin']] = obj
    return data


def compare(latest, previous):
    coupon = 0
    if 'coupon' in latest:
        latest['price'] = latest['price'] - latest['coupon']
        coupon = latest['coupon']

    if 'coupon' in previous:
        previous['price'] = previous['price'] - previous['coupon']

    if latest['price'] < previous['price']:
        diff = previous['price'] - latest['price']
        percent = diff / previous['price']
        # 値下がり
        send_message(latest['asin'],
                     latest['name'],
                     latest['price'],
                     previous['price'],
                     f"{percent:.2%} 値下がりしました",
                     coupon)
    elif latest['price'] > previous['price']:
        # 値上がり
        diff = latest['price'] - previous['price']
        percent = diff / previous['price']
        send_message(latest['asin'],
                     latest['name'],
                     latest['price'],
                     previous['price'],
                     f"{percent:.2%} 値上がりしました",
                     coupon)

def send_message(asin, item_name, latest_price, previous_price, title, coupon):
    body = {}
    msg = {}
    diff = latest_price - previous_price
    if diff > 0:
        diff_str = f"+{diff:,}"
    else:
        diff_str = f"{diff:,}"
    msg['title'] = title
    msg['text'] = item_name
    msg['fields'] = []
    msg['author_name'] = "Amazon Price Watcher"
    msg['fields'].append({"title": "価格変動", "value": diff_str, "short": False})
    msg['fields'].append({"title": "最新価格", "value": f"{latest_price:,}", "short": True})
    msg['fields'].append({"title": "前回の価格", "value": f"{previous_price:,}", "short": True})
    if coupon > 0:
        msg['fields'].append({"title": "クーポン", "value": f"{coupon:,}", "short": True})
    msg['fields'].append({"title": "商品URL", "value": 'https://www.amazon.co.jp/dp/' + asin, "short": False})
    msg['fields'].append({"title": "Evidence URL", "value": 'https://price-watcher.teraoka.me/asin/' + asin + '/', "short": False})
    body["attachments"] = [msg]
    print(body)
    res = s.post(os.environ['SLACK_WEBHOOK_URL'], headers={'Content-Type': 'application/json'}, data=json.dumps(body), timeout=(5.0, 10.0))
    print(res.status_code)

def main():
    previous = read_file(sys.argv[1])
    latest = read_file(sys.argv[2])

    for asin in latest:
        if asin in previous:
            compare(latest[asin], previous[asin])

main()
