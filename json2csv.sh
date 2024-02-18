#!/bin/bash

csv_file=evidence/sources/local/prices.csv

echo '"timestamp","asin","name","price","savings","lowest","highest","url","image_url"' > ${csv_file}

find data/ -type f \
  | xargs cat \
  | jq '[.timestamp, .asin, .name, .price, .savings_amount, .lowest_price, .highest_price, .url, .image_url_large] | @csv' -r \
  >> ${csv_file}

