//*
COPY Targets FROM '/docker-entrypoint-initdb.d/DataLoading/Targets.csv' DELIMITER ',' CSV HEADER;
COPY Deployments FROM '/docker-entrypoint-initdb.d/DataLoading/Deployments.csv' DELIMITER ',' CSV HEADER;
COPY GraphMap FROM '/docker-entrypoint-initdb.d/DataLoading/GraphMap.csv' DELIMITER ',' CSV HEADER;
COPY Reports FROM '/docker-entrypoint-initdb.d/DataLoading/Reports.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY ReportClasses FROM '/docker-entrypoint-initdb.d/DataLoading/ReportClasses.csv' DELIMITER ',' CSV HEADER;
COPY DataTotalEntry FROM '/docker-entrypoint-initdb.d/DataLoading/DataTotalEntry.csv' DELIMITER ',' CSV HEADER;
COPY Deployments FROM '/docker-entrypoint-initdb.d/DataLoading/Deployments.csv' DELIMITER ',' CSV HEADER;
COPY GraphMap FROM '/docker-entrypoint-initdb.d/DataLoading/GraphMap.csv' DELIMITER ',' CSV HEADER;
COPY Reports FROM '/docker-entrypoint-initdb.d/DataLoading/Reports.csv' DELIMITER ',' CSV HEADER NULL 'NULL';
COPY ReportClasses FROM '/docker-entrypoint-initdb.d/DataLoading/ReportClasses.csv' DELIMITER ',' CSV HEADER;
COPY DataTotalEntry FROM '/docker-entrypoint-initdb.d/DataLoading/DataTotalEntry.csv' DELIMITER ',' CSV HEADER;