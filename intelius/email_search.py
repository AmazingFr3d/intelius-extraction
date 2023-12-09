from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep

import data
import intelius

driver = intelius.driver
delay = intelius.delay


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

            data.to_csv(new_info, "phone", "intelius")

            count = 0
        else:
            count += 1
    data.to_csv(new_info, "phone", "intelius")

    return new_info
