##Ensure quit on error
set -e
##Add cron entries to psql configuration file
echo "shared_preload_libraries = 'pg_cron'" >> /var/lib/postgresql/data/postgresql.conf
echo "cron.database_name = '"$POSTGRES_DB"'" >> /var/lib/postgresql/data/postgresql.conf
##Restart psql
pg_ctl restart
##Execute schema setup
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/Creation/VD_schema_creation.sql
##Execute table setup
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/Creation/VD_table_creation.sql
##Execute pg_cron setup
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v postgres_user="$POSTGRES_USER" -f /docker-entrypoint-initdb.d/Creation/pg_cron_creation.sql
##Execute pg_cron setup
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v postgres_user="$POSTGRES_USER" -f /docker-entrypoint-initdb.d/Creation/VD_SP_creation.sql