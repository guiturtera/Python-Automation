from datetime import datetime
from build_integration.builder import Builder
from colorama import Fore, Style
import subprocess
import json
import sys
import os
from git_integration.version_handler import VersionHandler

class Msbuild(Builder):
    # Msbuild_path
    def __init__(self, root_project_dir: str, builder_path: str, version_info: VersionHandler, company_name="") -> None:
        super().__init__()
        self.root_project_dir = root_project_dir
        self.builder_path = builder_path
        self.default_assembly = self.__load_default_assembly(os.path.join(os.path.dirname(__file__), 'default_assemblies', 'msbuild'))
        self.version_info = version_info.get_next_version_for_assembly()
        self.company_name = company_name
        self.extension = ".csproj"

    def prepare_for_build(self, pattern):
        project_path = os.path.normpath(os.path.join(self.root_project_dir, os.path.dirname(pattern)))
        project_file = os.path.normpath(os.path.join(self.root_project_dir, pattern))
        project_name = self.__get_project_name(project_file)
        self.__write_assembly(project_path, project_name)

    def build(self, pattern: str):
        project_file = os.path.normpath(os.path.join(self.root_project_dir, pattern))
        result = subprocess.run(
            [self.builder_path, project_file, "-target:Rebuild", "-property:Configuration=Release", "-clp:ErrorsOnly;NoItemAndPropertyList", "-verbosity:quiet", "-nologo"],
            capture_output=True, text=True
        )

        if result.stdout == "":
            return f"{project_file} Success to build!"
            # print(Fore.GREEN, f"{project_file} Success to build!" + Style.RESET_ALL)
        else:
            raise Exception(f"Failed to build!\n{result.stdout}")
            # print(Fore.RED, f"{project_file} Failed to build!" + Style.RESET_ALL)
            # raise SystemExit(f"FAILED TO BUILD {project_file}")

    def __get_project_name(self, project_file) -> str:
        project_file_name = os.path.basename(project_file)
        if os.path.isfile(project_file) and project_file_name.__contains__(self.extension):
            return project_file_name.removesuffix(self.extension)
        else:
            raise Exception(f"Invalid project path -> {project_file}")

    def __write_assembly(self, project_path, project_name):
        try:
            path_to_write = os.path.join(project_path, "Properties", "AssemblyInfo.cs")
            
            description = f"Wrapper for {project_name}"
            year = datetime.now().year
            data_to_write = self.default_assembly.format(
                project_name=project_name, description=description, company_name=self.company_name, year=year, version=self.version_info)
            
            with open(path_to_write, "w", encoding="utf-8") as file:
                file.write(data_to_write)
        except:
            raise Exception(f"Invalid project path! {project_path}")

    def __load_default_assembly(self, default_assembly_path) -> str:
        with open(default_assembly_path, "r", encoding="utf-8") as file:
            default_assembly = file.read()  # project_name, description, company_name, year, version
        return default_assembly
       
