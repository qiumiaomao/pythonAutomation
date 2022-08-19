import time
import os
import pytest

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.yaml_helper import YamlHelper
from config.global_config import get_config
from configtest import driver


class Baidu(BasePage):
    # 从全局变量中获取DOMAIN
    DOMAIN = get_config('config')['DOMAIN']

    # YAML文件相对于本文件的路径
    element_locator_yaml = "./config/element_locator/baidu.yaml"
    # element_locator_yaml = YamlHelper().read_yaml(
        # os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/element_locator", "baidu.yaml"))
    element = YamlHelper.read_yaml(element_locator_yaml)
    # print(type(element))
    # print(element)

    # 获取所有的页面对象
    input_box = (By.ID, element['KEY_WORLD_LOCATOR'])           # 百度输入框
    search_btn = (By.ID, element['SEARCH_BUTTON_LOCATOR'])      # 搜索按钮
    first_result = (By.XPATH, element['FIRST_RESULT_LOCATOR'])   # 搜索结果页面的第一个搜索结果

    # 继承父类的init方法
    def __init__(self, driver=None):
        super().__init__(driver)


    # 定义方法类
    def baidu_search(self, search_string):
        # self.driver = driver
        self.driver.get(self.DOMAIN)
        # self.driver.get("https://www.baidu.com")
        # self.driver.find_element(By.ID, self.element['KEY_WORLD_LOCATOR']).clear()
        # self.driver.find_element(By.ID, self.element['KEY_WORLD_LOCATOR']).send_keys(search_string)
        # self.driver.find_element(By.ID, self.element['SEARCH_BUTTON_LOCATOR']).click()
        self.driver.find_element(*self.input_box).clear()
        self.driver.find_element(*self.input_box).send_keys(search_string)
        self.driver.find_element(*self.search_btn).click()

        time.sleep(2)

        # search_results = self.driver.find_element(By.XPATH, self.element['FIRST_RESULT_LOCATOR']).get_attribute('innerHTML')
        search_results = self.driver.find_element(*self.first_result).get_attribute('innerHTML')


        return search_results


