import sys
import os

import utils.dict_tools as dict_tools

def print_sorted_os_environ() -> None:
  print(dict_tools.sort_dict(os.environ))


def main():
  print_sorted_os_environ()

  dict_tools.get_filtered_dict(os.environ, "test", 12, "test2")

if __name__ == "__main__":
    main()