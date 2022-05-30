import json
from json import JSONEncoder
class ObjectDTO:
    def __init__(self, listTeacher,listClass ):
        self.listTeacher = listTeacher
        self.listClass = listClass

class ObjectDTOEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__