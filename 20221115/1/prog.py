def objcount(original_class):
    original_class.counter = 0
    original_init = original_class.__init__

    def __init__(self, *args, **kwargs):
        original_class.counter += 1
        original_init(self, *args, **kwargs)

    original_class.__init__ = __init__
    original_del = original_class.__del__ if "__del__" in dir(original_class) else 0

    def __del__(self):
        original_class.counter -= 1
        if original_del != 0:
            original_del(self)

    original_class.__del__ = __del__

    return original_class
