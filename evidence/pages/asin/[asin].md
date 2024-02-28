# {params.asin}

```sql item
SELECT name
     , image_url
  FROM local.prices
 WHERE asin = '${params.asin}'
 ORDER BY timestamp DESC
 LIMIT 1
```

<a href="https://www.amazon.co.jp/dp/{params.asin}?tag=ytera-22&linkCode=ogi&th=1&psc=1" target="_blank" rel="noreferrer sponsored"><Value data={item} column=name row=0 /></a>


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

## <Value data={latest} fmt='JPY' column='price' /> (at <Value data={latest} column='timestamp' fmt='yyyy-mm-dd H:MM AM/PM' /> UTC)

<LineChart
  data={prices}
  x=timestamp
  y=price
  yFmt=JPY0
  step=false
  markers=true
  markerShape=circle
  markerSize=6
/>

<img src="{fmt(item[0].image_url)}" alt="item image">

---

```sql category
SELECT category
  FROM local.items
 WHERE asin = '${params.asin}'
 LIMIT 1
```

## <Value data={category} />

```sql items
SELECT asin
     , name
     , '/asin/' || asin || '/' AS link
  FROM local.items
 WHERE category = (SELECT category FROM local.items WHERE asin = '${params.asin}')
--   AND asin <> '${params.asin}'
 ORDER BY name
```

```sql items_with_price
WITH
latest AS (
  SELECT max(timestamp) AS timestamp
       , asin
    FROM local.prices
   GROUP BY asin
),
latest_prices AS (
  SELECT prices.asin
       , prices.name
       , prices.price
    FROM local.prices prices
         JOIN
         latest
         ON prices.timestamp = latest.timestamp
)
SELECT items.asin
     , latest_prices.price
     , items.name
     , '/asin/' || items.asin || '/' AS link
  FROM local.items items
       JOIN
       latest_prices
       ON items.asin = latest_prices.asin
 WHERE items.category = (SELECT category FROM local.items WHERE asin = '${params.asin}')
--   AND items.asin <> '${params.asin}'
ORDER BY items.name
```

<DataTable data={items_with_price} search=true link=link rows=50 emptySet=pass emptyMessage=Empty>
  <Column id=asin />
  <Column id=price fmt=num0 />
  <Column id=name />
</DataTable>

---

## Categories

{@partial "categories.md"}
