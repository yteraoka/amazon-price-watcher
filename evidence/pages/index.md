---
title: Amazon Price Watcher
---

```sql categories
SELECT DISTINCT column1 AS category
  FROM local.items
```

<Dropdown
  data={categories}
  name=category
  value=category
/>

```sql items
SELECT column0 AS asin
     , column2 AS name
     , '/asin/' || column0 || '/' AS link
  FROM local.items
 WHERE column1 = '${inputs.category}'
 ORDER BY name
```

<DataTable data={items} search=true link=link openInNewTab=true rows=50>
  <Column id=asin />
  <Column id=name />
</DataTable>
