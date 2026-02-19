"""
Badminton/Tennis Court Booking Automation Tool

Usage:
    # Single user mode (compatible with original multi_jinze.py)
    python booking.py --usr "姓名" --phone "手机号" --court 场地编号 --time 时间段序号

    # Batch mode (read from config.json)
    python booking.py --batch
"""

import argparse
import datetime
import random
import threading
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_parser():
    parser = argparse.ArgumentParser('Badminton/Tennis Booking')
    parser.add_argument('--usr', type=str, default='于洋', help='User name')
    parser.add_argument('--phone', type=str, default='18217505025', help='Phone number')
    parser.add_argument('--num', type=int, default=6, help='Number of people')
    parser.add_argument('--type', type=str, default='羽毛球', help='Booking type')
    parser.add_argument('--court', type=int, default=1, help='Court number')
    parser.add_argument('--date', type=int, default=3, help='Days from today')
    parser.add_argument('--time', type=int, default=1, help='Time slot index')
    parser.add_argument('--batch', action='store_true', help='Run batch mode from config.json')
    parser.add_argument('--config', type=str, default='config.json', help='Config file path for batch mode')
    return parser


# Settings
CHROME_DRIVER_PATH = "C:/chromedriver-win64/chromedriver.exe"
FORM_URL = "https://jinshuju.com/f/vcswPJ"
START_TIME = '09:00:00.175'  # Booking start time


def pause(driver, run_time):
    """Wait until specified time before executing"""
    run_time_obj = datetime.datetime.strptime(run_time, '%H:%M:%S.%f')
    while True:
        now_str = datetime.datetime.now().strftime('%H:%M:%S.%f')
        now = datetime.datetime.strptime(now_str, '%H:%M:%S.%f')
        if now > run_time_obj:
            print('Time to start!')
            driver.refresh()
            break
        elif now + datetime.timedelta(minutes=10) < run_time_obj:
            print('Waiting for 10 minutes...')
            time.sleep(600 - random.randint(0, 60))
            driver.refresh()
        elif now + datetime.timedelta(minutes=5) < run_time_obj:
            print('Waiting for 5 minutes...')
            time.sleep(300)
            driver.refresh()
        else:
            time.sleep(0.7)


def find_element(driver, type, path, click=True):
    """Find element, click if needed"""
    while True:
        try:
            ele = driver.find_element(type, path)
            if click:
                ele.click()
            return ele
        except Exception:
            time.sleep(0.2)
            continue


def select_date(driver, target_date):
    """Select the target date on the form"""
    xpath = f"//div[@title='{target_date}']"
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except:
            driver.execute_script("arguments[0].click();", element)
        print(f"成功选中日期: {element.get_attribute('title')}")
    except Exception as e:
        print(f"无法选中日期 [{target_date}]，错误原因: {e}")
        driver.get_screenshot_as_file("error.png")


def fill_in_form(driver, usr, phone, num, booking_type, court, date_offset, time_slot):
    """Fill in the booking form and submit"""
    target_date = (datetime.datetime.now() + datetime.timedelta(days=date_offset)).strftime('%Y年%#m月%d日')
    print(f'预约项目：{booking_type}，场地：{court}，日期：{target_date}')

    # Wait until the specified time
    pause(driver, START_TIME)

    # Form data
    data = [usr, phone, num, booking_type]
    names = ['姓名', '手机', '同行人数', '预约项目']
    items = [None, None, None, None]

    driver.get(FORM_URL)

    # Wait for form to load
    while True:
        try:
            elements = driver.find_elements(By.XPATH, "//div[@data-api-code]")
            if not elements:
                print("未找到元素，刷新页面...")
                driver.refresh()
                time.sleep(0.3)
                continue
            break
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(f"出错了：{e}，刷新页面重试...")
            driver.refresh()
            time.sleep(1)

    # Map form fields to their labels
    for ele in elements:
        label = ele.find_element(By.XPATH, ".//label[@title]//span")
        label = label.text
        for i in range(len(names)):
            if names[i] in label:
                items[i] = ele

    # Fill in basic info
    for i in [0, 1, 2]:
        ele = items[i].find_element(By.XPATH, ".//input")
        ele.send_keys(data[i])
    print('已填写姓名、手机、同行人数')

    # Select booking type
    elements = items[3].find_elements(By.XPATH, ".//div[@data-value]")
    for ele in elements:
        e = ele.find_element(By.XPATH, ".//input[@type='radio']")
        label = ele.find_element(By.XPATH, ".//span[@class='other-choice-option-name']")
        if label.text != data[3]:
            continue
        if e.is_selected():
            pass
        else:
            e.click()
        break
    print(f'已选择项目：{data[3]}')

    # Select court
    elements = find_element(driver, By.XPATH, "//div[@class='reservation-field']", click=False)
    elements = elements.find_elements(By.XPATH, "./div")
    ele = elements[court - 1]
    ele = ele.find_element(By.XPATH, ".//a[@class='reservation-item-option-bar__right']")
    ele.click()
    print(f'已选择场地：{court}')

    # Select date
    select_date(driver, target_date)

    # Select time
    elements = driver.find_elements(By.XPATH, "//div[@class='with-calendar-time-range-list']//a")
    ele = elements[time_slot - 1]
    ele.click()
    print(f'已选择时间：{time_slot}')

    # Submit
    ele = driver.find_element(By.XPATH, "//div[@class='published-form__footer center']//button")
    ele.click()
    print("----------------抢场成功---------------------------------")
    print(f'场地：{court}  时间：{time_slot+6}--{time_slot+7}  预约人：{usr}')
    print("---------------------------------------------------------------")


def run_booking(usr, phone, num, booking_type, court, date_offset, time_slot):
    """Run a single booking in a thread"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        fill_in_form(driver, usr, phone, num, booking_type, court, date_offset, time_slot)
    except Exception as e:
        print(f"Booking failed for {usr}: {e}")


def run_single(args):
    """Run single user booking"""
    print(f"\n=== Starting single booking for {args.usr} ===\n")
    run_booking(
        usr=args.usr,
        phone=args.phone,
        num=args.num,
        booking_type=args.type,
        court=args.court,
        date_offset=args.date,
        time_slot=args.time
    )


def run_batch(args):
    """Run batch bookings from config file"""
    config_path = args.config

    if not os.path.exists(config_path):
        print(f"Error: Config file '{config_path}' not found!")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    users = config.get('users', [])
    common = config.get('common', {})

    if not users:
        print("No users found in config!")
        return

    # Default values from common config
    default_num = common.get('num', 6)
    default_type = common.get('type', '羽毛球')
    default_date = common.get('date', 3)

    print(f"\n=== Starting batch booking for {len(users)} users ===")
    print(f"Common config: num={default_num}, type={default_type}, date={default_date}\n")

    threads = []
    for user in users:
        usr = user.get('name', '')
        phone = user.get('phone', '')
        court = user.get('court', 1)
        time_slot = user.get('time', 1)
        num = user.get('num', default_num)
        booking_type = user.get('type', default_type)
        date_offset = user.get('date', default_date)

        print(f"Queuing: {usr} - Court {court}, Time {time_slot}")

        thread = threading.Thread(
            target=run_booking,
            args=(usr, phone, num, booking_type, court, date_offset, time_slot)
        )
        threads.append(thread)
        thread.start()

        # Small delay between starting threads
        time.sleep(0.5)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\n=== All bookings completed ===")


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.batch:
        run_batch(args)
    else:
        run_single(args)


if __name__ == '__main__':
    main()
