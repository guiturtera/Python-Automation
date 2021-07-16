import os
import shutil
import subprocess

from interfaces.request import Request

class DeployRunner():
    def __init__(self, resources_path: str, request: Request, SDCard_name: str = "SD Card") -> None:
        self.request = request
        self.request.query = "dir_to_copy=|sd card|flashdisk"
        self.SDCard_name = SDCard_name
        self.resources_path = resources_path
        self.remote_dir = f'//{self.request.ip_adress}/{self.SDCard_name}'
        self.remote_dir_to_create = f'{self.remote_dir}/flashdisk'

    def run(self):
        validateRes = self._verify_connection()
        if not validateRes["Success"]: return validateRes
        self._delete_if_exists(self.remote_dir_to_create)

        response = self._efficient_copytree(self.resources_path, self.remote_dir_to_create)
        if not response[0]:
            #shutil.copytree(self.resources_path, self.remote_dir_to_create, dirs_exist_ok=True, ignore=True)
            return {
                "Success": False,
                "Message": f"Error copying content to SD Card\nsrc -> {self.resources_path}\ndst -> {self.remote_dir_to_create}",
                "ErrorMessage": "",
                "ExitCode": response[1]
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
        
    def _delete_if_exists(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
            
        os.mkdir(dir)

    def _efficient_copytree(self, src, dst):
        #try:
         #   shutil.copytree(src, dst, dirs_exist_ok=True, ignore_dangling_symlinks=True)
        #except Exception as ex:
         #   return (False, ex.args)

        src = os.path.normpath(src).replace('/', '\\')
        dst = os.path.normpath(dst).replace('/', '\\')
        args = ["xcopy", src, dst, "/Y", "/E", "/Q"]
        proc = subprocess.Popen(args)
        exit_code = proc.wait()
        return (exit_code == 0, exit_code)