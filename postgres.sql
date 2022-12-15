    -- DATA DEFINITION
-- creating 3 tables: 1. clients(id(PK), name, surname, birthdate, age, email, country);
--                    2. client_accounts(account_id(PK), account_type, client_id, balance, currency_code);
--                    3. accounts(id(PK), name)

CREATE TABLE clients (
	id SERIAL PRIMARY KEY,
	name VARCHAR(30),
	surname VARCHAR(30),
	birthdate DATE,
	age INT,
	country_code CHAR(3)
    );

CREATE TABLE client_accounts (
	account_id SERIAL PRIMARY KEY,
	account_type INT NOT NULL,
	client_id VARCHAR(3) NOT NULL,
	balance NUMERIC(10, 3),
	currency_code VARCHAR(3),
    );

CREATE TABLE accounts (
	id SERIAL PRIMARY KEY,
	name VARCHAR(30) NOT NULL
    );


ALTER TABLE clients
    DROP COLUMN age
	ADD COLUMN email VARCHAR(30) UNIQUE
    RENAME COLUMN country_code TO country
    ALTER COLUMN country TYPE INT USING country::INT;

ALTER TABLE client_accounts
	ALTER COLUMN balance SET DEFAULT 0,
	ALTER COLUMN client_id TYPE INTEGER USING client_id::INTEGER;

-- adding FK to client_accounts table, column client_id referencing to clients.id
ALTER TABLE client_accounts
	ADD CONSTRAINT fk_client_id
	FOREIGN KEY (client_id)
	REFERENCES clients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE;

-- adding FK to client_accounts table, column account_type referencing to accounts.id
ALTER TABLE client_accounts
ADD CONSTRAINT fk_type
FOREIGN KEY (account_type)
REFERENCES accounts("id");


-- creating tables 1. countries(id(PK), country_code, name, currency_code) and
                -- 2. currencies(code(PK), name, rate_per_1EUR)
-- the data for these tables will be imported through pgadmin from already created csv tables 'countries.csv' and 'currencies.csv'
CREATE TABLE countries(
	id SERIAL PRIMARY KEY,
	country_code CHAR(3),
	name VARCHAR(60) NOT NULL,
	currency_code CHAR(3)
    );

CREATE TABLE currencies (
	code CHAR(3) PRIMARY KEY,
	name VARCHAR(30),
	rate_per_1EUR DECIMAL
	);

--setting clients.country to FK referencing to countries.id
ALTER TABLE clients
ADD CONSTRAINT fk_country
FOREIGN KEY (country)
REFERENCES countries("id");

--setting client_accounts.currency_code to FK referencing to currencies.code
ALTER TABLE client_accounts
ADD CONSTRAINT fk_currency_code
FOREIGN KEY (currency_code)
REFERENCES currencies(code);

-- creating a new table clients_age_groups with column client's age
CREATE TABLE clients_age_groups AS
SELECT clients.id as client_id, EXTRACT(YEAR FROM AGE(NOW(), birthdate)) AS age
FROM clients;


    -- DATA MANIPULATION
--inserting data into clients
INSERT INTO clients
VALUES	(1, 'Hristo', 'Ivanov', '1979-03-15', 'hristo@gmail.com', 13),
		(2, 'Ivana', 'Trump', '1982-05-15', 'iva@gmail.com', 10),
		(3, 'Zahari', 'Stoyanov', '1964-09-10', 'zsto@abv.bg', 13),
		(4, 'Beatrice', 'Johnson', '1990-04-05', 'beatrice@hotmail.com', 9),
		(5, 'Dwayne', 'Stayze', '1988-07-20', 'dwaynee@gmail.com', 78),
		(6, 'Natalia', 'Moskova', '1990-04-25', 'nmoskova@gmail.com', 13),
		(7, 'Petar', 'Cohl', '1977-11-15', 'petar@gmail.com', 13),
		(8, 'Stoyan', 'Stoyanov', '1980-03-15', 'stoykata@abv.bg', 13),
		(9, 'Ava', 'Georgieva', '1999-10-21', 'ava@abv.bg', 13),
		(10, 'Penka', 'Kostova', '1966-01-29', 'pepi@abv.bg', 13),
        (11, 'Hristo', 'Ivanov', '1979-03-15', 'hristo22@gmail.com', 99);

--trying to insert a non-existing country_code '2000'
INSERT INTO clients
VALUES	(12, 'Hristo', 'Ivanov', '1979-03-15', 'hristo2e2@gmail.com', 2000)
--gave the following error
ERROR:  insert or update on table "clients" violates foreign key constraint "fk_country"
DETAIL:  Key (country)=(2000) is not present in table "countries".

