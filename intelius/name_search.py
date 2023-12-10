import datetime as dt
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


import intelius
import data
import data_mgt


delay = 15
driver = intelius.driver


def single_name(name: str):
    intelius.login()
    email_list = ''
    address = ''
    job_title = ''
    split = name.split(" ")
    try:
        driver.find_element(By.CLASS_NAME, "search-form")
        driver.find_element(By.XPATH,
                            "(//li[@class='ui-tab-nav-item' or @class='ui-tab-nav-item active-item'])[1]").click()

        driver.find_element(By.NAME, "firstName").send_keys(split[0])
        driver.find_element(By.NAME, "lastName").send_keys(split[1])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(delay)

        # Age filter
        age = driver.find_element(By.XPATH, "//div[contains(@class, 'age')]/h3/text()").text
        if age > 65:
            pass
        else:
            try:
                driver.find_element(By.CLASS_NAME, "button-link").click()
                sleep(delay)
                try:
                    emails = driver.find_elements(By.XPATH,
                                                  "//div[@class='record-subsection emails-subsection']//div["
                                                  "@class='section-table-header']/h5")
                    email_list = [x.text.lower() for x in emails]

                    address = driver.find_element(By.XPATH,
                                                  "//div[@class='location-subsection-item']//p[@class='ui-text medium']").text

                    job_title = driver.find_element(By.XPATH, "(//div[contains(@class, 'job-section')]//h2[@class='job-title'])[1]/text()").text


                except NoSuchElementException:
                    email_list = ''
                    address = ''
                    job_title = ''

            except NoSuchElementException:
                email_list = ''
                address = ''
                job_title = ''
    except NoSuchElementException:
        pass

    contact_list = [email_list, address, job_title]

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
                'Job Title': contact[2],
                'Street_Address': contact[1]

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
