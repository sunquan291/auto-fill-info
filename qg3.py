import string
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# input file
fileName = "./data/121.txt"


userName = 'xxx'
password = 'xxxx'


def calcuateData():
    f = open(fileName, encoding='utf-8')
    i: int = 0
    line = f.readline()
    while line:
        # print(line,end='')
        # 按空格分隔一行字串
        out_str: string = ""
        try:
            out_str = line.split()
            print(out_str[0] + "," + out_str[1] + "," + out_str[2])
        except IndexError as e:
            print("第%d行数据不符合格式要求====>%s" % (i + 1, out_str))
            return -1
        i += 1
        # 循环读取
        line = f.readline()
    f.close()
    print("===数据条目总数【%d】===================================" % i)
    return i


def goInput(result):
    global errorMsg
    print("===数据开始处理【%d】===================================" % result)
    start = time.time()
    browser = webdriver.Chrome()  # Get local session of Chrome
    browser.maximize_window()
    browser.get("https://xxxxmin/index.html")  # Load page
    wait_driver = WebDriverWait(browser, 3, 0.5)
    # browser.find_element_by_xpath('//*[@id="sIcon1"]').click();
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

    f = open(fileName, encoding='utf-8')
    i: int = 0
    # 成功条数
    si: int = 0
    line = f.readline()
    while line:
        i += 1
        print("正在处理[%d/%d]===>%s" % (i, result, line))
        out_str = line.split()
        # browser.find_element(By.XPATH, '//*[@id="searchKeya"]').clear();
        # browser.find_element_by_xpath('//*[@id="searchKeya"]').send_keys(out_str[0]);
        # browser.find_element_by_xpath('//*[@id="btnSearch"]').click();
        # time.sleep(1)
        # time.sleep(1)
        # browser.find_element_by_class_name('dlshouwen-grid-check').click();
        # 这里的btnAdd与确认增加xpath一样，所以增加了一个btnBatchUpdateType等待
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '// *[ @ id = "btnBatchUpdateType"]'))
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="btnAdd"]'))
        browser.find_element(By.XPATH, '//*[@id="btnAdd"]').click()
        # time.sleep(1)
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="repeatSearch"]'))
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="customerName"]'))
        browser.find_element(By.XPATH, '//*[@id="customerName"]').send_keys(out_str[0])
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="customerCompany"]'))
        browser.find_element(By.XPATH, '//*[@id="customerCompany"]').send_keys(out_str[2])
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="titleId"]'))
        browser.find_element(By.XPATH, '//*[@id="titleId"]').send_keys('董事长')
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="customerRegisteredCapital"]'))
        browser.find_element(By.XPATH, '//*[@id="customerRegisteredCapital"]').send_keys('1000-5000万')
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="customerDataSources"]'))
        browser.find_element(By.XPATH, '//*[@id="customerDataSources"]').send_keys('朋友推荐')
        # time.sleep(2)
        # wait_driver.until(lambda temp: temp.find_element(By.XPATH, '//*[@id="btnAdd"]'))
        # 等待返回按钮
        wait_driver.until(lambda temp: temp.find_element(By.XPATH, '// *[ @ id = "btn"]'))
        # browser.find_element(By.XPATH, '// *[ @ id = "btn"]').click()
        # 点击添加按钮
        browser.find_element(By.XPATH, '//*[@id="btnAdd"]').click()
        time.sleep(1)
        # 等待添加成功，如果添加失败，页面会停在该页,下一行则获取不到数据
        try:
            # 防止弹出排重提醒对话框
            wait_driver.until(lambda temp: temp.find_element(By.CLASS_NAME, 'layui-layer-btn0'))
            browser.find_element(By.CLASS_NAME, 'layui-layer-btn0').click()
            si += 1

            # 如果还是原页面，则再次尝试点击添加按钮goto

        except TimeoutException as e:
            time.sleep(1)
            # 尝试再试一次 主要应对一个资产不达标的提示框
            try:
                browser.find_element(By.XPATH, '//*[@id="btnAdd"]').click()
                time.sleep(2)
                # errorMsg = browser.find_element(By.CSS_SELECTOR,
                #                                 "[class='layui-layer layui-layer-dialog layui-layer-border layui-layer-msg']").get_attribute(
                #     "innerHTML")
                # errorMsg = browser.find_element(By.CSS_SELECTOR,
                #                                 "[class='layui-layer-content layui-layer-padding']").text
                try:
                    errorMsg = browser.find_element(By.CSS_SELECTOR,
                                                    "[class='layui-layer layui-layer-dialog layui-layer-border layui-layer-msg']").text
                except  NoSuchElementException as e:
                    errorMsg = "unknown"
                time.sleep(1)
                wait_driver.until(lambda temp: temp.find_element(By.CLASS_NAME, 'layui-layer-btn0'))
                browser.find_element(By.CLASS_NAME, 'layui-layer-btn0').click()
                si += 1
            except TimeoutException as e:
                print("处理失败[%d/%d],原因:%s===>\n%s" % (i, result, errorMsg, line))
                browser.find_element(By.XPATH, '// *[ @ id = "btn"]').click()

        line = f.readline()
        # browser.find_element(By.XPATH, '//*[@id="level1_185"]/span').click()
    f.close()
    browser.quit()
    end = time.time()
    print("===数据处理成功率及耗时【%d/%d】【%.2f秒】===================================" % (
        si, result, (end - start)))


if __name__ == '__main__':

    result = calcuateData()
    if result != -1:
        goInput(result)
# browser.find_element_by_xpath('*[@id="level1_185"]').click();
