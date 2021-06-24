from build_integration.builder import Builder
import os
import io

class RecursiveBuilder(Builder):
    def __init__(self, builder: Builder) -> None:
        super().__init__()
        self.builder = builder
        self.builder_path = builder.builder_path
        self.root_project_dir = builder.root_project_dir
        self.extension = self.builder.extension

    def build(self, pattern: str):
        buffer = io.StringIO()
        patterns_list = self.__build_patterns(pattern)
        for i in patterns_list:
            buffer.write(self.builder.build(i))
            buffer.write('\n')

        return buffer.getvalue()

    def prepare_for_build(self, pattern: str):
        patterns_list = self.__build_patterns(pattern)
        for i in patterns_list:
            self.builder.prepare_for_build(i)


    def __build_patterns(self, pattern: str):
        previous_path, after_path = self.__convert_multiple_pattern(pattern)
        wipe_path = os.path.join(self.root_project_dir, previous_path)
        #standard_path = os.path.join(self.root_project_dir, standard_path)
        if not os.path.isdir(wipe_path):
            raise Exception(f"Folder {wipe_path} not exists!")

        memory_list = []
        for project in os.listdir(wipe_path):
            project_folder = os.path.join(wipe_path, project)
            complete_project_folder = os.path.join(project_folder, after_path)
            if os.path.isdir(project_folder):
                if os.path.exists(complete_project_folder):
                    pattern = os.path.join(previous_path, project, after_path, f"{project}{self.extension}")
                    memory_list.append(pattern)
                else:
                    raise Exception(f"Folder {complete_project_folder} not exists!")

        if len(memory_list) == 0:
            raise Exception("No projects found!")

        return memory_list

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