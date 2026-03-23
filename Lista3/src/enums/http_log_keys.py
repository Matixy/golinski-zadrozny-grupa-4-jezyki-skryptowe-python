from enum import Enum

class HTTP_LOG_KEYS(Enum):
  TS: str = 'ts'
  UID: str = 'uid' 
  ID_ORIG_H: str = 'ip'
  ID_ORIG_P: str = 'id.orig_p' 
  ID_RESP_H: str = 'id.resp_h' 
  ID_RESP_P: str = 'id.resp_p' 
  METHOD: str = 'method' 
  HOST: str = 'host' 
  URI: str = 'uri' 
  STATUS_CODE: str = 'status_code'