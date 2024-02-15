SET SCHEMA 'vision_data';
CREATE OR REPLACE FUNCTION INSERT_MODELS(
    _model_name VARCHAR,
    _creation_date DATE
)
RETURNS INT AS $$
DECLARE
    new_model_id INT;
BEGIN
    SET SCHEMA 'vision_data';
    INSERT INTO models(model_name, creation_date)
    VALUES (_model_name, _creation_date)
    RETURNING model_id INTO new_model_id;
    
    RETURN new_model_id;
END;
$$ LANGUAGE plpgsql;