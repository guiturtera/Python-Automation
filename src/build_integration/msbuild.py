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
        super().__init__(root_project_dir, builder_path)
        self.default_assembly = self.__load_default_assembly(os.path.join(os.path.dirname(__file__), 'default_assemblies', 'msbuild'))
        self.version_info = version_info.new_version
        self.company_name = company_name


    def build(self, project_file: str):
        result = subprocess.run(
            [self.builder_path, project_file, "-target:Rebuild", "-property:Configuration=Release", "-clp:ErrorsOnly;NoItemAndPropertyList", "-verbosity:quiet", "-nologo"],
            capture_output=True, text=True
        )

        if result.stdout == "":
            return f"{project_file} Success to build!"
            # print(Fore.GREEN, f"{project_file} Success to build!" + Style.RESET_ALL)
        else:
            raise Exception("Failed to build!")
            # print(Fore.RED, f"{project_file} Failed to build!" + Style.RESET_ALL)
            # raise SystemExit(f"FAILED TO BUILD {project_file}")

    def __write_assembly(self, project_path, project_name):
        path_to_write = os.path.join(project_path, "Properties", "AssemblyInfo.cs")
        
        description = f"Wrapper for {project_name}"
        year = datetime.now().year
        data_to_write = self.default_assembly.format(
            project_name, description, self.company_name, year, self.version_info)
        
        with open(path_to_write, "w", encoding="utf-8") as file:
            file.write(data_to_write)

    def __load_default_assembly(self, default_assembly_path) -> str:
        # project_name, description, company_name, year, version
        with open(default_assembly_path, "r", encoding="utf-8") as file:
            default_assembly = file.read()
        return default_assembly

    def prepare_and_build_multiple(self, pattern_from_root: str):
        wipe_path, standard_path = __convert_multiple_pattern(pattern_from_root)
        wipe_path = os.path.join(self.root_project_dir, wipe_path)
        standard_path = os.path.join(self.root_project_dir, standard_path)

        for project in os.listdir(wipe_path):
            if os.path.isdir(os.path.join(wipe_path, project)):
                project_folder = os.path.join(wipe_path, project, standard_path)
                project_path = os.path.join(project_folder, f"{project}.csproj")

                __write_assembly(project_folder, project)
                build(project_path)

    def __convert_multiple_pattern(self, pattern_from_root: str) -> tuple[str, str]:
        if not pattern_from_root.__contains__('{project_name}'):
            raise Exception('Wrong pattern! {project_name} not specified')
        
        aux = os.path.normpath(pattern_from_root)
        aux = aux.split(os.sep)
        return_tuple = [ "", "" ]

        index = 0
        for i in aux:
            if i == "{project_name}":
                index += 1
            else:
                return_tuple[index] = os.path.join(return_tuple[index], i)
        
        return return_tuple
