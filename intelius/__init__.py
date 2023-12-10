from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os
from pathlib import Path
import pandas as pd

from intelius import creds

delay = 15
username = creds.username
password = creds.password
url = "https://www.intelius.com/dashboard"
path = os.getcwd()
Path(f"{path}/data/UserData").mkdir(parents=True, exist_ok=True)

if not os.path.isfile("bank.csv"):
    headers = [
        {
            'First Name': '',
            'Last Name': '',
            'Email': '',
            'Job Title': '',
            'Street Address': '',
        }
    ]
    df = pd.DataFrame(headers)
    df.to_csv("bank.csv", index=False)

browser_profile = webdriver.ChromeOptions()
browser_profile.add_argument('--profile-directory=Default')
service = Service(ChromeDriverManager().install())
browser_profile.add_argument(f'--user-data-dir={path}/data/UserData')
# browser_profile.add_argument(f'--headless')
driver = webdriver.Chrome(options=browser_profile, service=service)

driver.get(url)
sleep(10)


def login():
    try:
        driver.find_element(By.NAME, "email").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(15)
    except NoSuchElementException:
        pass
