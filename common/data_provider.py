# data_provider.py模块赋予了测试框架数据驱动的能力。测试框架通过data_provider.py模块，根据提供的数据生成多个测试用例，并根据每组数据生成测试用例名

import re


def data_provider(test_data):
    def wrapper(func):
        setattr(func, "__data_provider__", test_data)
        global index_len
        index_len = len(str(len(test_data)))
        return func
    return wrapper

def mk_test_name(name, value, index=0):
    index = "{0:0{1}d}".format(index+1, index_len)
    test_name = "{0}_{1}_{2}".format(name, index, str(value))
    return re.sub(r'\W|^(?=\d)', '_', test_name)