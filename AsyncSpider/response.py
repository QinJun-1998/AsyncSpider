import json


class Response:
    def __init__(self, raw_data):
        self.text = raw_data['text']
        self.content = raw_data['content']
        self.status_code = raw_data['status']
        self.headers = raw_data['headers']

    def json(self):
        return json.loads(self.text)
