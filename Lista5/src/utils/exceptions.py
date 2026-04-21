class CliAppError(Exception):
    pass

class DataNotFoundError(CliAppError):
    pass

class StationNotExist(CliAppError):
    pass



