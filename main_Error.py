import functools
import platform
import subprocess
from collections import OrderedDict
from multiprocessing.pool import ThreadPool
from time import time
from common.customize_error import RunTimeTooLong
from common.test_case_finder import DiscoverTestCases
from common.test_filter import TestFilter
from common.user_options import parse_options
from config.global_config import init, set_config, get_config


# 根据进程名字强制退出进程
def kill_process_by_name(process_name):
    try:
        if platform.system() == "Windows":
            subprocess.check_output("taskkill /f /im %s" % process_name, shell=True, stderr=subprocess.STDOUT)
        else:
            subprocess.check_output("killall '%s'" % process_name, shell=True, stderr=subprocess.STDOUT)
    except BaseException as e:
        print(e)


# 清理环境
def clear_env():
    if platform.system() == "Windows":
        kill_process_by_name("chrome.exe")
        kill_process_by_name("chromedriver.exe")
        kill_process_by_name("firefox.exe")
        kill_process_by_name("iexplore.exe")
        kill_process_by_name("IEDriverServer.exe")
    else:
        kill_process_by_name("Google Chrome")
        kill_process_by_name("chromedriver")


def group_test_cases_by_class(cases_to_run):
    test_groups_dict = OrderedDict()
    for item in cases_to_run:
        tag_filter, cls, func_name, func, value = item
        test_groups_dict.setdefault(cls, []).append((tag_filter, cls, func_name, func, value))
    test_groups = [(x, y) for x, y in zip(test_groups_dict.keys(), test_groups_dict.values())]
    return test_groups

# 在上一个基础上加的
def class_run(case, test_thread_number):
    print(case)
    cls, func_pack = case
    p = ThreadPool(test_thread_number)
    p.map(func_run, func_pack)
    p.close()
    p.join()

# 在上一个基础上加的
def func_run(case):
    try:
        # 测试开始时间
        s = time()
        cls_group_name, cls, func_name, func, value = case
        cls_instance = cls()
        if value:
            getattr(cls_instance, func.__name__).__wrapped__(cls_instance, *value)
        else:
            getattr(cls_instance, func.__name__).__wrapped__(cls_instance)
        # 测试结束时间
        e = time()
        # 超出运行时间，通过get_config获取
        if e - s > get_config("config")["run_time_out"]:
            raise RunTimeTooLong(func_name, e-s)
    except RunTimeTooLong as runtime_err:
        print(runtime_err)
        # 当出现RunTimeTooLong错误时，设置相应的属性
        setattr(func, 'run_status', 'error')
        setattr(func, 'exception_type', 'RunTimeTooLong')
    except AssertionError as assert_err:
        print(assert_err)
    except Exception as e:
        print(e)
    finally:
        # 环境清理
        clear_env()


def main(args=None):
    start = time()
    # 解析用户输入
    options = parse_options(args)
    # 初始化环境变量
    init()
    # 设置全局环境变量
    set_config('config', options.config)

    # 从默认文件夹tests开始查找测试用例
    case_finder = DiscoverTestCases()
    # print(case_finder)
    # 查找测试模块并导入
    test_module = case_finder.find_test_modele()
    # print(test_module)
    # 查找并筛选测试用例
    original_test_cases = case_finder.find_tests(test_module)
    # print(original_test_cases)
    # 根据用户输入参数-i进一步筛选
    raw_test_suites = TestFilter(original_test_cases).tag_filter_run(options.include_tags_any_match)
    # print(raw_test_suites)
    # 获取最终的测试用例集，并按类名组织
    test_suites = group_test_cases_by_class(raw_test_suites)
    # print(test_suites)

    #
    print("运行线程数为：%s" %options.test_thread_number)
    # 传入并发数目
    p = ThreadPool(options.test_thread_number)
    # 使用偏函数固定并发数目
    # 使用map()函数将test_suites列表中的测试用例逐一传入class_run运行
    p.map(functools.partial(class_run, test_thread_number = options.test_thread_number), test_suites)
    p.close()
    p.join()
    end = time()
    print("本次总运行时间 %s s" %(end-start))

    # 运行每一个测试用例
    # for test_suite in test_suites:
    #     test_class, func_run_pack_list = test_suite
    #     for func_run_pack in func_run_pack_list:
    #         cls_group_name, cls, func_name, func, value = func_run_pack
    #         cls_instance = cls()
    #         if value:
    #             getattr(cls_instance, func.__name__).__wrapped__(cls_instance, *value)
    #         else:
    #             getattr(cls_instance, func.__name__).__wrapped__(cls_instance)

if __name__ == '__main__':
    # main()
    # main("-env prod -i smoke -t ./tests")
    main("-env prod -i smoke -t ./tests -n 8")