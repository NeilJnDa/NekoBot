# encoding = utf-8
import selenium
from selenium import webdriver
import time
from selenium.webdriver.support.wait import WebDriverWait
import sys
import queue
import Neko_add
from Neko_add import Status
import random


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


def open_login_website(driver):
    retry_times = 2
    while retry_times > 0:
        try:
            retry_times -= 1
            # 打开登录页
            print('打开办事大厅...')
            driver.get("http://ehall.seu.edu.cn/new/index.html")
            print('登录...')
            element = WebDriverWait(driver, 10).until(lambda x:
                                                      driver.find_element_by_xpath("//*[@id='ampHasNoLogin']"))
            time.sleep(1)
            element.click()
            break
        except:
            if retry_times == 0:
                return False
            print('打开登录页面出错，重试...')
            driver.refresh()
    return True


def input_user_info(driver, username, password):
    retry_times = 2
    while retry_times > 0:
        try:
            retry_times -= 1
            print('用户名...')
            element = WebDriverWait(driver, 10).until(lambda x:
                                                      driver.find_element_by_id("username"))
            element.send_keys(username)
            time.sleep(1)
            print('密码...')
            element = WebDriverWait(driver, 10).until(lambda x:
                                                      driver.find_element_by_id("password"))
            element.send_keys(password)
            time.sleep(1)
            print('提交登录...')
            element = WebDriverWait(driver, 10).until(lambda x:
                                                      driver.find_element_by_xpath("//*[@id='xsfw']"))
            time.sleep(4)
            element.click()
            break
        except:
            if retry_times == 0:
                return False
            print('输入用户名密码出错，重试...')
            driver.refresh()
    return True


def enter_system(driver):
    print('寻找填报系统入口...')
    retry_times = 2
    while retry_times > 0:
        try:
            retry_times -= 1
            element = WebDriverWait(driver, 20).until(
                lambda x: x.find_element_by_xpath("//*[@id='app']/div[2]/div[2]/div/div/div/div/div[3]/div[2]/a"))
            element.click()
            break
        except:
            if retry_times == 0:
                return False
            print('寻找填报系统入口出错，重试...')
            driver.refresh()
            pass
    return True


def switch_to_new(driver):
    retry_times = 2
    while retry_times > 0:
        try:
            retry_times -= 1
            n = driver.window_handles  # 获取当前页句柄
            print('切换窗口...')
            driver.switch_to.window(n[-1])  # 切换到新的网页窗口
            break
        except:
            if retry_times == 0:
                return False
            print('切换窗口出错，重试...')
            driver.refresh()
        pass
    return True


def new_case(driver):
    retry_times = 3
    while retry_times > 0:
        try:
            retry_times -= 1
            print('新增...')
            element = WebDriverWait(driver, 20).until(
                lambda x: driver.find_element_by_css_selector(
                    "body > main > article > section > div.bh-mb-16 > div.bh-btn.bh-btn-primary"))
            time.sleep(1)
            element.click()
            break
        except:
            if retry_times == 0:
                return False
            print('新增出错，重试...')
            if retry_times == 1:
                driver.refresh()
            pass
    return True


def check_and_upload(driver):
    retry_times = 4
    while retry_times > 0:
        try:
            retry_times -= 1
            # 2020.4.29修改  #########################
            print('当天晨检体温...')
            time.sleep(2)
            element = WebDriverWait(driver, 15).until(
                lambda x: driver.find_element_by_xpath("/html/body/div[11]/div/div[1]/section/div[2]/div/div[4]/div[2]/div[1]/div[1]/div/input"))
            print('输入体温...')
            temp = random.choice(['36.5', '36.6', '36.7', '36.8', '36.9'])
            element.send_keys(temp)
            #  #######################################
            print('保存...')
            time.sleep(3)
            element = WebDriverWait(driver, 15).until(
                lambda x: driver.find_element_by_xpath("//*[@id='save' and @class='bh-btn bh-btn-primary']"))
            element.click()
            time.sleep(3)

            print('确认...')
            element = WebDriverWait(driver, 15).until(
                lambda x: driver.find_element_by_xpath(
                    "//a[text()='确认' and @class ='bh-dialog-btn bh-bg-primary bh-color-primary-5']"))
            element.click()
            break
        except Exception as e:
            if retry_times == 0:
                return False
            print("提交出错，重试...")
            print(e)
            # driver.refresh()
    return True


