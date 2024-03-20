# {params.category}

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
       , prices.coupon
    FROM local.prices prices
         JOIN
         latest
         ON prices.timestamp = latest.timestamp
)
SELECT items.asin
     , latest_prices.price
     , items.name
     , '/asin/' || items.asin || '/' AS link
     , latest_prices.coupon
  FROM local.items items
       JOIN
       latest_prices
       ON items.asin = latest_prices.asin
 WHERE items.category = '${params.category}'
ORDER BY items.name
```

<DataTable data={items_with_price} search=true link=link rows=50>
  <Column id=asin />
  <Column id=price fmt=num0 />
  <Column id=coupon fmt=num0 />
  <Column id=name />
</DataTable>

---

## Categories

{@partial "categories.md"}
