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
     , lowest
     , highest
  FROM local.prices
 WHERE asin = '${params.asin}'
 ORDER BY timestamp
```

<BigValue
  data={prices}
  value='price'
  sparkline='date'
  fmt='JPY'
/>

<LineChart
  data={prices}
  x=timestamp
  y={["price","lowest","highest"]}
  yFmt=JPY0
  step=true
/>

lowest には中古の価格も含まれることがある

<img src="{fmt(item[0].image_url)}">
