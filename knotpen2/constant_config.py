import os
DIRNOW = os.path.dirname(os.path.abspath(__file__))
AUTOSAVE = os.path.join(DIRNOW, "auto_save.json") # 自动保存位置

CIRCLE_RADIUS = 10
LINE_WIDTH = 8

STRIDE = 50

LEFT_KEY_ID  = 1
MID_KEY_ID   = 2
RIGHT_KEY_ID = 3

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)