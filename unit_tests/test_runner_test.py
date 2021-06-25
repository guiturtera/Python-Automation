from posixpath import dirname
import unittest
import os

from src.unittest_integration.runner_test import RunnerTest
from src.unittest_integration.nunit_unit_runner import NUnitUnitRunner

class TestTestRunner(unittest.TestCase):
    def test__run_script(self):
        self.assertEqual((False, "stdout \r\n\r\n"), RunnerTest._run_script(None, "echo stdout & exit 2"))
        self.assertEqual((True, "stdout \r\n\r\n"), RunnerTest._run_script(None, "echo stdout & exit 0"))

class TestNUnitUnitRunner(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_dir = os.path.join(os.path.dirname(__file__), 'mock')
        self.mock_file = os.path.join(self.mock_dir, 'mock.bat')
        os.mkdir(self.mock_dir)

    def mock_test_executable(self, stdout, exit_code):
        with open(self.mock_file, 'w', encoding='utf-8') as f:
            f.write(f"@echo off\necho {stdout} %*\ncd\nexit {exit_code}\n")

    def test_run_script(self):
        some_text = 'hello world'

        self.mock_test_executable(some_text, 0)
        self.assertEqual((True, f"{some_text} --noheader --noresult a b\r\n{os.path.normpath(self.mock_dir)}\r\n\r\n"), NUnitUnitRunner(self.mock_file).run(["a", "b"]))

        self.mock_test_executable(some_text, 2)
        self.assertEqual((False, f"{some_text} --noheader --noresult a b\r\n{os.path.normpath(self.mock_dir)}\r\n\r\n"), NUnitUnitRunner(self.mock_file).run(["a", "b"]))

    def tearDown(self) -> None:
        os.system('rmdir /S /Q "{}"'.format(self.mock_dir)) 

if __name__ == '__main__':
    unittest.main()