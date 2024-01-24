SET SCHEMA 'vision_data';

BEGIN;
CREATE TABLE Targets(
    target_id INT PRIMARY KEY NOT NULL,
    target_name VARCHAR NOT NULL,
    alt_name VARCHAR,
    creation_date DATE NOT NULL,
    status_value VARCHAR NOT NULL,
    access VARCHAR,
    dob DATE, 
    age INT,
    role VARCHAR
);

CREATE TABLE Sources(
    source_id INT PRIMARY KEY NOT NULL,
    source_name VARCHAR,
    company_name VARCHAR,
    vers VARCHAR,
    install_date DATE,
    licensing VARCHAR, 
    license_expiry_date DATE
);

CREATE TABLE Source_lists(
    source_list_id INT PRIMARY KEY NOT NULL,
    source_id INT REFERENCES Sources(source_id) NOT NULL
);

CREATE TABLE Classes(
    class_id INT PRIMARY KEY NOT NULL,
    class_name VARCHAR NOT NULL,
    loc VARCHAR NOT NULL,
    data_count INT NOT NULL,
    source_list_id INT REFERENCES Source_lists(source_list_id) NOT NULL
);

CREATE TABLE Class_lists(
    class_list_id INT PRIMARY KEY NOT NULL,
    class_id INT REFERENCES Classes(class_id)
);

CREATE TABLE Categories(
    category_id INT PRIMARY KEY NOT NULL,
    category_name VARCHAR,
    class_list_id INT REFERENCES Class_lists(class_list_id) NOT NULL
);

CREATE TABLE Models(
    model_id INT PRIMARY KEY NOT NULL,
    model_name VARCHAR NOT NULL,
    creation_date DATE NOT NULL,
    class_list_id INT REFERENCES Class_lists(class_list_id) NOT NULL
);

CREATE TABLE Deployments(
    deployment_id INT PRIMARY KEY NOT NULL,
    deployment_name VARCHAR NOT NULL,
    target_id INT REFERENCES Targets(target_id) NOT NULL,
    status_value VARCHAR NOT NULL,
    model_id INT REFERENCES Models(model_id) NOT NULL,
    creation_date DATE NOT NULL,
    start_date DATE NOT NULL,
    expiry_date DATE NOT NULL
);

CREATE TABLE Frequency_Map(
    frequency_id INT PRIMARY KEY NOT NULL,
    frequency_type VARCHAR NOT NULL
);

CREATE TABLE Graph_Map(
    graph_id INT PRIMARY KEY NOT NULL,
    graph_type VARCHAR NOT NULL
);

CREATE TABLE Reports(
    report_id INT PRIMARY KEY NOT NULL,
    report_name VARCHAR NOT NULL,
    deployment_id INT REFERENCES Deployments(deployment_id)  NOT NULL,
    frequency INT NOT NULL,
    frequency_id INT REFERENCES Frequency_Map(frequency_id) NOT NULL,
    last_gen DATE NOT NULL,
    graph_id INT REFERENCES Graph_Map(graph_id) NOT NULL,
    class_list_id INT REFERENCES Class_lists(class_list_id) NOT NULL
);

CREATE TABLE Data_TotalEntry(
    entry_num INT NOT NULL,
    deployment_id INT NOT NULL,
    action_name VARCHAR NOT NULL, 
    creation_date DATE NOT NULL,
    result INT NOT NULL,
    unit VARCHAR
)
PARTITION BY RANGE (creation_date);

END;