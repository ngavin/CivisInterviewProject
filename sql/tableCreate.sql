CREATE TABLE Stop (
    id smallint PRIMARY KEY,
    on_street varchar(64),
    cross_street varchar(64),
    routes smallint[],
    boardings decimal(5,1),
    alightings decimal(5,1),
    creation timestamp,
    daytype varchar(7),
    coordinates point
);
