# {params.asin}

```sql item
SELECT name
     , url
     , image_url
  FROM local.prices
 WHERE asin = '${params.asin}'
 ORDER BY timestamp DESC
 LIMIT 1
```

[<Value data={item} column=name row=0 />](https://www.amazon.co.jp/dp/{params.asin}?tag=ytera-22&linkCode=ogi&th=1&psc=1)

```sql prices
SELECT timestamp
     , price
  FROM local.prices
 WHERE asin = '${params.asin}'
 ORDER BY timestamp
```

```sql lowest_price
SELECT MIN(lowest) AS price
  FROM local.prices
 WHERE asin = '${params.asin}'
```

```sql highest_price
SELECT MAX(highest) AS price
  FROM local.prices
 WHERE asin = '${params.asin}'
```

<LineChart data={prices} x=timestamp y=price yFmt=JPY0>
  <ReferenceLine data={lowest_price} y=price color=blue label="Lowest" />
  <ReferenceLine data={highest_price} y=price color=red label="Highest" />
</LineChart>
