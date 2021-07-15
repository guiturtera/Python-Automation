import os
import shutil
import subprocess

from interfaces.request import Request

class DeployRunner():
    def __init__(self, resources_path: str, request: Request, SDCard_name: str = "SD Card") -> None:
        self.request = request
        self.SDCard_name = SDCard_name
        self.resources_path = resources_path
        self.remote_dir = f'//{self.request.ip_adress}/{self.SDCard_name}'
        self.remote_dir_to_create = f'{self.remote_dir}/flashdisk'

    def run(self):
        validateRes = self._verify_connection()
        if not validateRes["Success"]: return validateRes
        self.create_and_delete_if_exists(self.remote_dir_to_create)

        try:
            shutil.copytree(self.resources_path, self.remote_dir_to_create, dirs_exist_ok=True)
        except Exception as ex:
            return {
                "Success": False,
                "Message": f"Error copying content to SD Card\nsrc -> {self.resources_path}\ndst -> {self.remote_dir_to_create}",
                "ErrorMessage": ex.args,
                "ExitCode": 100
            }
            

        return self.request.getjson()

    def _verify_connection(self):
        if os.path.exists(self.remote_dir):
            return { "Success": True }
        return {
                "Success": False,
                "Message": f"Could not access {self.remote_dir}",
                "ErrorMessage": "",
                "ExitCode": "" 
            }
        
    def create_and_delete_if_exists(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
        
        os.mkdir(dir)