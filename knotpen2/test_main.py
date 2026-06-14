import argparse
import os
import traceback

import sys

# 相对导入
try:
    from . import constant_config
    from . import error_log
    from .i18n import _
except ImportError:
    DIRNOW = os.path.dirname(os.path.abspath(__file__))
    sys.path = [DIRNOW] + sys.path
    import constant_config
    import error_log
    from i18n import _


def configure_stdout():
    encoding = (getattr(sys.stdout, "encoding", None) or "").lower()
    if encoding == "utf-8":
        return

    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
        except Exception:
            pass


def set_pygame_icon(icon_path:str):
    import pygame

    # 加载图标图像（确保图像文件存在）
    try:
        icon = pygame.image.load(icon_path)  # 替换为你的图标文件路径
        pygame.display.set_icon(icon)
    except pygame.error:
        print(_("无法加载图标图像，请检查文件路径和格式！"))

def run_app():
    import pygame

    try:
        from . import Knotpen2GameObject
        from . import ClassBinder
        from . import MemoryObject
        from . import MyAlgorithm
    except ImportError:
        import Knotpen2GameObject
        import ClassBinder
        import MemoryObject
        import MyAlgorithm

    pygame.init()
    set_pygame_icon(constant_config.PYGAME_ICON_PATH)

    mo   = MemoryObject.MemoryObject()
    algo = MyAlgorithm.MyAlgorithm(mo)
    k2go = Knotpen2GameObject.Knotpen2GameObject(mo, algo)
    cb   = ClassBinder.ClassBinder(k2go)
    cb.mainloop()

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog=constant_config.APP_NAME,
        description="Start the Knotpen2 graphical editor.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{constant_config.APP_NAME} {constant_config.APP_VERSION}",
    )
    parser.add_argument(
        "--data-dir",
        action="store_true",
        help="Print the user data directory and exit.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    configure_stdout()
    args = parse_args(argv)

    if args.data_dir:
        print(constant_config.USER_DATA_DIR)
        return 0

    os.makedirs(constant_config.DEFAULT_PROJECTS_FOLDER, exist_ok=True)
    os.makedirs(constant_config.ERROR_LOG_FOLDER, exist_ok=True)

    try:
        run_app()
    except:
        error_info = traceback.format_exc()
        print(error_info)

        filepath = error_log.error_log(error_info) # 记录错误信息并退出
        print(_("错误日志信息已经保存到：%s") % filepath)
        return 1

    return 0


def test_main():
    return main()


if __name__ == "__main__":
    raise SystemExit(main())
