import os
import sys
from pathlib import Path

APP_NAME = "knotpen2"
APP_VERSION = "2.5.0" # 不要删除这行内容，因为脚本会从这里抓取


def _is_packaged_executable() -> bool:
    return getattr(sys, "frozen", False) and bool(getattr(sys, "_MEIPASS", None))


def _get_program_exe_path() -> str:
    if _is_packaged_executable():
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.getcwd()


def _get_user_data_dir() -> str:
    if _is_packaged_executable():
        return _get_program_exe_path()

    if os.name == "nt":
        base_dir = os.environ.get("APPDATA") or str(Path.home())
        return os.path.join(base_dir, APP_NAME)

    if sys.platform == "darwin":
        return os.path.join(str(Path.home()), "Library", "Application Support", APP_NAME)

    base_dir = os.environ.get("XDG_DATA_HOME") or os.path.join(str(Path.home()), ".local", "share")
    return os.path.join(base_dir, APP_NAME)


# 当前程序执行路径。PyInstaller 版本为 exe 所在目录；源码/pip 运行时为当前工作目录。
PROGRAM_EXE_PATH = _get_program_exe_path()

# 包资源目录。PyInstaller 版本使用临时解包目录；源码/pip 运行时使用包目录。
PACKAGE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

# 用户可写数据目录。pip 安装时不能写入包安装目录，因此项目和日志放在这里。
USER_DATA_DIR = _get_user_data_dir()
AUTOSAVE_FILE_NAME = "auto_save.json"

ERROR_LOG_FOLDER = os.path.join(USER_DATA_DIR, "error_log")
DEFAULT_PROJECTS_FOLDER = os.path.join(USER_DATA_DIR, "projects")
PROJECT_FILE_NAME = "project.json"
PROJECT_AUTOSAVE_FOLDER_NAME = "auto_save"
PROJECT_ANSWER_FOLDER_NAME = "answer"

CIRCLE_RADIUS = 12
LINE_WIDTH = 8

BACKUP_TIME = 180 # 每三分钟自动保存一次，如果和上次自动保存内容完全一致，则删除最新的自动保存
STRIDE = 50

# i18n 文件夹位置
LOCALE_DIR = os.path.join(PACKAGE_DIR, "i18n", "locales")
LANG_CODE_SET = ['zh_CN', 'en_US'] # 可以使用的所有语言翻译

# 图标位置
PYGAME_ICON_PATH = os.path.join(PACKAGE_DIR, "logo.ico")

# 字体文件加载目录
FONT_TTF = os.path.join(PACKAGE_DIR, "font", "SourceHanSansSC-VF.ttf")
MAX_MESSAGE_CNT = 40
MESSAGE_SIZE = 18
SMALL_TEXT_SIZE = 14
BUTTON_FONT_SIZE = 14
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 34
BUTTON_GAP = 6
MIN_BUTTON_HEIGHT = 20
MIN_BUTTON_GAP = 3
BUTTON_MARGIN = 10
BUTTON_BORDER_RADIUS = 4
BUTTON_PANEL_PADDING = 8
WINDOW_MARGIN = 80
MIN_WINDOW_WIDTH = 640
MIN_WINDOW_HEIGHT = 480
WINDOW_RESIZE_STEP = 120
def MESSAGE_POSITION(i:int):
    return (10 , 10 + (MESSAGE_SIZE + 2) * i)

# SVG 绘图属性
SVG_STROKE_COLOR = "black"
SVG_STROKE_WIDTH = 3
SVG_FONT_SIZE = SMALL_TEXT_SIZE
SVG_TEXT_DELTA_Y = 15 # 对 SVG 文件中的文字位置进行微调
ARROW_SIZE = 5 # SVG 图片中箭头的大小
SVG_EXPAND_RATIO = 1 # 放大倍数

DOUBLE_CLICK_TIME = 0.25 # 双击时两次点击的最大间隔

LEFT_KEY_ID  = 1
MID_KEY_ID   = 2
RIGHT_KEY_ID = 3

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (128, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 192, 0)
BLUE = (0, 0, 255)
