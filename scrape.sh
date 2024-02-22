#!/bin/bash

set -euo pipefail

echo '"asin","category","name"' > item-list.csv
cat evidence/sources/local/items.csv >> item-list.csv

output_file=$(date --utc +data/%Y/%m/%d/%Y%m%d-%H%M%S).json
install -d $(dirname ${output_file})

source bs/.venv/bin/activate

python bs/price.py item-list.csv | tee ${output_file}
