from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import datetime
import time
import os


WAITING_TIME = 2


with open("setting.txt", "r") as file:
    datas = file.readlines()
    ID = datas[0]
    PASSWORD = datas[1]
    SELECT_VALUE1 = datas[2]
    SELECT_VALUE2 = datas[3]

    HORI1 = int(SELECT_VALUE1[0])
    TIME1 = int(SELECT_VALUE1[1:])+1
    HORI2 = int(SELECT_VALUE2[0])
    TIME2 = int(SELECT_VALUE2[1:])+1

    TARGET_DATE = datas[4]


def log(log_message):
    time.sleep(0.5)
    now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"[Log: {now_time}] {log_message}")

    return


def crawling():
    log("open the webdriver")
    nthualb = webdriver.Chrome(ChromeDriverManager().install())
    log("set implicitly waitting time as 10sec")
    nthualb.implicitly_wait(10)
    log("enter the website to login")
    nthualb.get("https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code")

    log("get account_blank")
    account_blank = nthualb.find_element_by_id("id")
    log("send account_blank")
    account_blank.send_keys(ID + PASSWORD)

    log("get captcha_blank")
    captcha_blank = nthualb.find_element_by_id("captcha_code")
    log("click captcha_blank")
    captcha_blank.click()

    # modify to "press any key to continue"
    print("Already login?")
    os.system("pause")

    log("enter the website to last day")
    nthualb.get("https://nthualb.url.tw/reservation/reservation?d=4")

    log("get last_date")
    last_date = nthualb.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[1]/tbody/tr/td[5]/div[2]").text
    log("waiting for target_date")
    while (last_date != TARGET_DATE):
        log("target_date not found")
        log(f"sleep for {WAITING_TIME} secs then refresh")
        time.sleep(WAITING_TIME)
        log("refresh the website")
        nthualb.refresh()
        log("refresh last_date")
        last_date = nthualb.find_element_by_xpath(
            "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[1]/tbody/tr/td[5]/div[2]").text

    log("target_date found!")

    log("select rows")
    select_table = nthualb.find_elements_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[2]/tbody/tr")
    select_table.pop()
    log("select col and select the button")
    place_button1 = select_table[TIME1].find_elements_by_tag_name("td")[HORI1].find_element_by_tag_name("div")
    log("click the button")
    place_button1.click()

    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()
    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()

    log("reget the website")
    nthualb.get("https://nthualb.url.tw/reservation/reservation?d=4")
    log(f"sleep for {WAITING_TIME} secs")
    time.sleep(WAITING_TIME)
    log("select rows")
    select_table = nthualb.find_elements_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[2]/tbody/tr")
    select_table.pop()
    log("select col and select the button")
    place_button2 = select_table[TIME2].find_elements_by_tag_name("td")[HORI2].find_element_by_tag_name("div")
    log("click the button")
    place_button2.click()

    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()
    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()

    for i in range(0, 20):
        log("crawling success!!!!!!")

    log("close the webdriver")
    nthualb.close()

    log("F.I.N.")
    return


if __name__ == '__main__':
    log("start running")
    crawling()
