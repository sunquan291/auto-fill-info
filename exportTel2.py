import codecs
import time
from math import ceil

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# username password
exportFileName = "./data/ep-mengqingwu.txt"
userName = 'xx'
password = 'xxxx'


def goInput():
    browser = webdriver.Chrome()  # Get local session of Chrome
    browser.maximize_window()
    browser.get("https://uxxxxxxadmin/index.html")  # Load page
    wait_driver = WebDriverWait(browser, 3, 0.5)
    browser.find_element(By.XPATH, '//*[@id="sIcon1"]').click()
    # time.sleep(5)
    # 登录
    wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="username"]'))
    # browser.find_element(By.XPATH, '//*[@id="username"]').send_keys('pengyou')
    # browser.find_element(By.XPATH, '//*[@id="username"]').send_keys('xushuqi')
    # browser.find_element(By.XPATH, '//*[@id="username"]').send_keys('kongfanyue')

    browser.find_element(By.XPATH, '//*[@id="username"]').send_keys(userName)
    wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="password"]'))
    # browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('PYwyr19911006')
    # browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('Xushuqi7')
    # browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('Kfanry291123')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)

    wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="loginBtn"]'))
    browser.find_element(By.XPATH, '//*[@id="loginBtn"]').click()
    # time.sleep(5)
    wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="level1_185"]/span'))
    browser.find_element(By.XPATH, '//*[@id="level1_185"]/span').click()
    time.sleep(1)
    browser.find_element(By.XPATH, '// *[ @ id = "level1_76"] / span').click()
    time.sleep(1)
    browser.find_element(By.XPATH, '// *[ @ id = "level2_247"]').click()
    time.sleep(2)
    page = browser.find_element(By.XPATH, '//*[@id="dtGridToolBarContainer"]/span[2]/span').text
    count = page[4:6]
    print("总共有%s条纪录" % (page[4:6]))
    perPageCount = ceil(int(count) / 10)
    print("需要翻页%s次" % perPageCount)
    x = 0
    url = "https://usexxxxxxmin/customerinfo/queryCusPhone.html"
    # data = {"id": 14724433}
    c = browser.get_cookies()
    cookies = {}
    # 获取cookie中的name和value,转化成requests可以使用的形式
    for cookie in c:
        cookies[cookie['name']] = cookie['value']
    # print(cookies)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://usxxxxx/dubbo-customer-admin/index.html'
    }
    # data = {"id": 14724433}
    # session = requests.session()
    # res = session.post(url=url, data=data, headers=headers, cookies=cookies)
    # print(res.text)

    for i in range(perPageCount):
        rows = browser.find_elements(By.CLASS_NAME, 'dlshouwen-grid-row')
        ix = 0
        for row in rows:
            # rows多了一行
            ix += 1
            if ix > 10:
                break
            try:
                # 计数
                x += 1
                tds = row.find_elements_by_tag_name('td')
                # phoneId = tds[3].find_element_by_tag_name('span').get_attribute("onmouseover")[19:-1]
                phoneId = tds[6].find_element_by_tag_name('span').get_attribute("onmouseover")[19:-1]
                # 根据ID查询真实号码
                data = {"id": phoneId}
                session = requests.session()
                res = session.post(url=url, data=data, headers=headers, cookies=cookies)
                # 截取号码
                #print(res.text)
                phone = res.text[9:20]
                print("%d\t%s\t%s\t%s" % (x, tds[3].text, phone, tds[9].text))
                output = tds[3].text + "\t" + phone + "\t" + tds[9].text
                f = codecs.open(exportFileName, "a", "utf-8")
                f.write("%s\n" % output)
            except Exception as e:
                print(x)
        browser.find_element(By.XPATH,
                             '/html/body/div[2]/div[2]/div/div[3]/div[3]/div/div/div[2]/div/div[2]/span[2]/ul/li[8]/a').click()
        time.sleep(1)


if __name__ == '__main__':
    goInput()
