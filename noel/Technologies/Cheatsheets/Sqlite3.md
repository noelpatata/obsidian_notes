# SQLite Unknown Database Cheatsheet

## Is it actually SQLite?

```bash
file database.db
xxd database.db | head -1
# Should start with: 53514c69 74652066 ("SQLite f")
```

```sql
PRAGMA integrity_check;
```

## Database metadata

```sql
PRAGMA database_list;
PRAGMA journal_mode;
PRAGMA page_count;
PRAGMA page_size;
PRAGMA encoding;
```

## Find all objects

```sql
-- Everything: tables, views, indexes, triggers
SELECT type, name, tbl_name FROM sqlite_master;

-- Tables only
SELECT name FROM sqlite_master WHERE type = 'table';

-- Views only
SELECT name FROM sqlite_master WHERE type = 'view';

-- Hidden/internal tables
SELECT name FROM sqlite_master WHERE name LIKE 'sqlite_%';
```

## Explore table structure

```sql
-- Full CREATE statement
SELECT sql FROM sqlite_master WHERE name = 'table_name';

-- Column details
PRAGMA table_info(table_name);

-- All columns across all tables
SELECT m.name AS tbl, p.name AS col, p.type
FROM sqlite_master m
JOIN pragma_table_info(m.name) p
WHERE m.type = 'table';
```

## Peek at data

```sql
SELECT * FROM table_name LIMIT 10;
SELECT COUNT(*) FROM table_name;
```

## Row counts for all tables

```sql
-- Generate count queries
SELECT 'SELECT ''' || name || ''' AS tbl, COUNT(*) AS rows FROM ' || name || ' UNION ALL'
FROM sqlite_master WHERE type = 'table';
```

## Indexes and foreign keys

```sql
-- All indexes
SELECT name, tbl_name, sql FROM sqlite_master WHERE type = 'index';

-- Foreign keys for a table
PRAGMA foreign_key_list(table_name);

-- Index info
PRAGMA index_list(table_name);
PRAGMA index_info(index_name);
```

## If sqlite_master is empty

The database might be:

- **Encrypted** (SQLCipher) — needs a key to open
- **Corrupted** — try `PRAGMA integrity_check;`
- **Not SQLite** — verify with `file` and `xxd`
- **WAL mode with uncommitted data** — check for `.db-wal` and `.db-shm` files alongside the db