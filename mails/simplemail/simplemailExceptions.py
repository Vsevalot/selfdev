from functools import wraps


class ExecutionFailed():
    def __init__(self, exception: Exception):
        self.exception = exception

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Execution object. Reason:\n{self.exception}"


def exception_decorator(f):
    """
    Exception handler
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            return res
        except Exception as e:
            print(e)
            return ExecutionFailed(e)
    return wrapper
