# {params.category}

```sql items
SELECT column0 AS asin
     , column2 AS name
     , '/asin/' || column0 || '/' AS link
  FROM local.items
 WHERE column1 = '${params.category}'
 ORDER BY name
```

<DataTable data={items} search=true link=link rows=50>
  <Column id=asin />
  <Column id=name />
</DataTable>
