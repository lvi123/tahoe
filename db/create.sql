create table obs(serial CHAR(16), timeStamp DATETIME, temp FLOAT, temp2 FLOAT, rh FLOAT, lowbatt BOOL, linkquality TINYINT, PRIMARY KEY (serial, timeStamp));