def screen_shot(driver, user):
    try:
        # picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        picture_url = driver.get_screenshot_as_file('F:\\Selenium\\Log\\' + picture_time + '\\' + user['name'] + '.png')
        print("截图:%s" % picture_url)
    except BaseException as msg:
        print('截图失败')


def if_filled(driver):
    flag = True
    try:
        print('寻找“今日已填报！”提示文字...')
        # dialog66bd7e22-cc1f-bf1f-2291-083f214c0f7c > div.bh-modal > div.bh-pop.bh-card.bh-card-lv4.bh-dialog-con > div.bh-dialog-center > div.bh-dialog-content > div
        # class ="content" tabindex="1" style="overflow: hidden; outline: none;" > 今日已填报！ < / div >
        WebDriverWait(driver, 5).until(
            lambda x: driver.find_element_by_class_name("content"))
        # driver.find_element_by_xpath("//*[@id='dialogf09fe0af-49dc-497b-09d1-42334833049a']/div[1]/div[1]/div[2]/div[1]/div"))
        print('已填报')
        return flag
    except:
        print('未填报')
        flag = False
        return flag


def single_operation(chrome_driver, user):
    print('——————————————————————————————————————————')
    print('user:' + user['id'])
    # 通过executable_path参数指定Chrome驱动文件所在位置
    if not open_login_website(chrome_driver):
        return Status.error
    if not input_user_info(chrome_driver, user['id'], user['password']):
        return Status.error
    if not enter_system(chrome_driver):
        return Status.error
    if not switch_to_new(chrome_driver):
        return Status.error
    if not new_case(chrome_driver):
        return Status.error
    if if_filled(chrome_driver):
        # driver.quit()
        return Status.filled
    if not check_and_upload(chrome_driver):
        return Status.error
    # driver.quit()
    return Status.done


def check_enable(each):
    if each['enable']:
        return True
    else:
        return False


# 时间
picture_time = time.strftime("%m-%d %H.%M", time.localtime(time.time()))
# Log与截图保存路径
mkpath = "F:\\Selenium\\Log\\" + picture_time
# 创建文件夹
mkdir(mkpath)
# 保存Log日志文件至txt
sys.stdout = Logger('F:\\Selenium\\Log\\' + picture_time + '\\Log.txt')  # 保存Log
# 读取用户信息，并向字典中添加Status变量
accounts = Neko_add.get_yaml('config.yml')
for each in accounts:
    if not check_enable(each):
        continue
    each['status'] = Neko_add.Status.unknown
# 存储未成功的case
q = queue.Queue()


for each in accounts:
    if not check_enable(each):
        continue
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        each_driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="F:\\Selenium\chromedriver.exe")

        status = single_operation(each_driver, each)
        if status == Neko_add.Status.error:
            print("出错项进入待重试队列...")
            each['status'] = status
            q.put(each)
            screen_shot(each_driver, each)
        else:
            print(each['id'] + ': ' + status.name)
            each['status'] = status
            Neko_add.send_email_auto(each)
            screen_shot(each_driver, each)
    except Exception as e:
        print(e)
        pass

while not q.empty():
    print("取待重试队列第一个任务...")
    each = q.get()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        each_driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="F:\\Selenium\chromedriver.exe")
        status = single_operation(each_driver, each)
        if status == Neko_add.Status.error:
            print("重新尝试" + each['id'] + status.name)
            each['status'] = status
            Neko_add.send_email_auto(each)
            screen_shot(each_driver, each)
        else:
            screen_shot(each_driver, each)
            each['status'] = status
            Neko_add.send_email_auto(each)
    except Exception as e:
        print(e)
        pass

print('——————————————————————————————————————————')

# 退出浏览器
