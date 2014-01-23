class SafetyException(Exception):
    pass

class NotSafeException(SafetyException):
    pass
class NotInstantiatedException(SafetyException):
    pass
