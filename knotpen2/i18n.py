import gettext
import locale
import constant_config

# 设置 locale 目录（存放翻译文件的路径）
localedir = constant_config.LOCALE_DIR

# 应用名称（对应 .mo 文件的域名）
domain = 'knotpen2'

# 设置语言
current_locale, encoding = "en_US", "UTF-8"

# 设置当前环境的语言
locale.setlocale(locale.LC_ALL, current_locale)

# 加载对应语言的翻译
t = gettext.translation(domain, localedir, languages=[current_locale], fallback=True)
_ = t.gettext
