SET SCHEMA 'vision_data';
CREATE OR REPLACE PROCEDURE test_sp()
LANGUAGE plpgsql
AS $$
BEGIN
  SET SCHEMA 'vision_data';
  CREATE TABLE IF NOT EXISTS test_db (
    id SERIAL PRIMARY KEY,
    example_column TEXT NOT NULL
  );
END;
$$;
