PRAGMA user_version=1;
PRAGMA foreign_keys = ON;

create table game (
    id integer primary key,
    name varchar not null,
    game_id varchar,

    game_path varchar not null,
    mod_path varchar not null,
    download_path varchar not null,
    overwrite_path varchar not null,
    work_path varchar not null
);

create table mod (
    id integer primary key,
    name varchar,
    load_order integer,
    active boolean,
    nexus_mod_id integer,
    version_id integer,
    game_id integer not null,
    latest_version varchar,
    tags text,
    FOREIGN KEY(version_id) REFERENCES mod_version(id),
    FOREIGN KEY(game_id) REFERENCES game(id)
);

create table mod_version (
    id integer primary key,
    nexus_mod_id integer,
    nexus_file_id integer,
    version varchar,
    game_id integer not null,
    path varchar not null,
    FOREIGN KEY(game_id) REFERENCES game(id)
);
