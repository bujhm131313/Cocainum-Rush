import arcade
from functools import wraps


def render(width: int, height: int, name: str):
    """
        Opens window with input params and provides rendering of incoming
        function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arcade.open_window(width, height, name)
            arcade.start_render()
            res = func(*args, **kwargs)
            arcade.finish_render()
            arcade.run()
            return res

        return wrapper
    return decorator
