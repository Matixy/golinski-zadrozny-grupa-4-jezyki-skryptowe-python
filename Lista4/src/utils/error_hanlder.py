import sys
import os

FILE_NOT_FOUND_ERROR_INFO: str = "Błąd, nie znaleziono pliku:"
DEFAULT_ERROR_INFO: str = "Błąd programu:"

def error_hanlder(func):
  """Funkcja ktora uruchamia i obsluguje potencjalne wyjatki metody podanej w parametrze """
  
  try:
    func()
  except FileNotFoundError as e:
    print(f"{FILE_NOT_FOUND_ERROR_INFO} {e}", file=sys.stderr)
    sys.exit(1)
  except KeyboardInterrupt:
    pass
  except BrokenPipeError:
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
    except Exception:
        pass
    sys.exit(0)
  except Exception as e:
    print(f"{DEFAULT_ERROR_INFO} {e}", file=sys.stderr)
    sys.exit(1)