CREATE OR REPLACE PROCEDURE CreateFutureDataTables()
LANGUAGE plpgsql
AS $$
DECLARE
    today DATE := CURRENT_DATE;
    advanceCount INT := 3; -- How often you want a new table to be produced
    iteration INT := 1;
    tableName VARCHAR;
    query VARCHAR;
BEGIN
    LOOP
        EXIT WHEN iteration > advanceCount;
        tableName := 'Data_' || to_char(today + INTERVAL '1 month' * iteration, 'YYYY_MM');
        --query := 'CREATE TABLE IF NOT EXISTS ' || tableName || ''; need to fill table structure in 
        --EXECUTE query;
        iteration := iteration + 1;
    END LOOP;
END;
$$;