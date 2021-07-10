from selenium import webdriver
import time, gspread, number_checker, status_checker, requests, json
import foo

gc = gspread.service_account(filename="./service_account.json")
sh = gc.open_by_url(foo.URL)
worksheet = sh.get_worksheet(1)

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
# browser = webdriver.Firefox()
browser.get('https://watools.io/check-numbers')

input = browser.find_element_by_tag_name("input")
button = browser.find_element_by_xpath('//button[@class="btn btn-primary btn-lg mb-4 mt-4"]')

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

def check():
    numbers = worksheet.col_values(1)
    l1 = len(numbers)
    l2 = len(worksheet.col_values(2)) - 1
    for i in range(l2, l1):
        try:
            input.clear()
            number = numbers[i]
            if len(number) != 12:
                raise Exception
            # number = f"91{number}"
            phone = int(number)
            input.send_keys(number)
            time.sleep(1)
            button.click()
            time.sleep(5)
            check = browser.find_element_by_class_name("my-0")
            if check.text == "Exists on WhatsApp!":
                worksheet.update(f"B{i+1}", "PRESENT - S")
                res = status_checker.check(phone=phone)
                _id = f"{phone}@c.us"
                if res['status'] == "available":
                    resp = send_message(chatId=_id, text="Message-1")
            elif check.text == "No exists on WhatsApp":
                worksheet.update(f"B{i+1}", "NOT PRESENT - S")
            else:
                res = number_checker.check(phone)['result']
                if res == "not exists":
                    worksheet.update(f"B{i+1}", "NOT PRESENT - C")
                else:
                    worksheet.update(f"B{i+1}", "PRESENT - C")
            time.sleep(1)
        except:
            continue


if __name__ == "__main__":
    check()