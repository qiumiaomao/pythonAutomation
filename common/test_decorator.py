# test_decorator.py模块是用于给测试用例打标签。通过类装饰器，测试用例可以根据测试需要，拥有多个测试标签。打过标签后，静态测试用例可以根据测试目的动态运行

from functools import wraps


class Test(object):
    # enabled 决定使用标签挑选测试用例是否启用
    # 默认启用，如为False，则不启用
    # tag为用户自定义标签
    def __init__(self, tag=None, enabled=True):
        self.enabled = enabled
        self.tag = tag

    def __call__(self, func):
        @wraps(func)
        def wrapper(*agrs, **kwargs):
            return func(*agrs, **kwargs)
        # 给原测试用例添加属性，以便测试框架判断当前测试函数是否为测试用例
        setattr(wrapper, "__test_tag__", self.tag)
        setattr(wrapper, "__test_case_type__", "__TestCase__")
        setattr(wrapper, "__test_case_enabled", self.enabled)
        return wrapper
