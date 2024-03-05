SET SCHEMA 'vision_data';
CREATE OR REPLACE FUNCTION GET_REPORT_DATA(
    _start_date VARCHAR, 
    _end_date VARCHAR, 
    _class_ids JSON, 
    _deployment_id INT,
    _metric_value VARCHAR DEFAULT NULL 
)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    result_json JSON;
BEGIN
    SET SCHEMA 'vision_data';
    SELECT json_agg(json_build_object(
        'classid', class_id,
        'creation_dates', creation_dates,
        'values', results,
        'metric', _metric_value 
    )) INTO result_json
    FROM (
        SELECT 
            class_id,
            array_agg(creation_date ORDER BY creation_date) AS creation_dates,
            array_agg(result ORDER BY creation_date) AS results
        FROM vision_data.datatotalentry
        WHERE deployment_id = _deployment_id
        AND creation_date BETWEEN _start_date::DATE AND _end_date::DATE
        AND class_id = ANY ((SELECT array_agg(value::int) FROM json_array_elements_text(_class_ids))::int[])
        AND (_metric_value IS NOT NULL AND unit = _metric_value OR _metric_value IS NULL)
        GROUP BY class_id
    ) AS subquery;

    RETURN result_json;
END;
$$;
