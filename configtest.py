from selenium import webdriver
import pytest

global driver

@pytest.fixture(scope="session", autouse=True)
def driver():
    global driver
    if driver is None:
        driver = webdriver.Chrome()
    return driver