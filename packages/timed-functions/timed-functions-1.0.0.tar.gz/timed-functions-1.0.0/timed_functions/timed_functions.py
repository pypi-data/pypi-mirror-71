import time


def timing(f):
    def print_duration(*args, **kwargs):
        start = time.time()

        ret = f(*args, **kwargs)

        millis = (time.time() - start) * 1000.0
        print("@timing - '{:s}' took {:.3f} ms".format(f.__name__, millis))
        return ret

    return print_duration
