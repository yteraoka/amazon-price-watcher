---
title: Amazon Price Watcher
---

```sql item_list
SELECT DISTINCT asin, name, '/asin/' || asin || '/' AS link
  FROM local.prices
 ORDER BY name
```

<DataTable data={item_list} search=true link=link openInNewTab=true rows=50>
  <Column id=asin />
  <Column id=name />
</DataTable>
