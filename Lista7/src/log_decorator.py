import time
from enum import Enum
import logging
import logger_setup
import inspect

logger = logging.getLogger(__name__)


class Logging_Levels(Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

def parse_logging_level(level_name: str) -> int:
    level_name = level_name.upper()
    try:
        return Logging_Levels[level_name].value
    except KeyError:
        raise ValueError(f"Invalid logging level: {level_name}")
    



def log_decorator(log_lvl = "INFO"):     # Decorators can accept their own arguments by adding another wrapper level.
    def log_decorator(func):
        def enchanced_func(*args, **kwargs):
            level = parse_logging_level(log_lvl)

            if inspect.isclass(func):
                logger.log(level, f"Start creating object of class: {func.__name__.upper()}")
                result = func(*args, **kwargs)
                logger.log(level, f"Finish, object created")
                
            else:
                logger.log(level, f"Functon name: {func.__name__.upper()}")
                if args:
                    logger.log(level, f"Args: {args}")
                if kwargs:
                    logger.log(level, f"Kwargs: {kwargs}")

                start_t = time.time()
                logger.log(level, f"Start time: {start_t}")
                result = func(*args, **kwargs)
                logger.log(level, f"Execute time: {time.time() - start_t}")
                logger.log(level, f"Return value: {result}")

            return result
        return enchanced_func
    return log_decorator


@log_decorator("DEBUG")
def make_tea(x, y):
    print("Making tea ...")
    time.sleep(2)
    print("Ready")
    return x+y

@log_decorator("INFO")
class TeaMachine:
    def __init__(self, model):
        self.model = model
        print(f"Uruchamiam maszynę: {self.model}")

def main():
    logger_setup.setup_logger()

    # maker = log_decorator("DEBUG")(make_tea)
    # maker(2,6)

    make_tea(2,6)
    
    my_machine = TeaMachine(model="T-1000")
    

if __name__ == "__main__":
    main()