import os
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
sys.path = [os.path.join(ROOT_DIR, "knotpen2")] + sys.path

import constant_config

print(constant_config.APP_VERSION)
