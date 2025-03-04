PRAGMA user_version=2;

create table setting (
    id integer primary key,
    key varchar not null unique,
    value varchar
);