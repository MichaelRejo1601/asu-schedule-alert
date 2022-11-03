import os
import traceback
import logging
from dotenv import load_dotenv
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import atexit

def crash_message():
    message = client.messages.create(
        body='Session Crashed',
        from_='+19793785584',
        to=phone)
    print(message.sid)

def clear_session(driver):
    driver.delete_all_cookies()
    sleep(1)
    print("Cleared Cookies")

def start_session(driver):
    driver.get(urls["main"])

    # WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.ID, "user-date-env-style"), 'ASUCSPRD'))
    print("On Page")

def run_session(driver): #recurring process 
    print("Running")
    try: 
        for num in course_nums:
            sleep(2)
            print(num)
            driver.find_element(By.ID, "keyword").send_keys(num)
            driver.find_element(By.ID, "search-button").click()
            sleep(2)
            seats = driver.find_element(By.XPATH, "//div[@class='class-results-cell seats']").text.split()
            if course_nums[num][1] != seats[0]:
                instructor = driver.find_element(By.XPATH, "//div[@class='class-results-cell instructor']")
                course_nums[num] = [instructor.text, seats[0], seats[2]]
                message = client.messages.create(
                    body='{0} now has {1} of {2} seats available for course #{3}'.format(course_nums[num][0], course_nums[num][1], course_nums[num][2], num),
                    from_='+19793785584',
                    to=phone)
                print(message.sid)
                print("Updated {0} Course".format(num))

    except:
        raise

urls = {
    "main":"https://catalog.apps.asu.edu/catalog/classes/classlist"
}

course_nums = {

}

with open("courses.txt") as file:
    for line in file:
        if line.isdigit():
            course_nums[line] = [None, None, None]

print(course_nums)

load_dotenv() #enviroment
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
phone = os.getenv('PHONE')

print(account_sid)
print(auth_token)
print(phone)

client = Client(account_sid, auth_token)
driver = webdriver.Chrome()

message = client.messages.create(
    body='Starting Session',
    from_='+19793785584',
    to=phone)
print(message.sid)

urls = {
    "main":"https://catalog.apps.asu.edu/catalog/classes/classlist"
}

course_nums = {

}

with open("courses.txt") as file:
    for line in file:
        if line.isdigit():
            course_nums[line] = [None, None, None]

print(course_nums)

load_dotenv() #enviroment
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
phone = os.getenv('PHONE')

print(account_sid)
print(auth_token)
print(phone)

message = client.messages.create(
    body='Starting Session',
    from_='+19793785584',
    to=phone)
print(message.sid)

atexit.register(crash_message)

while(True):
    print("Restarting Cycle")
    try:
        clear_session(driver)
        start_session(driver)
        run_session(driver)
    except Exception as e:
        print(traceback.exec())


