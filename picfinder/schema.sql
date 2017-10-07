drop table if exists entries;
create table entries (
  imgname text primary key,
  first text not null,
  second text not null,
  third text not null,
  fourth text not null,
  fifth text not null
);
