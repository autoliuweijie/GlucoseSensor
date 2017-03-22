create database if not exists glucose_sensor;
use glucose_sensor;

create table if not exists devices(
  d_id int auto_increment not null,
  type char(8) not null,
  unicode char(20) not null,
  date date not null,
  others varchar(100),
  primary key (d_id),
  unique (unicode)
);

create table if not exists users(
  u_id int auto_increment not null,
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
  r_id int auto_increment not null,
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
  reference_blood_pressure int,
  primary key (r_id)
);

create user 'glucose'@'localhost' identified by 'glucosepassword';
grant select, update, insert on glucose_sensor.* to 'glucose'@'localhost' identified by 'glucosepassword';


insert into glucose_sensor.devices(d_id, type, unicode, date, others) values(1, 1, 'ICSLNGM0001', '2017-03-22', 'test');
insert into users(username, password, email, age, gender, diabetes, unicode, phone) values('liuweijie', 'liuweijie', 'liuweijie@liu.com', 23, 1, 0, 'ICSLNGM0001', NULL);
insert into records (video_name, unicode, record_time, u_id) values( '1_20170322162859.webm', 'ICSLNGM0001', '2017-03-22 16:28:59', 1);