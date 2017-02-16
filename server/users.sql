drop table if exists users;
create table users (
    id integer primary key autoincrement,
    uname string not null,
    pwd string not null,
    userid string not null,
    score integer
);
