from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import re
from data import data

import intelius

driver = intelius.driver
delay = intelius.delay


# ---------------------------------------------------------------------------------------------------------
# Email search

def single_email(email: str):
    intelius.login()

    if driver.find_element(By.CLASS_NAME, "search-form"):
        driver.find_element(By.XPATH,
                            "(//li[@class='ui-tab-nav-item' or @class='ui-tab-nav-item active-item'])[3]").click()

        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(delay)

        try:
            driver.find_element(By.CLASS_NAME, "button-link").click()
            sleep(delay)

            try:
                phone_no = driver.find_element(By.CLASS_NAME, "phone-number").text
            except NoSuchElementException:
                phone_no = "N/A"

        except NoSuchElementException:
            phone_no = "N/A"

    return phone_no


def multi_emails(emails):
    count = 0
    new_info = []
    for index, row in emails.iterrows():

        driver.find_element(By.CLASS_NAME, "logo").click()
        sleep(10)
        phone_no = single_email(row['email'])
        new_info.append(
            {
                'Record ID': row['id'],
                'First Name': row[''],
                'Last Name': row['lnamfnamee'],
                'Email': row['email'],
                'Phone Number': phone_no
            }
        )
        if count == 10:

            data.to_csv(new_info, "phone")

            count = 0
        else:
            count += 1
    data.to_csv(new_info, "phone")

    return new_info


# -------------------------------------------------------------------------------------------------------------
# Phone number search

def single_phone(phone: str):
    login()
    email = "N/A"
    try:
        driver.find_element(By.CLASS_NAME, "search-form")
        driver.find_element(By.XPATH,
                            "(//li[@class='ui-tab-nav-item' or @class='ui-tab-nav-item active-item'])[2]").click()
        if phone_val(phone):
            driver.find_element(By.NAME, "phone").send_keys(phone)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            sleep(delay)

            try:
                driver.find_element(By.CLASS_NAME, "button-link").click()
                sleep(delay)

                try:
                    email = driver.find_element(By.XPATH, "//p[@class='ui-text small']").text
                except NoSuchElementException:
                    email = "N/A"

            except NoSuchElementException:
                email = "N/A"
    except NoSuchElementException:
        pass

    return email


def multi_phone(phones):
    count = 0
    new_info = []
    for index, row in phones.iterrows():

        driver.find_element(By.CLASS_NAME, "logo").click()
        sleep(10)
        email = single_phone(row['phone'])

        new_info.append(
            {
                'Record ID': row['id'],
                'First Name': row['fname'],
                'Last Name': row['lname'],
                'Email': email,
                'Phone Number': row['phone']

            }
        )
        print(new_info)
        if count == 10:
            data.to_csv(new_info, "email")
            count = 0
        else:
            count += 1

    data.to_csv(new_info, "email")

    return new_info


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Name search

def single_name(name: str):
    login()
    email = "N/A"
    email_list = []
    splited = name.split(" ")
    try:
        driver.find_element(By.CLASS_NAME, "search-form")
        driver.find_element(By.XPATH,
                            "(//li[@class='ui-tab-nav-item' or @class='ui-tab-nav-item active-item'])[1]").click()

        driver.find_element(By.NAME, "firstName").send_keys(splited[0])
        driver.find_element(By.NAME, "lastName").send_keys(splited[1])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(delay)

        try:
            driver.find_element(By.CLASS_NAME, "button-link").click()
            sleep(delay)

            try:
                emails = driver.find_elements(By.XPATH, "//p[@class='ui-text small']")
                email_list = [x.text for x in emails]
                # phone = driver.find_elements(By.XPATH, "//span[@class='phone-number']").text
            except NoSuchElementException:
                email = ""

        except NoSuchElementException:
            email = ""
    except NoSuchElementException:
        pass

    return email_list


def multi_name(names):
    count = 0
    new_info = []
    for index, row in names.iterrows():

        fullname = row['name']
        split_name = fullname.split(" ")
        firstname = split_name[0]
        lastname = split_name[1]

        driver.find_element(By.CLASS_NAME, "logo").click()
        sleep(10)
        email = single_name(fullname)

        new_info.append(
            {
                'First Name': firstname,
                'Last Name': lastname,
                'Email': email,
                'Phone Number': row['phone']

            }
        )
        print(new_info)
        if count == 10:
            data.to_csv(new_info, "email")
            count = 0
        else:
            count += 1

    data.to_csv(new_info, "email")

    return new_info
