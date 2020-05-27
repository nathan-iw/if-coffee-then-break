# if-coffee-then-break POC
The POC of the 'if-coffee-then-break' project. An ETL Python programmed to clean raw cafe data and load to an RDS instance of a SQL DB.

### Authors:

    Sam, Nathan & Alex

### Requirements: 

    PyMySQL==0.9.3

### Input: 

>(633, datetime.datetime(2020, 5, 18, 15, 46, 1), 'Isle of Wight', 'Oscar Ohara', ' Frappes - Chocolate Cookie', Decimal('2.75'), 'CASH', None)

### Input SQL table format:
> PLACE HOLDER

### Output: 

>(datetime.date(2020, 5, 18), datetime.time(15, 46, 1), 'Isle of Wight', 'Oscar', 'Ohara', 'Regular', 'Frappe', 'Chocolate Cookie', 2.75, 'Cash', None)

### Output SQL table generating queries:

>CREATE DATABASE poc_data;

>CREATE TABLE clean_transactions (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, date DATE NOT NULL, transaction_time TIME NOT NULL, location VARCHAR(50) NOT NULL, firstname VARCHAR(50) NOT NULL, lastname VARCHAR(50) NOT NULL, drink_order VARCHAR(200) NOT NULL, total_price DECIMAL(10,2), method VARCHAR(4) NOT NULL, ccn VARCHAR(20));

>CREATE TABLE drink_menu (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, drink_name VARCHAR(100) NOT NULL , drink_size VARCHAR(50), drink_flavour VARCHAR(50), price DECIMAL);
