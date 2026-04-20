class CliAppError(Exception):
    pass

class InvalidDateError(CliAppError):
    pass

class DataNotFoundError(CliAppError):
    pass

class StationNotExist(CliAppError):
    pass

class CalculationError(CliAppError):
    pass

