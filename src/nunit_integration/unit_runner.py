import os
from enum import Enum

from nunit_integration.runner_test import RunnerTest

#class EnumExitCode(Enum):
     

class UnitRunner(RunnerTest):
    def __init__(self, test_path: str) -> None:
        self.test_path = test_path
        pass

    def run(self, parameters: list[str]) -> tuple[bool, str]:
        test_dir = os.path.dirname(self.test_path)

        command = f"cd /d \"{test_dir}\" & \"{self.test_path}\""

        for i in parameters:
            command += f" {i}"

        command = f"{command} --noheader --noresult & exit /b %errorlevel%"

        return self._run_script(command)