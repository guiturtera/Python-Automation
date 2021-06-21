from datetime import datetime
import src.git_integration.git_deploy as git_deploy
import unittest

class TestGitDeploy(unittest.TestCase):
    def setUp(self) -> None:
        self.commit1 = git_deploy.Commit("some_hash1", "feat(some): some description here", "Guilherme", datetime.now().isoformat()) 
        self.commit2 = git_deploy.Commit("some_hash2", "fix: some description here", "Guilherme", datetime.now().isoformat()) 
        self.commit3 = git_deploy.Commit("some_hash3", "release(text): some description here", "Guilherme", datetime.now().isoformat()) 

    #def test_Commit_get_message_info(self):
    #    self.assertEqual("feat", self.commit1._get_message_info(self.commit1.type)[0])
    #    self.assertEqual("fix", self.commit2._get_message_info(self.commit2.type)[0])
    #    self.assertEqual("release", self.commit3._get_message_info(self.commit3.type)[0])
    #    self.assertEqual("some description here", self.commit1._get_message_info(self.commit1.message)[1])
    #    self.assertEqual("some description here", self.commit2._get_message_info(self.commit2.message)[1])
    #    self.assertEqual("some description here", self.commit3._get_message_info(self.commit3.message)[1])

    

    #def test_get_branch_path(self):
    #   self.assertEqual("", "NOT IMPLEMENTED YET")

if __name__ == '__main__':
    unittest.main()