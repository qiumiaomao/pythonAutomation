from common.test_decorator import Test
from common.data_provider import data_provider
from pages.baidu import Baidu
from pages.base_page import BasePage
import pytest
import time
from configtest import driver


class BaiduTest:

    @data_provider([('iTesting','iTesting'),('helloqa','iTesting')])
    @Test(tag='smoke')
    def test_baidu_search(self):
        baidu = Baidu()

        # search_string = 'iTesting'
        expect_string = 'iTesting'
        results = baidu.baidu_search(search_string="iTesting")
        assert expect_string in results
        time.sleep(3)

        # baidu.close()

    # @data_provider([('iTesting', 'iTesting'), ('helloqa', 'iTesting')])
    # @Test(tag='smoke')
    # def test_baidu_search_02(self):
    #     baidu = Baidu()
    #
    #     # search_string = 'iTesting'
    #     expect_string = 'iTesting'
    #     results = baidu.baidu_search("iTesting")
    #     assert expect_string in results
    #
    #     baidu.close()

if __name__ == '__main__':
    pytest.main(['-v','-s','test_baidu.py'])