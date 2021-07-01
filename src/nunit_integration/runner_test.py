import subprocess

from abc import ABC, abstractmethod

class RunnerTest(ABC):
    @abstractmethod
    def run(self, parameters) -> str:
        pass

    def _run_script(self, command) -> tuple[bool, str]:
        p1 = subprocess.Popen(command, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p1.wait()
        out, err = p1.communicate()
        out = out.decode(errors="ignore")
        err = err.decode(errors="ignore")

        if exit_code == 0: success = True 
        else: success = False
        output = f"{out}\r\n{err}"

        return (success, output)
        

