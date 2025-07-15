import pygame
import os

DIRNOW = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path=[DIRNOW] + sys.path; print(sys.path); 

# 相对导入
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
    test_main()
    os.makedirs(os.path.join(DIRNOW, "answer"), exist_ok=True)
    os.makedirs(os.path.join(DIRNOW, "auto_save"), exist_ok=True)
    os.makedirs(os.path.join(DIRNOW, "error_log"), exist_ok=True)
