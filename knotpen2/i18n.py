import gettext
import locale
import os

import constant_config

# 设置 locale 目录（存放翻译文件的路径）
localedir = constant_config.LOCALE_DIR

# 应用名称（对应 .mo 文件的域名）
domain = 'knotpen2'

# 获取系统语言
# def get_lang_variable():
#     """获取环境变量 LANG 的值"""
#     lang_value = os.getenv('LANG')
#     if lang_value is not None and lang_value.startswith("zh_"):
#         return "zh_CN"
#     else:
#         return "en_US"

def get_lang_variable():
    return "en_US"

# 设置当前环境的语言
current_locale = get_lang_variable()
locale.setlocale(locale.LC_ALL, current_locale)

# 加载对应语言的翻译
t = gettext.translation(domain, localedir, languages=[current_locale], fallback=True)
_ = t.gettext

if __name__ == "__main__":
    print(get_lang_variable())
