import datetime
import json
import requests
import sqlite3 as sql
from datetime import datetime

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler

import foo
import number_checker
import status_checker

application = Flask(__name__)

scheduler = BackgroundScheduler()


def send_requests(method, data):
    url = f"{foo.APIUrl}{method}?token={foo.token}"
    headers = {'Content-type': 'application/json'}
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    return answer.json()


def send_message(chatId, text):
    data = {
        "chatId": chatId,
        "body": text
    }
    answer = send_requests('sendMessage', data)
    return answer


def check_all_numbers():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Users WHERE Online=?", (0,))
    rows = cur.fetchall()
    numbers = [row[0] for row in rows]
    for number in numbers:
        res = status_checker.check(number)
        if res['status'] != "unavailable":
            command = '''
                UPDATE Users
                SET Online=?
                WHERE Phone=?
            '''
            cur.execute(command, (1, int(number)))
            con.commit()
            resp = send_message(chatId=f"{number}@c.us", text="Message-1")


@application.route("/getNumbers", methods=["POST"])
def get_numbers():
    if request.method == "POST":
        


@application.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        dict_messages = []
        dict_ack = []
        try:
            dict_messages = request.json['messages']
            print(dict_messages)
        except KeyError:
            dict_ack = request.json['ack']
            print(dict_ack)
        if dict_messages:
            for message in dict_messages:
                text = message['body']
                _id = message['chatId']
                if not message['fromMe']:
                    if _id == foo.CHAT_ID and text == foo.TRIGGER:
                        con = sql.connect("database.db")
                        con.row_factory = sql.Row
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users")
                        rows = cur.fetchall()
                        numbers = [row[0] for row in rows]
                        for number in numbers:
                            res = number_checker.check(number)
                            if res != "not exists":
                                command = '''
                                    UPDATE Users
                                    SET WhatsApp=?
                                    WHERE Phone=?
                                '''
                                cur.execute(command, (1, int(number)))
                                con.commit()
                        scheduler.add_job(func=check_all_numbers, trigger='interval', seconds=10)
                        scheduler.start()
                    else:
                        number = _id[:12]
                        try:
                            con = sql.connect("database.db")
                            con.row_factory = sql.Row
                            cur = con.cursor()
                            cur.execute("SELECT * FROM Users WHERE Phone=?", (number,))
                            resp = send_message(chatId=_id, text="https://www.example.com/")
                        except:
                            pass
        if dict_ack:
            for ack in dict_ack:
                _id = ack['id']
                chatId = ack['chatId']
                status = ack['status']
                phone = int(chatId[:12])
                if status == "viewed":
                    try:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users WHERE Phone=?", (phone,))
                        row = cur.fetchone()
                        if row[5] == 0:
                            cur.execute('UPDATE Users SET "M1 - Read"=? WHERE Phone=?',
                                        (1, phone))
                            con.commit()
                            # resp = send_message(chatId=chatId, text="Message-2")
                        else:
                            cur.execute('UPDATE Users SET "M2 - Read"=? WHERE Phone=?',
                                        (1, phone))
                            con.commit()
                    except:
                        continue
                elif status == "sent":
                    try:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users WHERE Phone=?", (phone,))
                        row = cur.fetchone()
                        if row[3] == 0:
                            cur.execute('UPDATE Users SET "M1 - Sent"=? WHERE Phone=?',
                                        (1, phone))
                        else:
                            cur.execute('UPDATE Users SET "M2 - Sent"=? WHERE Phone=?',
                                        (1, phone))
                        con.commit()
                    except:
                        continue
                elif status == "delivered":
                    try:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users WHERE Phone=?", (phone,))
                        row = cur.fetchone()
                        if row[4] == 0:
                            cur.execute('UPDATE Users SET "M1 - Delivered"=? WHERE Phone=?',
                                        (1, phone))
                        else:
                            cur.execute('UPDATE Users SET "M2 - Delivered"=? WHERE Phone=?',
                                        (1, phone))
                        con.commit()
                    except:
                        continue
        return 'NoCommand'


# @app.route("/check", methods=['GET'])
# def check():
#     if request.method == 'GET':
#         # req = request.json
#         # print(req)
#         try:
#             # phone = req['phone']
#             phone = request.args.get('phone')
#             resp = status_checker.check(phone=phone)
#             if resp['status'] != "available":
#                 try:
#                     print(resp['lastSeen'])
#                     _time = datetime.fromtimestamp(resp['lastSeen'])
#                     print(_time)
#                     resp['lastSeen'] = _time
#                 except:
#                     pass
#         except:
#             resp = {"message": "Please enter a valid mobile number!"}
#         print(resp)
#         return resp


if __name__ == '__main__':
    application.run()
