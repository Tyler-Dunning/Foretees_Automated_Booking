from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from functools import partial

import schedule

import time


def book_tee_time_automated(month, day, year, desired_time):
    driver = webdriver.Chrome()

    driver.get("https://web.foretees.com/v5/servlet/LoginPrompt?cn=valleyhicc")
    driver.implicitly_wait(5) 

    username = driver.find_element(By.NAME, "user_name")
    password = driver.find_element(By.NAME, "password")

    username.send_keys("190") # INPUT YOUR MEMBER NUMBER
    password.send_keys("Dunning") # INPUT YOUR LAST NAME

    sign_in_button = driver.find_element(By.CLASS_NAME, "button-primary")
    sign_in_button.click()
    
    wait = WebDriverWait(driver, 10)
    tee_times_menu = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Tee Times']")))

    actions = ActionChains(driver)
    actions.move_to_element(tee_times_menu).perform()

    submenu_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Make, Change, or View Tee Times']")))

    submenu_item.click()

    date_button = driver.find_element(By.XPATH, f"//td[@title='Tee Times Available' and @data-month='{month}' and @data-year='{year}']//a[text()='{day}']")
    date_button.click()
    
    time_button = driver.find_element(By.XPATH, f"(//a[contains(text(), '{desired_time}')])[1]")
    time_button.click()

    submit_button = driver.find_element(By.CLASS_NAME, "submit_request_button")
    submit_button.click()
  
job = partial(book_tee_time_automated, 5, 29, 2025, "6:00 PM") # CHANGE THESE VALUES IN SAME FORMAT --Input the tee time that you want: (month, day, year, time)

schedule.every().day.at("07:00").do(job) 

while True:
    schedule.run_pending()
    time.sleep(1)