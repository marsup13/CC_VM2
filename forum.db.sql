CREATE TABLE IF NOT EXISTS user (  id INTEGER NOT NULL,  email VARCHAR(255),  password VARCHAR(255),  name VARCHAR(255),  username VARCHAR(255),  active BOOLEAN,  confirmed_at DATETIME,  UNIQUE(username),  UNIQUE(email),  CHECK(active IN (0, 1)),  PRIMARY KEY(id) ); CREATE TABLE IF NOT EXISTS roles_users (  user_id INTEGER,  role_id INTEGER,  FOREIGN KEY(role_id) REFERENCES role(id),  FOREIGN KEY(user_id) REFERENCES user(id) ); CREATE TABLE IF NOT EXISTS thread (  id INTEGER NOT NULL,  title VARCHAR(30),  description VARCHAR(200),  date_created DATETIME NOT NULL,  PRIMARY KEY(id) ); CREATE TABLE IF NOT EXISTS reply (  id INTEGER NOT NULL,  thread_id INTEGER,  user_id INTEGER,  message VARCHAR(200),  date_created DATETIME,  FOREIGN KEY(thread_id) REFERENCES thread(id),  FOREIGN KEY(user_id) REFERENCES user(id),  PRIMARY KEY(id) );
INSERT INTO alembic_version (version_num) VALUES ('438e5072aa7c');
INSERT INTO user (id,email,password,name,username,active,confirmed_at) VALUES (1,'marwane.adala@supcom.tn','$2b$12$H40G.UVZ9i7k4KlsVvzRT.QH2dw/xAKv52EW.tHcO5/gc.GVq3hLC','MARWANE ADALA','maadac',1,NULL);
INSERT INTO thread (id,title,description,date_created) VALUES (1,'Helllo more','more is gone','2021-11-21 13:45:32.509301'),
 (2,'greetings','hello again','2021-11-21 14:39:07.564067'),
 (3,'first comment','this is a comment for you','2021-11-21 15:18:16.011170'),
 (4,'test','just  a test','2021-11-21 15:22:58.764268'),
 (5,'another thread','test laast thread','2021-11-21 16:35:05.722422'),
 (6,'last test','this is the last test here','2021-11-21 19:50:47.236858');
INSERT INTO reply (id,thread_id,user_id,message,date_created) VALUES (1,1,1,'this is the first message','2021-11-21 16:10:11.613918'),
 (2,1,1,'this is the first message','2021-11-21 16:18:05.878590'),
 (3,1,1,'this is the first message','2021-11-21 16:23:25.503527'),
 (4,1,1,'this is the first message','2021-11-21 16:26:21.178831'),
 (5,1,1,'Here you find another reply for me for this life
','2021-11-21 16:28:01.804839'),
 (6,5,1,'test retest test','2021-11-21 16:35:31.904890'),
 (7,6,1,'Hello, thank for these tests','2021-11-21 19:51:04.256607'),
 (8,6,1,'Youa are welcome, don''t worry!!!','2021-11-21 19:51:18.451327');
