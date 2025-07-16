import os
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)

sys.path = [os.path.join(ROOT_DIR, "knotpen2")] + sys.path
import constant_config # 这个 import 需要在上面新增的文件夹 import

print(constant_config.APP_VERSION)
