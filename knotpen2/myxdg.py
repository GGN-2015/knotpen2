import os
import sys

def get_config_dir(app_name):
    """获取应用的配置目录（兼容Linux和Windows）"""
    if sys.platform.startswith('win32'):
        # Windows：映射到 AppData\Roaming
        user_profile = str(os.environ.get('USERPROFILE'))
        base_dir = os.path.join(user_profile, 'AppData', 'Roaming')
    else:
        # Linux：遵循XDG规范
        base_dir = os.environ.get('XDG_CONFIG_HOME', 
                                 os.path.join(os.path.expanduser('~'), '.config'))
    aim_dir = os.path.join(base_dir, app_name)
    os.makedirs(aim_dir, exist_ok=True) # 保证文件夹存在
    print("get_config_dir: %s" % aim_dir)
    return aim_dir

def get_data_dir(app_name):
    """获取应用的数据目录（兼容Linux和Windows）"""
    if sys.platform.startswith('win32'):
        # Windows：映射到 AppData\Local
        user_profile = str(os.environ.get('USERPROFILE'))
        base_dir = os.path.join(user_profile, 'AppData', 'Local')
    else:
        # Linux：遵循XDG规范
        base_dir = os.environ.get('XDG_DATA_HOME', 
                                 os.path.join(os.path.expanduser('~'), '.local', 'share'))
    aim_dir = os.path.join(base_dir, app_name)
    os.makedirs(aim_dir, exist_ok=True) # 保证文件夹存在
    print("get_data_dir: %s" % aim_dir)
    return aim_dir
