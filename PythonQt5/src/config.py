import os
import sys

VERSION = 202312081708
APP_NAME = "诊断开发常用工具"
URL = "http://192.168.2.234/"
# 图片路径
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..\\images\\')
# 代码路径
# CURRENT_PATH = os.path.join(os.path.dirname(__file__), '..\\')
# 当前路径
CURRENT_PATH = os.path.dirname(os.path.realpath(sys.executable))
# 上层路径
# CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(sys.executable)))

if __name__ == '__main__':
    print(CURRENT_PATH)
    print(IMAGE_PATH)
