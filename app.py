from flask import Flask, request, jsonify
# from wabot import WABot
import status_checker, number_checker, foo
import datetime, requests, json
from datetime import date, datetime
import sqlite3 as sql

app = Flask(__name__)


def send_requests(method, data):
    url = f"{foo.APIUrl}{method}?token={foo.token}"
    headers = {'Content-type': 'application/json'}
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    return answer.json()


def send_message(chatId, text):
    data = {
        "chatId" : chatId,
        "body" : text
    }
    answer = send_requests('sendMessage', data)
    return answer


@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        dict_messages = []
        dict_ack = []
        try:
            dict_messages = request.json['messages']
            print(dict_messages)
        except:
            pass
        try:
            dict_ack = request.json['ack']
            print(dict_ack)
        except:
            pass
        if dict_messages:
            for message in dict_messages:
                text = message['body'].split()
                if not message['fromMe']:
                    _id = message['chatId']
                    if _id == foo.CHAT_ID and text[0] == foo.TRIGGER:
                        con = sql.connect("database.db")
                        con.row_factory = sql.Row
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users")
                        rows = cur.fetchall()
                        numbers = [row[0] for row in rows]
                        i = 1
                        for number in numbers:
                            i += 1
                            res = number_checker.check(number)
                            if res == "not exists":
                                command = '''
                                    UPDATE Users
                                    SET WhatsApp=?
                                    WHERE Phone=?
                                '''
                                cur.execute(command, ("NOT PRESENT - C", "", "", int(number)))
                                con.commit()
                            else:
                                # worksheet.update(f"B{i}", "PRESENT - C")
                                command = '''
                                    UPDATE Users
                                    SET WhatsApp=?,
                                        "M1 - Read"=?,
                                        "M2 - Read"=?
                                    WHERE Phone=?
                                '''
                                cur.execute(command, ("PRESENT - C", "", "", int(number)))
                                con.commit()
                                chatId = f"{number}@c.us"
                                # res = status_checker.check(phone=number)
                                # if res['status'] == "available":
                                resp = send_message(chatId=chatId, text="Message-1")
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
                        if row[4] == "":
                            cur.execute('UPDATE Users SET "M1 - Read"=? WHERE Phone=?',
                                        ("Yes", phone))
                            con.commit()
                            resp = send_message(chatId=chatId, text="Message-2")
                        else:
                            cur.execute('UPDATE Users SET "M2 - Read"=? WHERE Phone=?',
                                        ("Yes", phone))
                            con.commit()
                    except:
                        continue
                elif status == "sent":
                    try:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users WHERE Phone=?", (phone,))
                        row = cur.fetchone()
                        if row[2] == "No":
                            cur.execute('UPDATE Users SET "M1 - Sent"=? WHERE Phone=?',
                                        ("Yes", phone))
                        else:
                            cur.execute('UPDATE Users SET "M2 - Sent"=? WHERE Phone=?',
                                        ("Yes", phone))
                        con.commit()
                    except:
                        continue
                elif status == "delivered":
                    try:
                        con = sql.connect("database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM Users WHERE Phone=?", (phone,))
                        row = cur.fetchone()
                        if row[3] == "No":
                            cur.execute('UPDATE Users SET "M1 - Delivered"=? WHERE Phone=?',
                                        ("Yes", phone))
                        else:
                            cur.execute('UPDATE Users SET "M2 - Delivered"=? WHERE Phone=?',
                                        ("Yes", phone))
                        con.commit()
                    except:
                        continue
        return 'NoCommand'


@app.route("/check", methods=['GET'])
def check():
    if request.method == 'GET':
        # req = request.json
        # print(req)
        try:
            # phone = req['phone']
            phone = request.args.get('phone')
            resp = status_checker.check(phone=phone)
            if resp['status'] != "available":
                try:
                    print(resp['lastSeen'])
                    _time = datetime.fromtimestamp(resp['lastSeen'])
                    print(_time)
                    resp['lastSeen'] = _time
                except:
                    pass
        except:
            resp = {"message": "Please enter a valid mobile number!"}
        print(resp)
        return resp


if __name__ == '__main__':
    app.run()
