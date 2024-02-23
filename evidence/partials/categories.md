```sql categories
SELECT DISTINCT category AS category
     , '/category/' || category || '/' AS link
  FROM local.items
```

<DataTable data={categories} link=link rows=50>
  <Column id=category />
</DataTable>
