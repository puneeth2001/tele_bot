import json 
import requests
import datetime
import server
import mysql.connector
from mysql.connector import MySQLConnection, Error
def query_with_fetchall(day):

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='python_mysql',
                                       user='puneethchanda',
                                       password='Jyothiraj_112')
        cursor = conn.cursor()
        if(day == 'Monday'):
            cursor.execute("SELECT Monday FROM `tt` WHERE 1")
        elif(day == 'Tuesday'):
            cursor.execute("SELECT Tuesday FROM `tt` WHERE 1")
        elif(day == 'Wednesday'):
            cursor.execute("SELECT Wednesday FROM `tt` WHERE 1")
        elif(day == 'Thursday'):
            cursor.execute("SELECT Thursday FROM `tt` WHERE 1")
        elif(day == 'Friday'):
            cursor.execute("SELECT Friday FROM `tt` WHERE 1")
        rows = cursor.fetchall()
        
        for i in rows:
            a.append(i)
    
    except Error as k:
        print(k)
    return(a)

TOKEN = "<Place-TOKEN-Here>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_chat_id(updates,i):
    num_updates = len(updates["result"])
    chat_id = updates["result"][i]["message"]["chat"]["id"]
    return (chat_id)

def no_subscribers(updates):
    num_subs = len(updates["result"])
    return(num_subs)

def send_message(tt,chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(tt, chat_id)
    get_url(url)

def insert_book(chat_id):
    query = "insert into users(chat_id) values ('" + chat_id + "');"

    try:
        conn =  mysql.connector.connect(host = "localhost", database = "python_mysql", user="puneethchanda", password = "Jyothiraj_112")
 
        cursor = conn.cursor()
        cursor.execute(query)
 
        conn.commit()
    except Error as error:
        print(error)

if __name__ == '__main__':
    a=[]
    k=[]
    conn =  mysql.connector.connect(host = "localhost", database = "python_mysql", user="puneethchanda", password = "Jyothiraj_112")
    cursor = conn.cursor()
    for i in range(no_subscribers(get_updates())):
        b=str(get_chat_id(get_updates(),i))
        insert_book(b)
    cursor.execute("SELECT DISTINCT chat_id FROM users")
    rows = cursor.fetchall()    
    for i in rows:
        k.append(i)
    now = datetime.datetime.now()
    day=now.strftime("%A")
    query_with_fetchall(day)
    for i in range(len(k)):
        for j in range(len(a)):
            tt=a[j][0]
            chat = k[i][0]
            print(k[i][0])
            send_message(tt, chat)
