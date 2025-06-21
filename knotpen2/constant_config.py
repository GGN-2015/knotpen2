import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
AUTOSAVE_FOLDER = os.path.join(DIRNOW, "auto_save")
AUTOSAVE_FILE = os.path.join(AUTOSAVE_FOLDER, "auto_save.json") # 自动保存位置

CIRCLE_RADIUS = 10
LINE_WIDTH = 8

BACKUP_TIME = 180 # 每三分钟自动保存一次，如果和上次自动保存内容完全一致，则删除最新的自动保存
STRIDE = 50

DOUBLE_CLICK_TIME = 0.25 # 双击时两次点击的最大间隔

LEFT_KEY_ID  = 1
MID_KEY_ID   = 2
RIGHT_KEY_ID = 3

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 192, 0)
BLUE = (0, 0, 255)