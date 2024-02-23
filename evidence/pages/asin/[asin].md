# {params.asin}

```sql item
SELECT name
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

```sql latest
SELECT timestamp
     , price
  FROM local.prices
 WHERE asin = '${params.asin}'
 ORDER BY timestamp DESC
  LIMIT 1
```

<Value data={latest} fmt='JPY' column='price' /> (at <Value data={latest} column='timestamp' fmt='yyyy-mm-dd H:MM AM/PM' />)

<LineChart
  data={prices}
  x=timestamp
  y=price
  yFmt=JPY0
  step=true
/>

<img src="{fmt(item[0].image_url)}" alt="item image">

---

```sql items
SELECT column0 AS asin
     , column2 AS name
     , '/asin/' || column0 || '/' AS link
  FROM local.items
 WHERE column1 = (SELECT column1 FROM local.items WHERE column0 = '${params.asin}')
--   AND column0 <> '${params.asin}'
 ORDER BY column2
```

<DataTable data={items} rows=all link=link />
