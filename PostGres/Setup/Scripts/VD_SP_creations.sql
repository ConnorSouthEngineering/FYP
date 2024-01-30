SET SCHEMA 'vision_data';
CREATE OR REPLACE PROCEDURE create_data_partition()
LANGUAGE plpgsql
AS $$
DECLARE
    next_partition_start DATE;
    next_partition_end DATE;
    partition_name TEXT;
BEGIN   
    next_partition_start := (DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month')::DATE;
    next_partition_end := (DATE_TRUNC('month', next_partition_start) + INTERVAL '1 month')::DATE;
    partition_name := 'data_totalentry_' || TO_CHAR(next_partition_start, 'MMYYYY');
    IF NOT EXISTS(SELECT FROM pg_class WHERE relname = partition_name) THEN
        EXECUTE FORMAT('CREATE TABLE %I PARTITION OF Data_TotalEntry FOR VALUES FROM (%L) TO (%L)', partition_name, next_partition_start, next_partition_end);
    END IF;
    ALTER TABLE partition_name ADD PRIMARY KEY (entry_num, creation_date);
    ALTER TABLE partition_name ADD CONSTRAINT deployment_key
    FOREIGN KEY (deployment_id) REFERENCES Deployments(deployment_id);
END;
$$;
SELECT cron.schedule('create_data_partitions','0 0 2,20 * *');