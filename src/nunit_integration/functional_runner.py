import os

from interfaces.request import Request
from nunit_integration.runner_test import RunnerTest

#class EnumExitCode(Enum):
     

class FunctionalRunner(RunnerTest):
    def __init__(self, test_path, request: Request) -> None:
        self.test_path = os.path.normpath(test_path)
        self.formatted_test_path = self.test_path.replace('/', '|')
        self.req = request

        request.query = "test_path=" + self.formatted_test_path

    def run(self, parameters: list[str] = "") -> tuple[bool, str]:
        # Nunit_Functional_API is not yet available for parameters, so will be ignored:
        # parameters = Noneres =
        
        res = self.req.getjson()
        return (res["Success"], res["Message"] + "\r\n" + res["ErrorMessage"].__str__())
        
