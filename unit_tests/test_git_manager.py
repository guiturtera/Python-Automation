import os
import sys

from datetime import datetime
from src.git_integration.git_manager import GitManager, Commit
import unittest

class TestGitManager(unittest.TestCase):
    def setUp(self) -> None:
        now = datetime.now().isoformat()
        self.raw_commit = [f'hash1|fix(aux): First fix commit|name1|{now}', f'hash2|fix: Second fix commit|name2|{now}', f'hash4|feat(aux): First feature commit|name2|{now}', f'hash5|feat: Second feature commit|name2|{now}' ]
        self.commit_dic = { 
            "fix":
            [ Commit("hash1", "name1", 'fix(aux): First fix commit', now),
            Commit("hash2", "name2", 'fix: Second fix commit', now), ],
            "feat":
            [ Commit("hash4", "name2", 'feat(aux): First feature commit', now),
            Commit("hash5", "name2", 'feat: Second feature commit', now) ]
            }

    def test___get_organized_commits_dic(self):
        #self.maxDiff=None
        result = GitManager._GitManager__get_organized_commits_dic(None, self.raw_commit)
        for key in self.commit_dic.keys():
            for i in range(len(self.commit_dic[key])):
                print(self.commit_dic[key][i])
                print(result[key][i])
                #self.assertEqual(self.commit_dic[key][i].hash, result[key][i].hash)
                #self.assertEqual(self.commit_dic[key][i].type, result[key][i].type)
                #self.assertEqual(self.commit_dic[key][i].date, result[key][i].date)
                #self.assertEqual(self.commit_dic[key][i].description, result[key][i].description)
                #self.assertEqual(self.commit_dic[key][i].valid, result[key][i].valid)


if __name__ == '__main__':
    unittest.main()