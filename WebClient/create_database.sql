create database if not exists glucose_sensor;
use glucose_sensor;

create table if not exists devices(
  d_id int not null,
  type char(8) not null,
  unicode char(20) not null,
  date date not null,
  others varchar(100),
  primary key (d_id),
  unique (unicode)
);

create table if not exists users(
  u_id int not null,
  username varchar(50) not null,
  password varchar(200) not null,
  email varchar(100) not null,
  phone char(20),
  age int not null,
  gender bit not null,
  weights int,
  heights int,
  diabetes bit not null,
  unicode char(20) not null references devices(unicode),
  primary key (u_id),
  unique (username)
);

create table if not exists records(
  r_id int not null,
  u_id int not null references users(u_id),
  record_time datetime not null,
  unicode char(20) not null references devices(unicode),
  video_name char(20) not null,
  predict_blood_glucose int,
  predict_blood_oxygen int,
  predict_heart_rate int,
  predict_body_temperature int,
  predict_blood_pressure int,
  reference_blood_glucose int,
  reference_blood_oxygen int,
  reference_heart_rate int,
  reference_body_temperature int,
  reference_blood_pressure int
);

create user 'glucose'@'localhost' identified by 'glucosepassword';
grant select, UPDATE on glucose_sensor.* to 'glucose'@'localhost';
