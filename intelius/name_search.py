from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import datetime as dt

import intelius
from intelius import data, data_mgt

delay = 15
driver = intelius.driver


def single_name(name: str):
    intelius.login()
    email_list = ''
    address = ''
    phone_list = ''
    split = name.split(" ")
    try:
        driver.find_element(By.CLASS_NAME, "search-form")
        driver.find_element(By.XPATH,
                            "(//li[@class='ui-tab-nav-item' or @class='ui-tab-nav-item active-item'])[1]").click()

        driver.find_element(By.NAME, "firstName").send_keys(split[0])
        driver.find_element(By.NAME, "lastName").send_keys(split[1])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(delay)

        try:
            driver.find_element(By.CLASS_NAME, "button-link").click()
            sleep(delay)

            try:
                emails = driver.find_elements(By.XPATH,
                                              "//div[@class='record-subsection emails-subsection']//div[@class='section-table-header']/h5")
                email_list = [x.text.lower() for x in emails]

                phones = driver.find_elements(By.XPATH, "//span[@class='phone-number']")
                phone_list = [x.text for x in phones]

                address = driver.find_element(By.XPATH,
                                              "//div[@class='location-subsection-item']//p[@class='ui-text medium']").text

            except NoSuchElementException:
                email_list = ''
                phone_list = ''
                address = ''

        except NoSuchElementException:
            email_list = ''
            phone_list = ''
            address = ''
    except NoSuchElementException:
        pass

    contact_list = [email_list, phone_list, address]

    return contact_list


def multi_name(names):
    count = 0
    saves = 0
    new_info = []
    for index, row in names.iterrows():

        fullname = row['name']
        split_name = fullname.split(" ")
        firstname = split_name[0]
        lastname = split_name[1]

        driver.find_element(By.CLASS_NAME, "logo").click()
        sleep(delay)
        contact = single_name(fullname)

        new_info.append(
            {
                'First_Name': firstname,
                'Last_Name': lastname,
                'Email': contact[0],
                'Phone_Number': contact[1],
                'Street_Address': contact[2]

            }
        )
        sleep(delay)

        if count == 9:
            data.to_csv(new_info, "contact")
            names.drop(names.index[:10], inplace=True)
            names.to_csv("input.csv", index=False)
            count = 0
            saves += 1

            data_mgt.clean_up()
        else:
            count += 1

        try:
            last_id = names.iloc[index + 1]
        except IndexError:
            data.to_csv(new_info, "contact")
            names.drop(names.index[:10], inplace=True)
            names.to_csv("input.csv", index=False)
            count = 0
            saves += 1

            data_mgt.clean_up()

        date_time = dt.datetime.now()
        d = date_time.strftime("%d-%m-%y %H:%M")
        dl = d.split()

        print(f"{count} | {firstname} {lastname}")
        print(f"Saves = {saves}")
        print(f'Date: {dl[0]} | Time : {dl[1]}\n')

    return new_info
