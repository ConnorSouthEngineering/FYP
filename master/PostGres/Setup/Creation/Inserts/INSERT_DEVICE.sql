SET SCHEMA 'vision_data';

CREATE OR REPLACE FUNCTION INSERT_DEVICE(_device_name VARCHAR, _creation_date DATE)
RETURNS INT AS $$
DECLARE
    resolved_device_id INT;
BEGIN
    SET SCHEMA 'vision_data';

    SELECT device_id INTO resolved_device_id FROM devices WHERE device_name = _device_name;

    IF FOUND THEN
        RETURN resolved_device_id;
    END IF;

    INSERT INTO devices(device_name, creation_date)
    VALUES (_device_name, _creation_date)
    RETURNING device_id INTO resolved_device_id;
    
    RETURN resolved_device_id;
END;
$$ LANGUAGE plpgsql;
