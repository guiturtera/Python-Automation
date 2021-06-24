from datetime import datetime
import os
from src.git_integration.version_handler import VersionHandler
import unittest
import shutil
from src.build_integration.msbuild import Msbuild
from src.git_integration.git_manager import Commit
from src.build_integration.recursive_build import RecursiveBuilder

from src.build_integration.msbuild import Msbuild

class TestRecursiveBuilder(unittest.TestCase):
    def setUp(self) -> None:
        try:
            self.current_dir = os.path.dirname(__file__)
            self.mock_dir = os.path.join(self.current_dir, "mock")
            self.properties_mock = os.path.join(self.mock_dir, "properties")
            self.assembly_mock = os.path.join(self.properties_mock, "assemblyinfo.cs")
            self.version_info_path = os.path.join(self.mock_dir, "versioninfo.txt")

            os.mkdir(self.mock_dir)
            os.mkdir(self.properties_mock)
            self.default_assembly_mock = '{project_name}, {description}, {company_name}, {project_name}, {year}'

            with open(self.version_info_path, "w", encoding='utf-8') as f:
                f.write("v1.0.0")

            with open(self.assembly_mock, "w", encoding='utf-8') as f:
                f.write(self.default_assembly_mock)

            now = datetime.now().isoformat()
            self.commit_dic = { 
                "fix":
                [ Commit("hash1", 'fix(aux): First fix commit', 'name1', now),
                Commit("hash2", 'fix: Second fix commit', "name2", now), ],
                "feat":
                [ Commit("hash4", 'feat(aux): First feature commit', "name2", now),
                Commit("hash5", 'feat: Second feature commit', "name2", now) ]
                }

            self.msbuildtest = Msbuild(self.mock_dir, "", VersionHandler(self.version_info_path, self.commit_dic), "Presys")
            self.recursivebuild_test = RecursiveBuilder(self.msbuildtest)

        except: 
            shutil.rmtree(self.mock_dir)

    def test___convert_multiple_pattern(self):
        type_test = "aux\\aux2\\aux3\\{project_name}\\aux4\\aux5"
        self.assertEqual([ "aux\\aux2\\aux3", "aux4\\aux5" ], RecursiveBuilder._RecursiveBuilder__convert_multiple_pattern(None, type_test))
        try:
            type_test = "aux\\aux2\\aux3\\aux4\\aux5"
            RecursiveBuilder._RecursiveBuilder__convert_multiple_pattern(None, type_test)
        except Exception as ex:
            self.assertEqual(ex.args[0], 'Wrong pattern! {project_name} not specified')

    def test___build_patterns(self):
        self.__create_mock_proj()

        self.assertEqual(["src\\project_1\\src\\project_1.csproj", "src\\project_2\\src\\project_2.csproj"], self.recursivebuild_test._RecursiveBuilder__build_patterns("src/{project_name}/src"))

        try:
            self.recursivebuild_test._RecursiveBuilder__build_patterns("src")
        except Exception as ex:
            self.assertEqual('Wrong pattern! {project_name} not specified', ex.args[0])

        try:
            self.assertRaises(Exception, self.recursivebuild_test._RecursiveBuilder__build_patterns("src/{project_name}/a"))
        except Exception as ex:
            expected_path = os.path.join(self.mock_dir, "src", "project_1", "a")
            self.assertEqual(f"Folder {expected_path} not exists!", ex.args[0])

        try:
            self.assertRaises(Exception, self.recursivebuild_test._RecursiveBuilder__build_patterns("sr/{project_name}"))
        except Exception as ex:
            expected_path = os.path.join(self.mock_dir, "sr")
            self.assertEqual(f"Folder {expected_path} not exists!", ex.args[0])



    def __create_mock_proj(self):
        src_dir = os.path.join(self.mock_dir, 'src')
        project_1 = os.path.join(src_dir, 'project_1')
        project_2 = os.path.join(src_dir, 'project_2')
        somte_txt_path = os.path.join(src_dir, 'some_txt.txt')
        src_project1 = os.path.join(project_1, 'src')
        src_project2 = os.path.join(project_2, 'src')
        proj1_path = os.path.join(src_project1, 'project_1.csproj')
        proj2_path = os.path.join(src_project2, 'project_2.csproj')
        
        os.mkdir(src_dir)
        os.mkdir(project_1)
        os.mkdir(project_2)
        os.mkdir(src_project1)
        os.mkdir(src_project2)

        with open(proj1_path, "w", encoding='utf-8') as f:
            f.write("hello world")
        with open(proj2_path, "w", encoding='utf-8') as f:
            f.write("hello world")
        with open(somte_txt_path, "w", encoding='utf-8') as f:
            f.write("hello world")

    def tearDown(self) -> None:
        shutil.rmtree(self.mock_dir)

if __name__ == '__main__':
    unittest.main()