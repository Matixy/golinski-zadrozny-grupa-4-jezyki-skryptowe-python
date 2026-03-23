from enum import Enum

class SESSION_LOG_KEYS(Enum):
  UID: str = 'uid' 
  HOSTS: str = 'hosts'
  REQUEST_NUMBER: str = 'req_num'
  REQUEST_FIRST: str = 'req_first'
  REQUEST_LAST: str = 'req_last'
  METHODS_RATIO: str = 'methods_ratio'
  SUCCES_METHODS_RATIO = '2xx methods ratio'
