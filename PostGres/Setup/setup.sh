##Ensure quit on error
set -e
##Execute schema setup
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/Scripts/VD_schema_creations.sql
##Execute table setup
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/Scripts/VD_table_creations.sql
