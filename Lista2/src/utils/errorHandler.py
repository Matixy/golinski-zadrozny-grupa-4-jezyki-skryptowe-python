import sys
import os

VALUE_ERROR_INFO: str = "Błąd danych:"
DEFAULT_ERROR_INFO: str = "Błąd programu:"

def runFuncWithExceptionHandling(func):
  """Funkcja ktora uruchamia i obsluguje potencjalne wyjatki metody podanej w parametrze """
  
  try:
    func()
  except ValueError as e:
    print(f"{VALUE_ERROR_INFO} {e}", file=sys.stderr)
    sys.exit(1)
  except BrokenPipeError:
    # wyjście przy pękniętym potoku- zignorowanie błędu
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
    except Exception:
        pass
    sys.exit(0)
    
  except Exception as e:
    print(f"{DEFAULT_ERROR_INFO} {e}", file=sys.stderr)
    sys.exit(1)