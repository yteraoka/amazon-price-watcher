# {params.asin}

```sql item_name
SELECT name
  FROM local.prices
 WHERE asin = '${params.asin}'
 LIMIT 1
```

[<Value data={item_name} column=name row=0 />](https://www.amazon.co.jp/dp/{params.asin}/)

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
