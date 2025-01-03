from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

print('found file!')
load_dotenv('/Users/carolinabolnykh/Desktop/winterBreak/dmvBot/dmv/.env')
print('loaded envs')
print(time.time())
service = Service(executable_path="/Users/carolinabolnykh/Desktop/winterBreak/dmvBot/dmv/chromedriver")
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
dmv_url = os.getenv("DMV_URL")
page = requests.get(dmv_url)
soup = bs(page.content, 'html.parser')
# print(soup)
# click the 'make an appointment' button
btn = soup.find('button', attrs = {"id":"cmdMakeAppt"})
print(btn.text)

def send_email(subject, body):
    email = os.getenv("EMAIL_USER")
    password = os.getenv("APP_PW")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Login to your Gmail account
    server.login(email, password)
    # Send the email
    server.sendmail(email, recipient_email, msg.as_string())
    # Quit the server
    server.quit()

# chrome webdriver
# set up headless (no gui)
driver = webdriver.Chrome(service=service, options=options)
driver.get(dmv_url)
sleep(3)
createAptBtn = driver.find_element("id", "cmdMakeAppt")
# print(createAptBtn.text)
createAptBtn.click()
sleep(10)
driver.find_element('xpath', '//*[@title="New driver over 18, new N.C. resident, REAL ID"]').find_element('xpath', './..').click()
sleep(3)
claytonOffice = driver.find_element('xpath', '//*[@title="Create an appointment at the Clayton office, located at 1665 Old U.S. 70, Clayton, NC 27520"]')
# only select active units (available for appointment)
parentDiv = claytonOffice.find_element('xpath', './..')
# print(parentDiv.text)
# status = parentDiv.find_elements('xpath', '//*[@class="Active-Unit"]')
if("we don’t have availability at this moment" in parentDiv.text):
    print("no appointments available for the next 3 months")
else:
    send_email("DMVBot", "An appointment has opened at the Clayton dmv! https://skiptheline.ncdot.gov/Webapp/Appointment/Index/a7ade79b-996d-4971-8766-97feb75254de")
driver.quit()