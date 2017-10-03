create database if not exists survey;
use survey;
create table if not exists response (
   rowid integer auto_increment primary key,
   created       timestamp,
   firstnameEncrypted text,
   firstname          text,
   ageEncrypted       text,
   age integer
);

create table if not exists response_json (
   rowid integer auto_increment primary key,
   created       timestamp,
   jsonEncrypted text,
   json          text
);

