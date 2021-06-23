import os
import sys
from datetime import datetime
from src.git_integration.git_manager import Commit
from src.git_integration.version_handler import VersionHandler
import unittest

class TestVersionHandler(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test___convert_multiple_pattern(self):
        pass

    def test___write_assembly(self):
        pass

    def test__load_default_assembly(self):
        pass

    def test_build(self):
        pass

    def test_prepare_and_build_multiple(self):
        pass

    def tearDown(self) -> None:
        os.remove(self.versioninfo_path)

if __name__ == '__main__':
    unittest.main()