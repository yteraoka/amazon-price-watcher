---
title: Amazon Price Watcher
---

```sql categories
SELECT DISTINCT column1 AS category
     , '/category/' || column1 || '/' AS link
  FROM local.items
```

<DataTable data={categories} link=link rows=50>
  <Column id=category />
</DataTable>
