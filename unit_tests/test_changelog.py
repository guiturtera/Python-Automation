import os
import unittest

from datetime import datetime
from src.git_integration.changelog_handler import ChangelogHandler
from src.git_integration.version_handler import VersionHandler
from src.git_integration.git_manager import Commit

class TestChangelogHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.versioninfo_path = ".\\unit_tests\\versioninfo.txt"
        self.versioninfo = "v1.0.0"
        self.create_versioninfo_mock(self.versioninfo)

        self.commit_dic = { 
            "fix":
            [ Commit("hash1", "name1", 'fix(aux): First fix commit', datetime.now().isoformat()),
            Commit("hash2", "name2", 'fix: Second fix commit', datetime.now().isoformat()),
            Commit("hash3", "name1", 'fix(aux): Third fix commit', datetime.now().isoformat()) ],
            "feat":
            [ Commit("hash4", "name2", 'feat(aux): First feature commit', datetime.now().isoformat()),
            Commit("hash5", "name2", 'feat: Second feature commit', datetime.now().isoformat()),
            Commit("hash6", "name2", 'feat(aux): Third feature commit', datetime.now().isoformat()) ],
            }
        self.changelog_mock_text = """## [v1.0.0]
        ### fix
        0b56f80|Guilherme Turtera|2021-06-18 18:12:06 -0300 -> Third feature commit
        005d2c8|Guilherme Turtera|2021-06-18 16:35:56 -0300 -> Second feature commit
        ff06ab9|Guilherme Turtera|2021-06-18 16:35:32 -0300 -> feat(aux): First feature commit
        78218e7|Guilherme Turtera|2021-06-18 16:34:54 -0300 -> fix(aux): Fourth commit fix"""
        self.changelog_mock_path = '.\\unit_tests\\changelog.md'
        self.create_changelog_mock()

        self.changelog_handler = ChangelogHandler(self.changelog_mock_path, self.commit_dic, VersionHandler(self.versioninfo_path, self.commit_dic))

    def test___load_changelog(self):
        self.assertEqual(self.changelog_mock_text, self.changelog_handler._ChangelogHandler__load_changelog(self.changelog_mock_path))

    def test___changelog_text_to_append(self):
        text = self.changelog_handler._ChangelogHandler__changelog_text_to_append(self.commit_dic, "v1.0.0")
        
    def create_changelog_mock(self):
        with open(self.changelog_mock_path, 'w', encoding='utf-8') as f:
            f.write(self.changelog_mock_text)

    def create_versioninfo_mock(self, version):
        with open(self.versioninfo_path, 'w', encoding='utf-8') as f:
            f.write(version)

    def tearDown(self):
        os.remove(self.changelog_mock_path)



if __name__ == '__main__':
    unittest.main()