# import json, requests, datetime, time, random
# import foo, script, number_checker, status_checker
#
# from datetime import datetime
#
# class WABot():
#     def __init__(self, json):
#         self.json = json
#         self.dict_messages = []
#         self.dict_ack = []
#         try:
#             self.dict_messages = json['messages']
#         except:
#             pass
#         try:
#             self.dict_ack = json['ack']
#         except:
#             pass
#         self.APIUrl = foo.APIUrl
#         self.token = foo.token
#
#     def send_requests(self, method, data):
#         url = f"{self.APIUrl}{method}?token={self.token}"
#         headers = {'Content-type': 'application/json'}
#         answer = requests.post(url, data=json.dumps(data), headers=headers)
#         return answer.json()
#
#     def send_message(self, chatId, text):
#         data = {
#             "chatId" : chatId,
#             "body" : text
#         }
#         answer = self.send_requests('sendMessage', data)
#         return answer
#
#     def processing(self):
#         if self.dict_messages != []:
#             for message in self.dict_messages:
#                 text = message['body'].split()
#                 if not message['fromMe']:
#                     id  = message['chatId']
#                     if id == foo.CHAT_ID and text[0] == foo.TRIGGER:
#                         # phone = id[:12]
#                         # print(phone)
#                         # script.check()
#                         # return self.send_message(chatId=id, text="Hello")
#                         # try:
#                         #     r = worksheet.find(phone).row
#                         #     res = number_checker.check(phone)
#                         #     if res == "not exists":
#                         #         worksheet.update(f"B{r}", "NOT PRESENT - C")
#                         #     else:
#                         #         worksheet.update(f"B{r}", "PRESENT - C")
#                         #         res = status_checker.check(phone=phone)
#                         #         if res['status'] == "available":
#                         #             resp = self.send_message(chatId=id, text="Message-1")
#                         # except CellNotFound:
#                         #     continue
#                         numbers = worksheet.col_values(1)[1:]
#                         i = 1
#                         for number in numbers:
#                             i += 1
#                             res = number_checker.check(number)
#                             if res == "not exists":
#                                 worksheet.update(f"B{i}", "NOT PRESENT - C")
#                             else:
#                                 worksheet.update(f"B{i}", "PRESENT - C")
#                                 chatId = f"{number}@c.us"
#                                 # res = status_checker.check(phone=number)
#                                 # if res['status'] == "available":
#                                 resp = self.send_message(chatId=chatId, text="Message-1")
#         if self.dict_ack != []:
#             for ack in self.dict_ack:
#                 _id = ack['id']
#                 chatId = ack['chatId']
#                 status = ack['status']
#                 phone = chatId[:12]
#                 if status == "viewed":
#                     try:
#                         r = worksheet.find(phone).row
#                         if worksheet.acell(f"C{r}").value is None:
#                             worksheet.update(f"C{r}", "Viewed")
#                             resp = self.send_message(chatId=chatId, text="Message-2")
#                         else:
#                             worksheet.update(f"D{r}", "Viewed")
#                     except:
#                         continue
#         return 'NoCommand'
