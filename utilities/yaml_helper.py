# yaml_helper.py模块进行元素的读取

import yaml
import os


class YamlHelper:
    @staticmethod
    def read_yaml(yaml_file_path):
        with open(yaml_file_path, "r", encoding='utf-8') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(e)


if __name__ == '__main__':
    # print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/element_locator", "baidu.yaml"))
    res = YamlHelper().read_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/element_locator", "baidu.yaml"))
    print(type(res))
    print(type(res['KEY_WORLD_LOCATOR']))