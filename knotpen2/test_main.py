import pygame
from . import Knotpen2GameObject
from . import ClassBinder
from . import MemoryObject
from . import MyAlgorithm

def test_main():
    pygame.init()

    mo   = MemoryObject.MemoryObject()
    algo = MyAlgorithm.MyAlgorithm(mo)
    k2go = Knotpen2GameObject.Knotpen2GameObject(mo, algo)
    cb   = ClassBinder.ClassBinder(k2go)
    cb.mainloop()
