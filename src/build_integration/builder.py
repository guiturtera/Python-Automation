from abc import abstractmethod

class Builder:
    def __init__(self) -> None:
        self.extension: str = ""
        self.root_project_dir: str = ""
        self.builder_path: str = ""
        pass

    @abstractmethod
    def build(self, project_file: str):
        ''' Builds the app with the specific builder and project path '''
        pass
    @abstractmethod
    def prepare_for_build(self, pattern, project_name):
        ''' Prepare all necessary tools for building the application '''
        pass