# pages文件夹存放所有的页面对象类。为类方便建立一个页面对象基类，即base_page.py

from selenium import webdriver


class BasePage:

    def __init__(self, driver):
        # 初始化浏览器驱动
        if driver:
            self.driver = driver
        else:
            self.driver = webdriver.Chrome()

    def open_page(self, url):
        # 根据地址打开浏览器
        self.driver.get(url)

    def close(self):
        # 关闭浏览器
        self.driver.close()