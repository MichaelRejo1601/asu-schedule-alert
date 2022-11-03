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

urls = {
  "login":"https://cs.oasis.asu.edu/psp/asucsprd/?cmd=logout&cmd=login&errorCode=127&languageCd=ENG"
}
load_dotenv() #enviroment
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
username = os.getenv('U')
password = os.getenv('P')

print(account_sid)
print(auth_token)

course_nums = {

}

with open("courses.txt") as file:
    for line in file:
        if line.isdigit():
            course_nums[line] = [None, None, None]

print(course_nums)

def clear_session(driver): #clear session 
  # message = client.messages.create(
  # body='Ending Session',
  # from_='+19793785584',
  # to='+19252165474'
  # print(message.sid)
  driver.delete_all_cookies()
  sleep(5) 
  print("Cleared Cookies")

def start_session(driver): #start session 
  # message = client.messages.create(
  # body='Restarting Session and Logging In',
  # from_='+19793785584',
  # to='+19252165474'
  # print(message.sid)
  driver.get(urls["login"])
  driver.find_element_by_id("userid").send_keys(username)
  driver.find_element_by_id("pwd").send_keys(password)  
  driver.find_element_by_name("Submit").click()
  
  WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.ID, "user-date-env-style"), 'ASUCSPRD'))
    

  print("Logged In")

def run_session(driver): #recurring process 
  print("Running")

client = Client(account_sid, auth_token)
driver = webdriver.Chrome()

while(True):
  print("Restarting Cycle")
  try:
    clear_session(driver)
    start_session(driver)
  except Exception as e:
    logging.error(traceback.format_exc())
  else:
    run_session(driver)
