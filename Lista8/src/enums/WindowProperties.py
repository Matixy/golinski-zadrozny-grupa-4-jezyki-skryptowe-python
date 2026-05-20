from enum import Enum

class WindowProperties(Enum):
  NAME: str = "HTTP Log analyzer"
  WIDTH: int = 1200
  HEIGHT: int = 960
  RESIZABLE: bool = True
  MIN_SIZE: tuple = (800, 600)