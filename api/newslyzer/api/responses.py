import json

from flask import Response

class JSON(Response):
    def __init__(self, *args, **kwargs):
        if 'response' in kwargs:
            if type(kwargs['response']) != str:
                kwargs['response'] = json.dumps(kwargs['response']).encode("utf-8")

        kwargs['content_type'] = "application/json"
        super(JSON, self).__init__(*args, **kwargs)

class CSV(Response):
    def __init__(self, *args, **kwargs):
        if 'response' in kwargs:
            res = "\n".join(['|'.join([str(el) for el in row]) for row in kwargs['response']])
            kwargs['response'] = res.encode("utf-8")

        kwargs['content_type'] = "text/csv"
        super().__init__(*args, **kwargs)
