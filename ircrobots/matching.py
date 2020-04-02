from typing import List
from irctokens import Line
from .numerics import NUMERIC_NAMES

class ResponseParam(object):
    def match(self, arg: str) -> bool:
        return False

class BaseResponse(object):
    def match(self, line: Line) -> bool:
        return False

class Numerics(BaseResponse):
    def __init__(self,
            numerics: List[str]):
        self._numerics = [NUMERIC_NAMES.get(n, n) for n in numerics]

    def match(self, line: Line):
        return line.command in self._numerics

class Response(BaseResponse):
    def __init__(self,
            command: str,
            params:  List[ResponseParam]):
        self._command = command
        self._params  = params

    def match(self, line: Line) -> bool:
        if line.command == self._command:
            for i, param in enumerate(self._params):
                if (i >= len(line.params) or
                        not param.match(line.params[i])):
                    return False
            else:
                return True
        else:
            return False

class ResponseOr(BaseResponse):
    def __init__(self, *responses: BaseResponse):
        self._responses = responses
    def match(self, line: Line) -> bool:
        for response in self._responses:
            if response.match(line):
                return True
        else:
            return False

class ParamAny(ResponseParam):
    def match(self, arg: str) -> bool:
        return True
class ParamLiteral(ResponseParam):
    def __init__(self, value: str):
        self._value = value
    def match(self, arg: str) -> bool:
        return self._value == arg
class ParamNot(ResponseParam):
    def __init__(self, param: ResponseParam):
        self._param = param
    def match(self, arg: str) -> bool:
        return not self._param.match(arg)