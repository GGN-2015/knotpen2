from . import Knotpen2GameObject
from . import ClassBinder
from . import MemoryObject

def test_main():
    mo   = MemoryObject.MemoryObject()
    k2go = Knotpen2GameObject.Knotpen2GameObject(mo)
    cb   = ClassBinder.ClassBinder(k2go)
    cb.mainloop()