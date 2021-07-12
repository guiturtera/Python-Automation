import requests

from interfaces.request import Request

class RequestFacade(Request):
    def __init__(self, ip_adress: str, url_path: str, query: str = "", port_number: int = 5000, login: str = "", password: str = "") -> None:
        super().__init__(ip_adress, url_path, query, port_number, login, password)

    def getjson(self):
        try:
            url = 'http://{0}:{1}/{2}?{3}'.format(self.ip_adress, self.port_number, self.url_path, self.query)
            auth = (self.login, self.password)
            res = requests.get(url, auth=auth)
            
            jsonRes = res.json()
            if jsonRes["Success"] == False:
                jsonRes["Message"] +=  f" -> {url}"

            return jsonRes
        except Exception as ex:
            return { "Success": False, "Message": "Failed -> " + url, "ErrorMessage": ex.args, "ExitCode": 110 }