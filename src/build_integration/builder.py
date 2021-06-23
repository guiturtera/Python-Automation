from abc import abstractmethod

class Builder:
    def __init__(self, root_project_dir:str, builder_path: str) -> None:
        self.root_project_dir = root_project_dir
        self.builder_path = builder_path

    @abstractmethod
    def prepare_and_build_multiple(self, pattern_from_root: str) -> bool:
        ''' If you have multiple projects inside, you can specify your project's
            default path, from the root path. ex: src/{project_name}/src
            The path src/ will be wiped and will build everything, with the folder's project_name
          '''
        pass
    @abstractmethod
    def build(self, project_file: str) -> bool:
        ''' Builds the app with the specific builder and project path '''
        pass
    @abstractmethod
    def prepare_for_build(self):
        ''' Prepare all necessary tools for building the application '''
        pass