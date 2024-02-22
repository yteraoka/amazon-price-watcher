#!/bin/bash

csv_file=evidence/sources/local/prices.csv

echo '"timestamp","asin","name","price","image_url"' > ${csv_file}

find data/ -type f \
  | xargs cat \
  | jq '[.timestamp, .asin, .name, .price, .image_url] | @csv' -r \
  >> ${csv_file}

