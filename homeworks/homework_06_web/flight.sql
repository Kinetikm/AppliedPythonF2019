create table flight (
    id INT PRIMARY KEY,
    name VARCHAR,
    dept_time TIME,
    arr_time TIME,
    travel_time TIME,
    airport VARCHAR,
    type VARCHAR
);

INSERT INTO flight(id, name, dept_time, arr_time, travel_time, airport, type)
            VALUES (0, 'PD180', '18:00', '20:00', '2:00', 'moscow', 'pass');
INSERT INTO flight(id, name, dept_time, arr_time, travel_time, airport, type)
            VALUES (1, 'DR124', '10:00', '14:00', '4:00', 'berlin', 'pass');
