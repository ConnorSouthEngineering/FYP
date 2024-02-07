SET SCHEMA 'vision_data';

CREATE OR REPLACE FUNCTION INSERT_REPORTS(
    _report_name VARCHAR,
    _deployment_id INT,
    _frequency_value DECIMAL,
    _frequency_unit FREQUENCY_UNIT,
    _creation_date DATE,
    _last_gen DATE,
    _graph_id INT
)
RETURNS INT AS $$
DECLARE
    new_report_id INT;
BEGIN
    SET SCHEMA 'vision_data';
    INSERT INTO Reports(report_name, deployment_id, frequency_value, frequency_unit, creation_date, last_gen, graph_id)
    VALUES (_report_name, _deployment_id, _frequency_value, _frequency_unit, _creation_date, _last_gen, _graph_id)
    RETURNING report_id INTO new_report_id;
    
    RETURN new_report_id;
END;
$$ LANGUAGE plpgsql;

