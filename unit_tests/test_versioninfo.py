import os
import sys
from datetime import datetime
from src.git_integration.git_manager import Commit
from src.git_integration.version_handler import VersionHandler
import unittest

class TestVersionHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.versioninfo_path = ".\\unit_tests\\versioninfo.txt"
        self.versioninfo = "v1.0.0"
        self.create_versioninfo_mock(self.versioninfo)
        self.commit_dic = { 
            "fix":
            [ Commit("hash1", "name1", 'fix(aux): First fix commit', datetime.now().isoformat())], 
            "feat":
            [ Commit("hash4", "name2", 'feat(aux): First feature commit', datetime.now().isoformat())]
            }

    def test___get_version(self):
        self.assertEqual(self.versioninfo, VersionHandler._VersionHandler__get_current_version(None, self.versioninfo_path))

        self.create_versioninfo_mock('v1.0.2')
        try:
            VersionHandler._VersionHandler__get_current_version(None, self.versioninfo_path)
        except Exception as ex:
            self.assertEqual('Version info path invalid! Format must be vx.y.z', ex.args[0])

    def test___get_next_version(self):
        handler = VersionHandler(self.versioninfo_path)
        self.assertEqual('v1.1.3', handler._VersionHandler__get_next_version("v1.1.2", { 'fix': None }))
        self.assertEqual('v1.2.0', handler._VersionHandler__get_next_version("v1.1.2", { 'feat': None }))
        self.assertEqual('v2.0.0', handler._VersionHandler__get_next_version("v1.1.2", { 'api': None }))
        self.assertEqual('v2.0.0', handler._VersionHandler__get_next_version("v1.1.2", { 'api': None, 'feat': None }))
        self.assertEqual('v2.0.0', handler._VersionHandler__get_next_version("v1.1.2", { 'api': None, 'fix': None}))
        self.assertEqual('v1.2.0', handler._VersionHandler__get_next_version("v1.1.2", { 'feat': None, 'fix': None }))
        self.assertEqual('v2.0.0', handler._VersionHandler__get_next_version("v1.1.2", { 'feat': None, 'fix': None, 'api': None }))

    def test___format_xyz(self):
        self.assertEqual("v1.0.2", VersionHandler._VersionHandler__format_xyz(None, 1, 0, 2))

    def test___get_xyz(self):
        self.assertEqual(['1', '0', '2'], VersionHandler._VersionHandler__get_xyz(None, "v1.0.2"))

    def create_versioninfo_mock(self, version):
        with open(self.versioninfo_path, 'w', encoding='utf-8') as f:
            f.write(version)

    def tearDown(self) -> None:
        os.remove(self.versioninfo_path)

if __name__ == '__main__':
    unittest.main()