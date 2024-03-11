CREATE OR REPLACE FUNCTION UPDATE_NODE_DEVICE_MAP(_node_id INT, _device_ids_json JSON)
RETURNS VOID AS $$
DECLARE
    _device_id BIGINT;
BEGIN
    FOR _device_id IN SELECT value::INT
                      FROM json_array_elements_text(_device_ids_json) AS value
    LOOP
        UPDATE nodedevice
        SET status_value = 'Connected'
        WHERE node_id = _node_id AND device_id = _device_id AND status_value <> 'Connected';

        IF NOT FOUND THEN
            INSERT INTO nodedevice(node_id, device_id, status_value)
            VALUES (_node_id, _device_id, 'Connected')
            ON CONFLICT (node_id, device_id) DO NOTHING;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
