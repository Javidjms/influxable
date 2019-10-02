def raise_if_error(func):
    def func_wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return func_wrapper
