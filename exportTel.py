import codecs
import time
from math import ceil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# export file
# exportFileName = "./data/ep.txt"


exportFileName = "./data/ep-xujingping.txt"
userName = 'xx'
password = '1xq'


def goInput():
    browser = webdriver.Chrome()  # Get local session of Chrome
    browser.maximize_window()
    browser.get("https://xxxxxxxxx/index.html")  # Load page
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
    time.sleep(2)
    # browser.find_element(By.XPATH, '// *[ @ id = "level1_76"] / span').click()
    # browser.find_element(By.XPATH, '// *[ @ id = "level2_247"]').click()
    time.sleep(1)
    page = browser.find_element(By.XPATH, '//*[@id="dtGridToolBarContainer"]/span[2]/span').text
    count = page[4:8]
    print("总共有%s条纪录" % (page[4:8]))
    perPageCount = ceil(int(count) / 10)
    print("需要翻页%s次" % perPageCount)
    x = 0

    for i in range(perPageCount):
        for j in range(20):
            try:
                num = str(j)
                js = "document.getElementsByClassName(\"tip\")[" + num + "].style.display='block';"
                browser.execute_script(js)
            except Exception as e:
                print(j)

        time.sleep(1)
        rows = browser.find_elements(By.CLASS_NAME, 'dlshouwen-grid-row')
        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            x += 1

            print("%d\t%s\t%s\t%s\t%s" % (
            x, tds[3].text, tds[5].text, tds[6].find_elements_by_tag_name('span')[1].text, tds[8].text))
            output = tds[3].text + "\t" + tds[5].text + "\t" + tds[6].find_elements_by_tag_name('span')[1].text + "\t" + \
                     tds[8].text
            f = codecs.open(exportFileName, "a", "utf-8")
            # with open(exportFileName, "w") as f:
            f.write("%s\n" % output)
        browser.find_element(By.XPATH,
                             '/html/body/div[2]/div[2]/div/div[3]/div[3]/div/div/div[2]/div/div[2]/span[2]/ul/li[8]/a').click()
        time.sleep(1)


if __name__ == '__main__':
    goInput()
