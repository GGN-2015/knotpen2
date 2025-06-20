from . import Knotpen2GameObject
from . import ClassBinder

def test_main():
    k2go = Knotpen2GameObject.Knotpen2GameObject()
    cb = ClassBinder.ClassBinder(k2go)
    cb.mainloop()