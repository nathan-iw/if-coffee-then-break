sql_query = "INSERT INTO transactions (date, time, location, firstname, lastname, order, total_price, method, ccn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

CREATE DATABASE IF NOT EXISTS poc_data;

USE poc-data;

CREATE TABLE clean_transactions (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, date DATE NOT NULL, transaction_time TIME NOT NULL, location VARCHAR(50) NOT NULL, firstname VARCHAR(50) NOT NULL, lastname VARCHAR(50) NOT NULL, drink_order VARCHAR(200) NOT NULL, total_price DECIMAL(10,2), method VARCHAR(4) NOT NULL, ccn VARCHAR(10));

CREATE TABLE basket (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, trans_id varchar(36) NOT NULL, transaction_time TIME NOT NULL, location VARCHAR(50) NOT NULL, firstname VARCHAR(50) NOT NULL, lastname VARCHAR(50) NOT NULL, drink_order VARCHAR(200) NOT NULL, total_price DECIMAL(10,2), method VARCHAR(4) NOT NULL, ccn VARCHAR(10));


CREATE TABLE drink_menu (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, drink_name VARCHAR(100) NOT NULL , drink_size VARCHAR(50), drink_flavour VARCHAR(50), price DECIMAL);
ALTER TABLE drink_menu ADD UNIQUE unique_index (drink_name,drink_size,drink_flavour);

ALTER TABLE drink_menu ADD drink_size VARCHAR(20) AFTER drink_name;

ALTER TABLE drink_menu ADD drink_flavour VARCHAR(50) AFTER drink_size;

ALTER TABLE drinks_menu
ADD CONSTRAINT unique UNIQUE (drink_name,size,flavour);

ALTER TABLE locations ADD ids INT(AUTO_INCREMENT NOT NULL) AFTER id; 

# Queries

select drink_name, size, count(*) as drink_size_frequency from clean_transactions group by drink_name order by count(*) desc;

select drink_name, size NOT NULL, count(*) as drink_size_frequency from clean_transactions group by drink_name order by count(*) desc;

select drink_name, count(*) as drink_count from clean_transactions group by drink_name order by count(*) desc;

# Set up foerign key

ALTER TABLE Orders
ADD FOREIGN KEY (PersonID) REFERENCES Persons(PersonID);




echo "export test='TEST'" > ~/.bash_profile &&
echo "export DB_USER_SAINS='sam'" >> ~/.bash_profile &&
echo "export DB_PW_SAINS='s1LmE2%&&uVgmi\$hdrN&eOI&aULLD\$!xM1#h70E%'" >> ~/.bash_profile &&
echo "export DB_HOST_SAINS='sainsburys-cafe-prod.cqohmuwgawul.eu-west-1.rds.amazonaws.com'" >> ~/.bash_profile &&
echo "export DB_NAME_SAINS='cafe-data'" >> ~/.bash_profile &&
echo "export DB_USER2='admin'" >> ~/.bash_profile &&ddsds
echo "export DB_PW2='zA8bnZeg7huCIKnLgXfEqq3c'" >> ~/.bash_profile &&
echo "export DB_HOST2='cafe-poc.cqohmuwgawul.eu-west-1.rds.amazonaws.com'" >> ~/.bash_profile &&
echo "export DB_NAME2='poc_data'" >> ~/.bash_profile 
