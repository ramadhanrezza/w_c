from flask import Flask
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'website_crawl'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def init_db():
    fileOpen = open('company_profiles.json', 'r')
    company_list = json.load(fileOpen)

    if company_list:
        # create table if not exist
        conn = mysql.connect()
        cursor = conn.cursor()
        drop_table = "DROP TABLE IF EXISTS company_profiles"
        insert_table = '''
            CREATE TABLE company_profiles (id int(11) NOT NULL AUTO_INCREMENT, 
            ticker_symbol varchar(255) DEFAULT NULL, 
            uid varchar(255), country varchar(255), 
            company_name text, 
            company_street_address text, 
            company_phone_number varchar(150), 
            company_email varchar(255), 
            company_website varchar(150), 
            business varchar(255), 
            revenue float(100,0), 
            PRIMARY KEY (`id`))
        '''

        # cursor.execute(drop_table)
        # cursor.execute(insert_table)
        for item in company_list:
            print("INSERT DATA {} to database:::".format(item['ticker_symbol']))
            str_insert = '''
            INSERT INTO company_profiles (ticker_symbol, 
                                        uid, 
                                        country,
                                        company_name, 
                                        company_street_address, 
                                        company_phone_number,
                                        company_email,
                                        company_website,
                                        business,
                                        revenue)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            cursor.execute(str_insert, (item['ticker_symbol'],item['uid'],
                                        item['country'],item['company_name'],
                                        item['company_street_address'],', '.join(item['company_phone_number']),
                                        item['company_email'],item['company_website'],
                                        item['business'],item['revenue'].replace(',','')))
            conn.commit()
        
        cursor.close()
        print('INSERT DATA COMPLETED::::')



if __name__ == "__main__":
    init_db()