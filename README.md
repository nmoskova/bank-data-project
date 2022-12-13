# bank-data-project
ETL project using Pandas/BeautifulSoup/SQL/PosgreSQL

Extract - extracting data from three sources - 2 different web-sites using requests and BeautifulSoup and 
                                               a REST API https://apilayer.com/ through requests

Transform - modifying the data with Pandas into the desired format, creating three tables: 
    1. country_codes
    2. currencies
    3. exchange_rates

Load - importing the above described 3 tables in PostgreSQL and creating three additional tables using SQL:
    1. client_accounts
    2. clients
    3. clients_by_age_groups ,
    
    inserting data into them and making some data queries to the DB.
 
 
 
