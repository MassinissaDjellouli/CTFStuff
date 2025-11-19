[BACK](../README.md)

https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection
## Find db type:

| DB Type    | Command |
|------------|------------------|
| SQLite     | SELECT sqlite_version() |
| MySQL      | SELECT VERSION() |
| PostgreSQL | SELECT version() |
| MSSQL      | SELECT @@version |
| Oracle     | SELECT banner FROM v$version |

## Print tables:

| DB Type    | Command |
|------------|------------------|
| SQLite     | SELECT name FROM my_db.sqlite_master WHERE type='table' |
| MySQL      | SELECT table_name FROM information_schema.tables WHERE table_schema = 'my_db' |
| PostgreSQL | SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' |
| MSSQL      | SELECT name FROM sysobjects WHERE xtype = 'U' |
| Oracle     | SELECT table_name FROM user_tables |

## Print columns:
| DB Type    | Command |
|------------|------------------|
| SQLite     | SELECT name from pragma_table_info('my_table') |
| MySQL      | SELECT column_name FROM information_schema.columns WHERE table_name = 'my_table' |
| PostgreSQL | SELECT column_name FROM information_schema.columns WHERE table_name = 'my_table' |
| MSSQL      | SELECT name FROM syscolumns WHERE id = object_id('my_table') |
| Oracle     | SELECT column_name FROM user_tab_columns WHERE table_name = 'my_table' |

## Concatenate rows
| DB Type    | Command |
|------------|------------------|
| SQLite     | SELECT group_concat(column_name) FROM my_table |
| MySQL      | SELECT group_concat(column_name) FROM my_table |
| PostgreSQL | SELECT string_agg(column_name, ',') FROM my_table |
| MSSQL      | SELECT STRING_AGG(column_name, ',') FROM my_table |
| Oracle     | SELECT LISTAGG(column_name, ',') FROM my_table |


SELECT group_concat(name) from pragma_table_info('users') --