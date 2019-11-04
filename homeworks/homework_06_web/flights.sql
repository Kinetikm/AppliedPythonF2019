drop table if exists flight, destination_airport, type_aircraft, log;

CREATE TABLE destination_airport(
    id SERIAL NOT NULL PRIMARY KEY,
    airport VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE type_aircraft(
    id SERIAL NOT NULL PRIMARY KEY,
    aircraft VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE flight(
    id SERIAL NOT NULL PRIMARY KEY,
    id_da INT NOT NULL REFERENCES destination_airport(id),
    id_ta INT NOT NULL REFERENCES type_aircraft(id),
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    travel_time TIME NOT NULL
);

CREATE TABLE log(
    id SERIAL NOT NULL PRIMARY KEY,
    arrival_time TIME NOT NULL,
    url VARCHAR(100) NOT NULL,
    method VARCHAR(6) NOT NULL,
    action VARCHAR(17) NOT NULL,
    body VARCHAR(500),
    response VARCHAR(1000),
    http_status INT NOT NULL,
    duration Float NOT NULL
);

CREATE INDEX func_index ON log USING HASH (action);