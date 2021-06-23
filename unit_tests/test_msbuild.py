from datetime import datetime
import os
from src.git_integration.version_handler import VersionHandler
import unittest
import shutil
from src.build_integration.msbuild import Msbuild
from src.git_integration.git_manager import Commit

from src.build_integration.msbuild import Msbuild

class TestVersionHandler(unittest.TestCase):
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

        except: 
            shutil.rmtree(self.mock_dir)


    def test___convert_multiple_pattern(self):
        type_test = "aux\\aux2\\aux3\\{project_name}\\aux4\\aux5"
        self.assertEqual([ "aux\\aux2\\aux3", "aux4\\aux5" ], Msbuild._Msbuild__convert_multiple_pattern(None, type_test))
        try:
            type_test = "aux\\aux2\\aux3\\aux4\\aux5"
        except Exception as ex:
            self.assertEqual('Wrong pattern! {project_name} not specified', ex.args[0])

    def test___write_assembly(self):
        expected = self.msbuildtest.default_assembly.format(project_name="mock_project", description="Wrapper for mock_project", company_name="Presys", year=datetime.now().year, version="v1.1.0")
        self.msbuildtest._Msbuild__write_assembly(self.mock_dir, "mock_project")
        with open(self.assembly_mock, "r", encoding='utf-8') as f:
            result = f.read()

        self.assertEqual(expected, result)

    def test__load_default_assembly(self):
        result = Msbuild._Msbuild__load_default_assembly(None, self.assembly_mock)
        self.assertEqual(self.default_assembly_mock, result)

    def test_build(self):
        pass

    def test_prepare_and_build_multiple(self):
        pass

    def tearDown(self) -> None:
        shutil.rmtree(self.mock_dir)

if __name__ == '__main__':
    unittest.main()