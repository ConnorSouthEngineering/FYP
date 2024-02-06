CREATE FUNCTION get_graph_data(start_date VARCHAR, end_date VARCHAR, classes JSON, deployment_id INT)
RETURNS graph_data JSON

SELECT creation_date, result 
FROM vision_data.data_totalentry
WHERE class_id = '1' AND deployment_id = '2' AND creation_date BETWEEN start_date AND end_date;