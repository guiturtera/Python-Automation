import os
import shutil

from interfaces.request import Request
from urllib3.exceptions import ProtocolError

class GoldenImageRunner():
    def __init__(self, database_address: str, request: Request, version: str, SDCard_name: str = "SD Card") -> None:
        self.request = request
        self.version = version
        self.SDCard_name = SDCard_name
        self.database_path = database_address
        self.database_path_to_copy = os.path.join(self.database_path, "release-" + version)
        self.remote_dir = f'//{self.request.ip_adress}/{self.SDCard_name}'
        self.golden_image_path = f'{self.remote_dir}/golden_image/flashbackup.bin'

    def run(self):
        validateRes = self._verify_connection()
        if not self._verify_connection()["Success"]: return validateRes
        validateRes = self._verify_remote()
        if not self._verify_remote()["Success"]: return validateRes

        res = self.request.getjson()
        if self._verify_success(res):
            res["ErrorMessage"] = "" # Success in the flashdisk bk
            res["Success"], res["Message"], res["ExitCode"] = self._copy_to_database()

        return res
        # An exception is expected when Golden Image is over, because the flashdisk will be unaccessable until toradex reboot.

    def _verify_success(self, res):
        if type(res["ErrorMessage"][0]) is ProtocolError:
            if os.path.exists(self.golden_image_path):
                return True
            else:
                res["Message"] = f"Path {self.golden_image_path} does not exist!"
                res["ExitCode"] = 1
        return False

    def _verify_connection(self):
        if os.path.exists(self.remote_dir):
            return { "Success": True }
        return {
                "Success": False,
                "Message": f"Connection via remote failed at {self.remote_dir}",
                "ErrorMessage": "",
                "ExitCode": "" 
            }

    def _copy_to_database(self):
        src = os.path.dirname(self.golden_image_path)
        dst = self.database_path_to_copy
        if os.path.isdir(self.database_path):
            try: 
                shutil.copytree(src, dst)
                return (True, f"Success to copy files!\n{dst}", 0)
            except OSError as err:
                return (False, f"Golden image already exists for this version! + {self.version}", 17)
            except Exception as err:
                return (False, f"Failed copying files to + {dst}", 17)
        else:
           return (False, f"Database dir does not exist.\n{dst}", 1)
  
    def _verify_remote(self):
        if not os.path.exists(self.database_path_to_copy):
            return { "Success": True }
        
        return {
                "Success": False,
                "Message": f"Golden image of this version already exists! {self.database_path_to_copy}",
                "ErrorMessage": "",
                "ExitCode": "" 
            }