--trying to insert an email which already exists
INSERT INTO clients
VALUES	(12, 'Hristo', 'Ivanov', '1979-03-15', 'hristo22@gmail.com', 14)
-- gave the following error
ERROR:  duplicate key value violates unique constraint "clients_email_key"
DETAIL:  Key (email)=(hristo22@gmail.com) already exists.

--inserting data into accounts and client_accounts
INSERT INTO accounts
	VALUES  (1, 'basic'),
			(2, 'current'),
			(3, 'savings'),
			(4, 'student'),
			(5, 'children'),
			(6, 'deposit');


INSERT INTO client_accounts
VALUES (1, 2, 1, 3000, 'BGN'),
       (2, 1, 2, 1560, 'AMD'),
	   (3, 4, 5, 20550, 'BGN'),
	   (4, 4, 3, 1000, 'ARS'),
	   (5, 5, 6, 10000, 'BGN'),
	   (6, 3, 8, 20, 'EUR'),
	   (7, 3, 2, 1300, 'BGN'),
	   (8, 4, 9, 20000, 'EUR'),
	   (9, 1, 9, 200, 'BGN'),
	   (10, 2, 7, 1000, 'EUR'),
	   (11, 3, 10, 15000, 'USD');


 -- DATA QUERY
 -- using inner join between tables client_accounts and clients with balance >=1000 AND <=10000
SELECT ca.account_id, CONCAT(c.name,' ', c.surname) as full_name, ca.balance, ca.currency_code
FROM client_accounts AS ca
JOIN clients AS "c"
ON ca.client_id = c.id
    WHERE balance BETWEEN 1000 AND 10000;

1	"Hristo Ivanov"	3000.000	"BGN"
2	"Ivana Trump"	1560.000	"AMD"
4	"Zahari Stoyanov"	1000.000	"ARS"
5	"Natalia Moskova"	10000.000	"BGN"
7	"Ivana Trump"	1300.000	"BGN"
10	"Petar Cohl"	1000.000	"EUR"


-- WHEN CASE, grouping the clients by age
  SELECT client_id, age,
    CASE WHEN age BETWEEN 12 AND 17 THEN 'children'
      WHEN age BETWEEN 18 AND 25 THEN 'young adults'
      WHEN age BETWEEN 26 AND 40 THEN 'adults'
      WHEN age BETWEEN 41 AND 60 THEN 'middle-age adults'
      WHEN age > 60 THEN 'older adults'
    END AS age_group
  FROM clients_age_group
  ORDER BY age DESC;

-- query output
client_id, age, age_group
3	58	"middle-age adults"
10	56	"middle-age adults"
7	45	"middle-age adults"
1	43	"middle-age adults"
11	43	"middle-age adults"
8	42	"middle-age adults"
2	40	"adults"
5	34	"adults"
6	32	"adults"
4	32	"adults"
9	23	"young adults"

-- total balance of all clients_accounts grouped by currencies
SELECT ca.currency_code, ROUND(SUM(ca.balance * c.rate_per_1EUR)) AS total_in_EUR
FROM client_accounts AS ca
	JOIN currencies AS c
		ON ca.currency_code = c.code
		GROUP BY ca.currency_code

currency_code, total_in_EUR
"BGN"	68580
"ARS"	179275
"USD"	15832
"AMD"	650638
"EUR"	21020

-- JOIN BETWEEN 4 TABLES
SELECT c.id, CONCAT(c.name, ' ', c.surname) AS full_name,ca.account_type, ca.balance, ca.currency_code as currency, c2.name, c1.name as address
FROM client_accounts AS ca
	JOIN clients AS c
		ON ca.client_id = c.id
	JOIN countries AS c1
		ON c.country = c1.id
	JOIN currencies AS c2
		ON ca.currency_code = c2.code
ORDER BY currency;
--
id, full name, balance, currency, name, address
2	"Ivana Trump"	1	1560.000	"AMD"	"Armenian Dram"	"Argentina"
3	"Zahari Stoyanov"	4	1000.000	"ARS"	"Argentine Peso"	"Australia"
5	"Dwayne Stayze"	4	20550.000	"BGN"	"Bulgarian Lev"	"Fiji"
9	"Ava Georgieva"	1	200.000	"BGN"	"Bulgarian Lev"	"Australia"
6	"Natalia Moskova"	5	10000.000	"BGN"	"Bulgarian Lev"	"Australia"
1	"Hristo Ivanov"	2	3000.000	"BGN"	"Bulgarian Lev"	"Australia"
2	"Ivana Trump"	3	1300.000	"BGN"	"Bulgarian Lev"	"Argentina"
8	"Stoyan Stoyanov"	3	20.000	"EUR"	"Euro"	"Australia"
9	"Ava Georgieva"	4	20000.000	"EUR"	"Euro"	"Australia"
7	"Petar Cohl"	2	1000.000	"EUR"	"Euro"	"Australia"
10	"Penka Kostova"	3	15000.000	"USD"	"US Dollar"	"Australia"