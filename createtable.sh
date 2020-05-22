sql_query = "INSERT INTO transactions (date, time, location, firstname, lastname, order, total_price, method, ccn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

CREATE DATABASE IF NOT EXISTS poc_data;

USE poc-data;

CREATE TABLE clean_transactions (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, date DATE NOT NULL, transaction_time TIME NOT NULL, location VARCHAR(50) NOT NULL, firstname VARCHAR(50) NOT NULL, lastname VARCHAR(50) NOT NULL, drink_order VARCHAR(200) NOT NULL, total_price DECIMAL(10,2), method VARCHAR(4) NOT NULL, ccn VARCHAR(10));

CREATE TABLE drink_menu (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, drink_name VARCHAR(100) NOT NULL , drink_size VARCHAR(50), drink_flavour VARCHAR(50), price DECIMAL);
ALTER TABLE drink_menu ADD UNIQUE unique_index (drink_name,drink_size,drink_flavour);

ALTER TABLE drink_menu ADD drink_size VARCHAR(20) AFTER drink_name;

ALTER TABLE drink_menu ADD drink_flavour VARCHAR(50) AFTER drink_size;

