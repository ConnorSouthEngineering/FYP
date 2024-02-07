SET SCHEMA 'vision_data';

CREATE OR REPLACE FUNCTION INSERT_DEPLOYMENTS(
    _deployment_name VARCHAR,
    _target_id INT,
    _status_value VARCHAR,
    _model_id INT,
    _creation_date DATE,
    _start_date DATE,
    _expiry_date DATE
)
RETURNS INT AS $$
DECLARE
    new_deployment_id INT;
BEGIN
    SET SCHEMA 'vision_data';
    INSERT INTO Deployments(deployment_name, target_id, status_value, model_id, creation_date, start_date, expiry_date)
    VALUES (_deployment_name, _target_id, _status_value, _model_id, _creation_date, _start_date, _expiry_date)
    RETURNING deployment_id INTO new_deployment_id;
    
    RETURN new_deployment_id;
END;
$$ LANGUAGE plpgsql;

