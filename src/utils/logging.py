import logging
import functools

def get_logger(name):
    logger = logging.getLogger(name)
    handler = logging.FileHandler('./alert.log', 'a+')
    f = logging.Formatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s')
    handler.setFormatter(f)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def log_error(*args, **kwargs):

    def error_log(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Execute the called function
                # If it throws an error `Exception` will be called.
                # Otherwise it will be execute successfully.
                return func(*args, **kwargs)
            except Exception as e:
                logger = get_logger(f'{func.__name__}Error')
                error_msg = 'And error has occurred at /' + func.__name__ + '\n'
                logger.error(error_msg, e)

                return e  # Or whatever message you want.

        return wrapper

    return error_log
