SET SCHEMA 'vision_data';
CREATE OR REPLACE PROCEDURE test_sp(OUT result text)
LANGUAGE plpgsql
AS $$
BEGIN
  result := 'test works';
END;
$$;
