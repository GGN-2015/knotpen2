import pygame
import os
import traceback

DIRNOW = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path=[DIRNOW] + sys.path; print(sys.path); 

# 相对导入
import constant_config
import error_log
import Knotpen2GameObject
import ClassBinder
import MemoryObject
import MyAlgorithm

def test_main():
    pygame.init()
    mo   = MemoryObject.MemoryObject()
    algo = MyAlgorithm.MyAlgorithm(mo)
    k2go = Knotpen2GameObject.Knotpen2GameObject(mo, algo)
    cb   = ClassBinder.ClassBinder(k2go)
    cb.mainloop()

if __name__ == "__main__":
    os.makedirs(constant_config.ANSWER_FOLDER, exist_ok=True)
    os.makedirs(constant_config.AUTOSAVE_FOLDER, exist_ok=True)
    os.makedirs(constant_config.ERROR_LOG_FOLDER, exist_ok=True)

    try:
        test_main()
    except:
        error_info = traceback.format_exc()
        print(error_info)

        filepath = error_log.error_log(error_info) # 记录错误信息并退出
        print("错误日志信息已经保存到：%s" % filepath)
        sys.exit(1)
