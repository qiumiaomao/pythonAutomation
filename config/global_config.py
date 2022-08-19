# global_config.py模块用于获取用户输入的环境变量，并将其作为全局变量共享。

def init():
    global _config
    _config = {}


def get_config(k):
    try:
        return _config[k]
    except KeyError:
        return None


def set_config(k, v):
    try:
        _config[k] = v
    except KeyError:
        return None