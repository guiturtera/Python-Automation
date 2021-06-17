from datetime import datetime
from colorama import Fore, Style
import subprocess
import json
import sys
import os

def call_ms_build(msbuild_path, project_full_path, arguments):
    result = subprocess.run(
        [msbuild_path, project_full_path, "-target:Rebuild", "-property:Configuration=Release", "-clp:ErrorsOnly;NoItemAndPropertyList", "-verbosity:quiet", "-nologo"],
         capture_output=True, text=True
    )

    if result.stdout == "":
        print(Fore.GREEN, f"{project_full_path} Success to build!" + Style.RESET_ALL)
    else:
        print(Fore.RED, f"{project_full_path} Failed to build!" + Style.RESET_ALL)
        raise SystemExit(f"FAILED TO BUILD {project_full_path}")

def write_assembly(src_path, default_assembly, project_name, app_config):
    path_to_write = os.path.join(src_path, project_name, "src", "Properties", "AssemblyInfo.cs")
    
    description = f"Wrapper for {project_name}"
    year = datetime.now().year
    data_to_write = default_assembly.format(project_name, description, app_config["company_name"], year, app_config["version_info"])
    
    with open(path_to_write, "w", encoding="utf-8") as file:
        file.write(data_to_write)


def load_default_assembly():
    # project_name, description, company_name, year, version
    with open("default_assembly.txt", "r", encoding="utf-8") as file:
        default_assembly = file.read()
    return default_assembly

def build_folder_recursively(folder_to_build, default_assembly, app_config):
    for project in os.listdir(folder_to_build):
        if os.path.isdir(os.path.join(folder_to_build, project)):
            write_assembly(folder_to_build, default_assembly, project, app_config)
            call_ms_build(app_config["msbuild_path"], os.path.join(folder_to_build, project, "src", f"{project}.csproj"), "a")

def load_app_config():
    with open('..\\appconfig.json', 'r', encoding="utf-8") as file:
        app_config = json.load(file)
    return app_config


try:
    app_config = load_app_config()
    default_assembly = load_default_assembly()

    build_folder_recursively(os.path.abspath("..\\src\\"), default_assembly, app_config)
    build_folder_recursively(os.path.abspath("..\\tests\\"), default_assembly, app_config)

except:
    with open(app_config["output_path"], "w", encoding="utf-8") as file:
        file.write(sys.exc_info()[0])
    raise SystemExit(1)






