import os
import time
from helpers import get_creds, send_sms
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def usa_visa_checker():
    messages_to_be_sent = {}
    no_appointment_id = "consulate_date_time_not_available"
    email, password, visa_url = get_creds()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(visa_url)
    # Form fields
    user_email = driver.find_element(By.XPATH, '//*[@id="user_email"]')
    user_password = driver.find_element(By.XPATH, '//*[@id="user_password"]')
    login_button = driver.find_element(By.XPATH, '//*[@id="new_user"]/p[1]/input')
    privacy_check = driver.find_element(
        By.XPATH, '//*[@id="new_user"]/div[3]/label/div'
    )
    # Clear input fields
    user_email.clear()
    user_password.clear()
    # Input to credential fields and logging in
    user_email.send_keys(email)
    user_password.send_keys(password)
    privacy_check.click()
    login_button.click()
    time.sleep(5)
    # Check for the next available dates
    continue_button = driver.find_element(By.LINK_TEXT, "Continue")
    continue_button.click()
    reschedule_button = driver.find_elements(By.LINK_TEXT, "Reschedule Appointment")[0]
    reschedule_button.click()
    time.sleep(3)
    reschedule_button = driver.find_elements(By.LINK_TEXT, "Reschedule Appointment")[1]
    reschedule_button.click()
    time.sleep(3)
    # Check if slots are open in Montreal region if not continue to Quebec City, if not, then to Toronto
    city_field = driver.find_element(
        By.XPATH, '//*[@id="appointments_consulate_appointment_facility_id"]'
    )
    time.sleep(3)
    # Check for slots in Montreal, if not, then try Quebec City
    city_field.send_keys("Montreal")
    time.sleep(2)
    error_notice = driver.find_element(By.ID, no_appointment_id)
    if not error_notice:
        messages_to_be_sent.update(
            {
                "Montreal": "YAAAYYYY! New slots have opened up in Montreal. OPEN THE WEBSITE NOW AND RESCHEDULE"
            }
        )
    else:
        messages_to_be_sent.update({"Montreal": "No new slots available in Montreal"})
    time.sleep(2)
    # Check for slots in Quebec City, if not, then try Quebec City
    city_field.send_keys("Quebec City")
    time.sleep(2)
    error_notice = driver.find_element(By.ID, no_appointment_id)
    if not error_notice:
        messages_to_be_sent.update(
            {
                "Quebec City": "YAAAYYYY! New slots have opened up in Quebec City. OPEN THE WEBSITE NOW AND RESCHEDULE"
            }
        )
    else:
        messages_to_be_sent.update(
            {"Quebec City": "No new slots available in Quebec City"}
        )
    # Check for slots in Toronto, if not available, close it
    city_field.send_keys("Toronto")
    time.sleep(2)
    driver.find_element(By.ID, no_appointment_id)
    if not error_notice:
        messages_to_be_sent.update({"Toronto": "Slots in Toronto have been closed"})
    else:
        next_counter = 0
        flag = True
        date_dropper = driver.find_element(
            By.XPATH, '//*[@id="appointments_consulate_appointment_date_input"]'
        )
        date_dropper.click()
        time.sleep(2)
        messages_to_be_sent.update({"Toronto": "No new dates available for Toronto :("})
        while next_counter <= 15 and flag:
            next_button = driver.find_element(
                By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a'
            )
            time.sleep(1)
            date_elements = driver.find_elements(By.TAG_NAME, "td")
            data_handler_attributes = [
                element.get_attribute("data-handler") for element in date_elements
            ]
            if any(data_handler_attributes):
                print(f"Executing this block. Next counter : {next_counter}")
                messages_to_be_sent.update(
                    {
                        "Toronto": "YAAYY!! An Earlier date is available for Toronto. HURRY UP!"
                    }
                )
                flag = False
                break
            else:
                next_counter += 1
                print(f"Executing that block. Next counter : {next_counter}")
                next_button.click()
                time.sleep(1)

    print(f"Messages to be sent : {messages_to_be_sent}")
    time.sleep(3)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print("running the program ....")
    usa_visa_checker()
