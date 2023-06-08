#  Copyright (c) 2021. Copyright belongs to evoflow team

import uuid
from json import JSONEncoder

import json_tricks as json


class BaseObject:
    """
    Base object of all things
    """

    def __init__(self, name=None, **kwargs):
        self.name = f"{self.__class__.__name__} {name}"
        self.id = uuid.uuid4().hex
        for key, value in kwargs.items():
            setattr(self, key, value)

    def summary(self, **kwargs):
        info = self.__info__(**kwargs)
        info["name"] = self.name
        json_string = json.dumps(info, ensure_ascii=False, indent=2)
        return json_string

    def kill(self, **kwargs):
        pass

    def __info__(self) -> dict:
        """

        @rtype: return object info to display or log
        @param kwargs:
        """
        return {"name": self.name}

    def to_json(self):
        data = self.__dict__
        json_string = json.dumps(data, ensure_ascii=False, indent=2)
        return json_string

    class Encoder(JSONEncoder):
        def default(self, o):
            return o.to_dict()

    def to_dict(self):
        return self.__dict__
