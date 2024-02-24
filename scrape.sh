#!/bin/bash

set -euo pipefail

output_file=$(date --utc +data/%Y/%m/%d/%Y%m%d-%H%M%S).json
install -d $(dirname ${output_file})

source bs/.venv/bin/activate

python bs/price.py evidence/sources/local/items.csv | tee ${output_file}
