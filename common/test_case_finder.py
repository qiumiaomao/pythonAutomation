# test_case_finder.py模块用于根据指定的文件夹查找并返回可执行的测试用例。查找测试用例支持自定义标签
import importlib.util
import inspect
import os
import sys
from common.data_provider import mk_test_name


class DiscoverTestCases:
    def __init__(self, target_file_or_path=None):
        '''指定测试用例开始查找目录，如果没有指定，则分配固定目录'''
        if not target_file_or_path:
            self.target_file_or_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')
        else:
            self.target_file_or_path = target_file_or_path

    def find_test_modele(self):
        '''根据指定文件查找测试用例模块并导入'''
        mod_ref = []
        file_lists = []
        # 判断用户给定的-t参数的值是否为文件夹，如是，则将其中的所有模块递归解析出来，并放入列表
        if os.path.isdir(self.target_file_or_path):
            def recursive_file_parser(file_path):
                files = os.listdir(file_path)
                for f in files:
                    f_p = os.path.join(file_path, f)
                    if os.path.isdir(f_p):
                        recursive_file_parser(f_p)
                    else:
                        if f_p.endswith('.py'):
                            file_lists.append(os.path.join(file_path, f_p))
                return file_lists
            all_files = recursive_file_parser(self.target_file_or_path)

            module_name_list = []
            module_file_paths = []
            for item in all_files:
                '''根据文件路径查找模块'''
                # inspect.getmodulename(path)：根据path返回模块名（不包括其所在的package）
                module_name_list.append(inspect.getmodulename(item))
                module_file_paths.append(item)

        elif os.path.isfile(self.target_file_or_path):
            module_name_list = [inspect.getmodulename(self.target_file_or_path)]
            module_file_paths = [self.target_file_or_path]

        # 动态导入查到的每个模块
        for module_name, module_file_path in zip(module_name_list,module_file_paths):
            try:
                # 通过模块名和文件路径来引入一个模块
                # 首先获取到模块的实际路径和名称。然后我们将这些信息传入到util的spec_from_file_location函数中，这个将会返回模块的说明
                module_spec = importlib.util.spec_from_file_location(module_name, module_file_path)
                # 将其(模块的说明)传入到module_from_spec函数，它将会返回引入的模块
                module = importlib.util.module_from_spec(module_spec)

                module_spec.loader.exec_module(module)
                sys.modules[module_name] = module
                mod_ref.append(module)
            except ImportError:
                raise ImportError('Module:{} can not imported'.format(self.target_file_or_path))
        return mod_ref


    def find_tests(self, mod_ref):
        '''遍历上一步查找到的测试模块，过滤出符合条件的测试用例'''
        test_cases = []
        for module in mod_ref:
            cls_members = inspect.getmembers(module, inspect.isfunction(module))
            for cls in cls_members:
                cls_name, cls_code_object = cls
                for func_name in dir(cls_code_object):
                    tests_suspect = getattr(cls_code_object, func_name)
                    if getattr(tests_suspect, "__test_case_type__", None) == "__TestCase__":
                        # 获取测试函数__test_tag__属性的值
                        tag_filter = getattr(tests_suspect, "__test_tag__", None)
                        # 获取测试类中的所有方法，查看是否有"__data_Provider__"属性
                        if hasattr(tests_suspect,"__data_Provider__"):
                            for i, v in enumerate(getattr(tests_suspect, "__data_Provider__")):
                                # 根据测试数据的数组调用mk_test_name生成新的测试用例名
                                new_test_name = mk_test_name(tests_suspect.__name__, getattr(v, "__name__", v), i)
                                # 将测试函数Tag，测试类，新生成的测试用例名，测试数据组成一条测试用例共测试框架后续调用
                                test_cases.append((tag_filter, cls_code_object, func_name, tests_suspect, None))
                        else:
                            # 当没有"__data_Provider__"属性，直接返回原测试用例
                            test_cases.append((tag_filter, cls_code_object, func_name, tests_suspect, None))
        return test_cases