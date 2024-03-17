#!/bin/bash

csv_file=evidence/sources/local/prices.csv

echo '"timestamp","asin","name","price","image_url","coupon","coupon_text"' > ${csv_file}

find data/ -type f \
  | xargs cat \
  | jq '[.timestamp, .asin, .name, .price, .image_url, .coupon, .coupon_text] | @csv' -r \
  >> ${csv_file}

