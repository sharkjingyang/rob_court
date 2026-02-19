from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time, datetime, random
import argparse

parser = argparse.ArgumentParser('Badminton_Tennis')
parser.add_argument('--usr', type=str, default='于洋')
parser.add_argument('--phone', type=str, default='18217505025')
parser.add_argument('--num', type=int, default=6)
parser.add_argument('--type', type=str, default='羽毛球')
parser.add_argument('--court', type=int, default=1)
parser.add_argument('--date', type=int, default=3) # 从今天后开始算第n天
parser.add_argument('--time', type=int, default=1)

args = parser.parse_args()

# 设定代码开始运行时间
def pause(driver, run_time):
    run_time = datetime.datetime.strptime(run_time, '%H:%M:%S.%f')
    while True:
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')
        now = datetime.datetime.strptime(now, '%H:%M:%S.%f')
        if now > run_time:
            print('Time to start!')
            driver.refresh()
            break
        elif now + datetime.timedelta(minutes=10) < run_time:
            print('Waiting for 10 minutes...')
            time.sleep(600 - random.randint(0, 60))
            driver.refresh()
        elif now + datetime.timedelta(minutes=5) < run_time:
            print('Waiting for 5 minutes...')
            time.sleep(300)
            driver.refresh()
        else:
            time.sleep(0.7)

# 查找（单个）网页元素，每0.2s查找一次，找到后自动点击（可设置不点击）
def find_element(driver, type, path, click=True):
    while True:
        try:
            ele = driver.find_element(type, path)
            if click:
                ele.click()
            return ele
        except Exception:
            time.sleep(0.2)
            continue

# 填写表单信息
def fill_in_form(driver, args):
    # 设定预约日期
    target_date = (datetime.datetime.now() + datetime.timedelta(days=args.date)).strftime('%Y年%#m月%d日')
    print(f'预约项目：{args.type}，场地：{args.court}，日期：{target_date}')
    
    # ！！！请按需注释
    pause(driver, '09:00:00.175')
    
    # 提取要填写的表单元素
    data = [args.usr, args.phone, args.num, args.type]
    names = ['姓名', '手机', '同行人数', '预约项目']
    items = [None, None, None, None]

    driver.get("https://jinshuju.com/f/vcswPJ")

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


    # 识别每块输入名称，如果确定与 names 顺序一致，可以直接令 items = elements
    for ele in elements:
        label = ele.find_element(By.XPATH, ".//label[@title]//span")
        label = label.text
        for i in range(len(names)):
            if names[i] in label:
                items[i] = ele

    # 输入 姓名、手机、同行人数
    for i in [0, 1, 2]:
        ele = items[i].find_element(By.XPATH, ".//input")
        ele.send_keys(data[i])
    print('已填写姓名、手机、同行人数')
    
    # 选择项目
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

    # 查找场地，点击预约
    elements = find_element(driver, By.XPATH, "//div[@class='reservation-field']", click=False)
    elements = elements.find_elements(By.XPATH, "./div")
    ele = elements[args.court - 1]
    ele = ele.find_element(By.XPATH, ".//a[@class='reservation-item-option-bar__right']")
    ele.click()
    print(f'已选择场地：{args.court}')

    # 选择日期

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC



    # element = find_element(driver, By.XPATH, f"//div[@title='{target_date}']", click=False)
    # time.sleep(1) # 等待元素可点击，发现未点击日期可尝试调整该数值
    # driver.execute_script("arguments[0].click();", element)
    # # element.click()
    # # 测试日期是否正确
    # date = element.get_attribute('title')
    # print(f'已选择日期：{date}')


    def select_date(driver, target_date):
        xpath = f"//div[@title='{target_date}']"
        try:
            # 1. 等待元素存在且可点击
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # 2. 滚动到该元素（防止某些UI框架拦截）
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            # 3. 尝试直接点击，如果不成功则使用 JS 点击
            try:
                element.click()
            except:
                driver.execute_script("arguments[0].click();", element)
            print(f"成功选中日期: {element.get_attribute('title')}")
        except Exception as e:
            print(f"无法选中日期 [{target_date}]，错误原因: {e}")
            # 这里可以截图调试
            driver.get_screenshot_as_file("error.png")
    
    select_date(driver, target_date)


    # 选择时间
    elements = driver.find_elements(By.XPATH, "//div[@class='with-calendar-time-range-list']//a")
    ele = elements[args.time - 1]
    ele.click()
    print(f'已选择时间：{args.time}')

    # # 测试时间是否正确
    # ele = ele.find_element(By.XPATH, "./div")
    # timerange = ele.text
    # print(timerange)

    # 提交按钮
    ele = driver.find_element(By.XPATH, "//div[@class='published-form__footer center']//button")

    # ！！！请按需注释
    # print('当前未提交，请去除代码注释')
    ele.click()
    print("----------------抢场成功---------------------------------")
    print(f'场地：{args.court}  时间：{args.time+6}--{args.time+7}  预约人：{args.usr} ')
    print("---------------------------------------------------------------")



def main():
    chrome_driver_path = "C:/chromedriver-win64/chromedriver.exe" # 当driver（驱动）路径出错时手动设置
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=options) # 当server（驱动）路径出错时手动设置
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    fill_in_form(driver, args)

if __name__ == '__main__':
    main()
