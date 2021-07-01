from abc import ABC, abstractmethod


class Request(ABC): # "pages/functionaltests.cgi"
    def __init__(self, ip_adress: str, url_path: str, query: str, port_number: int = 5000, login: str = "", password: str = "") -> None:
        self.ip_adress = ip_adress
        self.url_path = url_path
        self.query = query
        self.port_number = port_number
        self.login = login
        self.password = password

    @abstractmethod
    def getjson(self):
        """Get the response from the specified Request"""
        pass