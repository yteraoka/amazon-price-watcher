# {params.category}

```sql items
SELECT asin
     , name
     , '/asin/' || asin || '/' AS link
  FROM local.items
 WHERE category = '${params.category}'
 ORDER BY name
```

<DataTable data={items} search=true link=link rows=50>
  <Column id=asin />
  <Column id=name />
</DataTable>

---

## Categories

{@partial "categories.md"}
