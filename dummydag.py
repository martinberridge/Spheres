Stored = 1
CanSet = 2
Serializeable = 3

class domObj(object):
    pass


def dagMethod(arg):
    if callable(arg):
        def newfn(*args, **kwargs):
            return arg(*args, **kwargs)
        return newfn
    else:
        def d2(fn):
            def newfn(*args, **kwargs):
                return fn(*args, **kwargs)
            return newfn
        return d2
