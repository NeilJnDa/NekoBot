
# encoding = utf-8
import selenium
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
import sys

# 保存日志文件类
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

# 创建文件夹
def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print
        path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print
        path + ' 目录已存在'
        return False




# 用户名密码
config = [['213162797', '14789ldj'], ['213170769', '8eeeeeeee'], ['213160539','woshituzi.,'], ['213160533', 'Cengong1996']]


def open_login_website():
    retry_times = 4
    while retry_times > 0:
        try:
            retry_times -= 1
            # 打开登录页
            print('打开办事大厅...')
            driver.get("http://ehall.seu.edu.cn/new/index.html")
            time.sleep(2)
            print('登录...')
            driver.find_element_by_xpath("//*[@id='ampHasNoLogin']").click()
            time.sleep(2)
            break
        except:
            print('打开登录页面出错，重试...')
            if retry_times == 2:
                driver.refresh()
            time.sleep(3)


def input_user_info(username, password):
    retry_times = 4
    while retry_times > 0:
        try:
            retry_times -= 1
            print('用户名...')
            driver.find_element_by_id("username").send_keys(username)
            time.sleep(1)
            print('密码...')
            driver.find_element_by_id("password").send_keys(password)
            time.sleep(1)
            print('提交登录...')
            driver.find_element_by_xpath("//*[@id='xsfw']").click()
            time.sleep(1)
            break
        except:
            print('输入用户名密码出错，重试...')
            if retry_times == 2:
                driver.refresh()
            time.sleep(3)


def switch_to_new():
    retry_times = 4
    while retry_times > 0:
        try:
            retry_times -= 1
            n = driver.window_handles  # 获取当前页句柄
            print('切换窗口...')
            driver.switch_to.window(n[-1])  # 切换到新的网页窗口
            time.sleep(2)
            break
        except:
            print('切换窗口出错，重试...')
            if retry_times == 2:
                driver.refresh()
            time.sleep(3)
        pass


def enter_system():
    print('寻找填报系统入口...')
    retry_times = 4
    time.sleep(3)
    while retry_times > 0:
        try:
            retry_times -= 1
            element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath("//*[@id='app']/div[2]/div[2]/div/div/div/div/div[3]/div[2]/a"))
            element.click()
            #driver.find_element_by_xpath("//*[@id='app']/div[2]/div[2]/div/div/div/div/div[3]/div[2]/a").click()
            time.sleep(4)
        except:
            print('寻找填报系统入口出错，重试...')
            if retry_times == 2:
                driver.refresh()
            time.sleep(3)
            pass


def new_case():
    retry_times = 4
    while retry_times > 0:
        try:
            retry_times -= 1
            print('新增...')
            driver.find_element_by_css_selector(
                "body > main > article > section > div.bh-mb-16 > div.bh-btn.bh-btn-primary").click()
            time.sleep(3)
            break
        except:
            print('新增出错，重试...')
            if retry_times == 2:
                driver.refresh()
            time.sleep(3)
            pass


def check_and_upload():
    retry_times = 4
    while retry_times > 0:
        try:
            retry_times -= 1
            time.sleep(5)
            print('保存...')
            driver.find_element_by_xpath("//*[@id='save' and @class='bh-btn bh-btn-primary']").click()
            time.sleep(3)
            print('确认...')
            driver.find_element_by_xpath("//a[text()='确认' and @class ='bh-dialog-btn bh-bg-primary bh-color-primary-5']").click()
            break
        except:
            print("出错重试")
            if retry_times == 2:
                driver.refresh()


def screen_shot():
    try:
        # picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        picture_url = driver.get_screenshot_as_file('F:\\Selenium\\Log\\' + picture_time + '\\' + user[0] + '.png')
        print("截图:%s" % picture_url)
    except BaseException as msg:
        print(msg)


def if_filled():
    flag = True
    time.sleep(3)
    try:
        driver.find_element_by_class_name("content")
        print('已填报')
        return flag
    except:
        print('未填报')
        flag = False
        return flag


picture_time = time.strftime("%m-%d %H.%M", time.localtime(time.time()))
mkpath = "F:\\Selenium\\Log\\" + picture_time
mkdir(mkpath)
sys.stdout = Logger('F:\\Selenium\\Log\\' + picture_time + '\\Log.txt')  # 保存Log
for user in config:
    try:
        driver = webdriver.Chrome(executable_path="F:\\Selenium\chromedriver")
        print('user:'+user[0])
        # 通过executable_path参数指定Chrome驱动文件所在位置
        open_login_website()
        input_user_info(user[0], user[1])
        enter_system()
        switch_to_new()
        new_case()
        if if_filled():
            screen_shot()
            # driver.quit()
            continue
        check_and_upload()
        screen_shot()
        # driver.quit()
    except Exception as e:
        print(user[0] + "出错")
        screen_shot()
        print(e)
        pass


# 退出浏览器
