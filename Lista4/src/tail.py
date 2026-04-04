import sys
import argparse
import time

from typing import TextIO
from collections import deque

from utils.error_hanlder import error_hanlder

def get_last_n_lines(stream: TextIO, n: int = 10) -> list:
  """
  return n last lines from text stream
  
  uses deque with a fixed maximum length to keep memory usage
  """
  
  last_lines: deque = deque(stream, maxlen=n) # deque has fixed length- provides replacing first appended elem with new if que has maxlen

  return list(last_lines)

def read_line_arguments() -> argparse.Namespace:
  """
  parse command-line arguments and return them as namespace object 
  
  supports long and (optionally) short argument names (provides by argparse)

  arguments:
  file (optional)
  --lines (default: 10)
  --follow
  """
  
  parser: argparse.ArgumentParser = argparse.ArgumentParser()
  
  parser.add_argument('file', nargs='?', type=str) # add arugment file nargs=? menas it is optional argument
  parser.add_argument('--lines', type=int, default=10)
  parser.add_argument('--follow', action='store_true') # action=store_true means if --follow was in arguments set true else false
  
  args: argparse.Namespace = parser.parse_args()
  
  return args

def tail(stream: TextIO, args: argparse.Namespace) -> None:
  """
  print the last n lines from the stream

  if the --follow flag is enabled and a file is provided,
  continue to monitor the stream and print new lines
  """
  
  last_lines: list = get_last_n_lines(stream, args.lines)
  
  for line in last_lines:
    print(line, end="") # end="" cause line conatins \n at end of line
    
  sys.stdout.flush() # force to print buffor (casued by end="")
    
    
  #--follow option implementation only when file was in arguments
  if args.follow and args.file:
    for new_line in follow_stream(stream):
      print(new_line, end="") # end="" cause line conatins \n at end of line
      sys.stdout.flush() # force to print buffor (casued by end="")
      

def follow_stream(stream: TextIO):
  """
  Generator that yields new lines appended to the stream
  
  reads from the stream and waits for new data
  if no new line is available- sleeps before retrying
  """
  
  while True:
    line = stream.readline()
    
    # if no line dont appear sleep program for 0.1s
    if not line:
      time.sleep(0.1)
      continue
    
    # new line- return
    yield line

def main():
  args: argparse.Namespace = read_line_arguments()
  
  # first check if user pointed file 
  if args.file:
    # with always closing file after action
    with open(args.file, 'r', encoding='utf-8') as stream:
      tail(stream, args)
  else: # if not read from stdin
    stream: TextIO = sys.stdin
    tail(stream, args)
    
if __name__ == "__main__":
  error_hanlder(main)