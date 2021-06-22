import unittest
import os
import sys
from src.git_integration.git_manager import Commit

class TestCommit(unittest.TestCase):
    def setUp(self) -> None:
    #    self.available_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'available-commits.txt')
        self.available_path_text = 'feat|fix|release'
    #    self.create_available_path()

    # ainda adicionara um app config
    def test_split_commit_msg(self):
        description_test = 'some description here'
        self.assertEqual(( True, 'feat', description_test ), Commit.split_commit_msg(None, f"feat(some): {description_test}", { 'feat', 'fix' }))
        self.assertEqual(( True, 'fix', description_test ), Commit.split_commit_msg(None, f"fix(some): {description_test}", { 'feat', 'fix' }))
        self.assertEqual(( True, 'fix', description_test ), Commit.split_commit_msg(None, f"fix: {description_test}", { 'feat', 'fix' }))
        self.assertEqual(( True, 'aux', description_test ), Commit.split_commit_msg(None, f"aux(some): {description_test}", { 'feat', 'aux' }))
        self.assertEqual(( False, '', '' ), Commit.split_commit_msg(None, f"Feat(some):{description_test}", { 'feat', 'fix' }))
        self.assertEqual(( False, '', '' ), Commit.split_commit_msg(None, f"release(some): {description_test}", { 'feat', 'fix' }))
        self.assertEqual(( False, '', '' ), Commit.split_commit_msg(None, f"release: {description_test}", { 'feat', 'fix' }))

        
    #def test_get_available_commits(self):
    #    self.assertEqual({ 'feat', 'fix', 'release' }, Commit.get_available_commits(None, self.available_path))
    
    #def create_available_path(self):
    #    with open(self.available_path, 'w', encoding='utf-8') as f:
    #        f.write(self.available_path_text)

    #def tearDown(self) -> None:
        # os.remove(self.available_path)


if __name__ == '__main__':
    unittest.main()