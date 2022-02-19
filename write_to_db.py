from cgi import test
import mysql.connector
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

host = config['MySQL']['host']
user = config['MySQL']['user']
database = config['MySQL']['database']
password = config['MySQL']['password']


def timestamp():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor()


def write_db(list):
    for el in list:
        sql = "INSERT INTO dixy (name, price, qty, mesure, date) VALUES (%s, %s, %s, %s, %s)"
        name = el[0]
        price = float(el[1])
        try:
            qty = int(el[2])
        except ValueError as err:
            qty = 0
        mesure = el[3]

        val = (name, price, qty, mesure, timestamp())
        # print(val)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

# test_list = [['test', 0, 0, 'kg', timestamp()], ['test', 0, 0, 'kg', timestamp()]] #For test
# wrire_to_db(test_list)
