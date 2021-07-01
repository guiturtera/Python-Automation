import json

from src.interfaces.request import Request

class MockRequest(Request):
    def __init__(self, fail_test: bool, ip_adress: str, url_path: str, query: str, port_number: int = 5000, login: str = "", password: str = "") -> None:
        super().__init__(ip_adress, url_path, query, port_number, login, password)
        self.fail_test = fail_test

    def getjson(self):
        if not self.fail_test:
            return json.loads("{\"ErrorMessage\": \"some error\", \"Message\": \"1 test(s) failed!\", \"ExitCode\": 1, \"Success\": false}")
        else:
            return json.loads("{\"ErrorMessage\": \"\", \"Message\": \"success!!\", \"ExitCode\": 0, \"Success\": true}")
