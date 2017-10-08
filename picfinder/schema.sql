drop table if exists entries;
create table entries (
  imgname text primary key,
  img blob,
  first text,
  second text,
  third text,
  fourth text,
  fifth text
);
