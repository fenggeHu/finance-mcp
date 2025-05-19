from functools import wraps


def OAuth_required(func):
    """
    OAuth 2.1
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pass
