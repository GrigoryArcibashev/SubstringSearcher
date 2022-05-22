import time


def stopwatch(head_message: str = None):
    def decorator(func):
        def decorated(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            finish = time.time()
            if head_message is not None:
                print(f"{head_message}: ", end="")
            print(f"working time is {finish - start} seconds")

            return result

        return decorated

    return decorator
