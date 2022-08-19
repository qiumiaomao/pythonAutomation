from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest


class TestBaidu:
    def test_baidu(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.baidu.com")
        self.driver.find_element(By.ID,"kw").send_keys("iTesting")


if __name__ == '__main__':
    pytest.main(['test_baidu.py'])