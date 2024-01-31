SET SCHEMA 'vision_data';

BEGIN;

CREATE TYPE FREQUENCY_UNIT AS ENUM ('day','week','month','year');

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

CREATE TABLE Classes(
    class_id INT PRIMARY KEY NOT NULL,
    class_name VARCHAR NOT NULL,
    data_count INT NOT NULL
);

CREATE TABLE ClassSources(
    class_source_id INT PRIMARY KEY NOT NULL,
    class_id INT REFERENCES Classes(class_id) NOT NULL,
    source_id INT REFERENCES Sources(source_id) NOT NULL
);

CREATE TABLE Categories(
    category_id INT PRIMARY KEY NOT NULL,
    category_name VARCHAR
);

CREATE TABLE ClassCategories(
    class_category_id INT PRIMARY KEY NOT NULL,
    class_id INT REFERENCES Classes(class_id),
    category_id INT REFERENCES Categories(category_id)
);

CREATE TABLE Models(
    model_id INT PRIMARY KEY NOT NULL,
    model_name VARCHAR NOT NULL,
    creation_date DATE NOT NULL
);

CREATE TABLE ModelClasses(
    model_class_id INT PRIMARY KEY NOT NULL,
    model_id INT REFERENCES Models(model_id),
    class_id INT REFERENCES Classes(class_id)
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

CREATE TABLE GraphMap(
    graph_id INT PRIMARY KEY NOT NULL,
    graph_type VARCHAR NOT NULL
);

CREATE TABLE Reports(
    report_id INT PRIMARY KEY NOT NULL,
    report_name VARCHAR NOT NULL,
    deployment_id INT REFERENCES Deployments(deployment_id)  NOT NULL,
    frequency_value DECIMAL(4,2) NOT NULL,
    frequency_unit FREQUENCY_UNIT NOT NULL,
    last_gen DATE,
    graph_id INT REFERENCES GraphMap(graph_id) NOT NULL
);

CREATE TABLE ReportClasses(
    report_class_id INT PRIMARY KEY NOT NULL,
    class_id INT REFERENCES Classes(class_id),
    report_id INT REFERENCES Reports(report_id)
);

CREATE TABLE DataTotalEntry(
    entry_num INT NOT NULL,
    deployment_id INT NOT NULL,
    class_id INT NOT NULL REFERENCES Classes(class_id), 
    creation_date DATE NOT NULL,
    result INT NOT NULL,
    unit VARCHAR
)
PARTITION BY RANGE (creation_date);

END;