import os
import sys

# 图片路径
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '..\\images\\')
# 代码路径
CURRENT_PATH = os.path.join(os.path.dirname(__file__), '..\\')

if __name__ == '__main__':
    print(CURRENT_PATH)
