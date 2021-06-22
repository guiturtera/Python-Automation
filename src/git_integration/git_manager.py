import re
import sys
import git
from git.repo.base import Repo
from datetime import datetime

class GitManager():
    def __init__(self, repo_directory) -> None:
        self.repo_directory = repo_directory
        self.gitHandler = git.Git(repo_directory)
        #if not Repo(repo_directory).bare:
        #    raise Exception('Not a single git repo!')

    def __get_last_release_date(self):
        strIso = (self.gitHandler.log("-n 1", "--grep=release", "--oneline", "--pretty=%ci")).replace(" -0300", "")   # default -0300 from git
        aux = datetime.fromisoformat(strIso) # git default
        aux = aux.replace(second = aux.second + 1)
        return aux
    
    def get_commits_since_last_release(self):
        commits_data = self.__get_commits_log_since_last_release().split('\n')
        return self.__get_organized_commits_dic(commits_data) # get from app config

    def __get_commits_log_since_last_release(self):
        return self.gitHandler.log("--date=short", f"--since={self.__get_last_release_date()}", "--oneline", "--pretty=%h|%s|%cN|%ci")

    def __get_organized_commits_dic(self, commits_data):
        dic = {}
        for log in commits_data:
            commit_list = log.split('|')  # hash|message|name lastname|date
            current_commit = Commit(commit_list[0], commit_list[1], commit_list[2], commit_list[3])

            if current_commit.valid:
                if not dic.__contains__(current_commit.type):
                    dic.setdefault(current_commit.type, [])

                dic[current_commit.type].append(current_commit)
            else:
                raise Exception(f'{current_commit.hash} -> Commit message [{current_commit.message}] invalid!')
        
        return dic # {type, Commit[]}

## CREATE AN APP CONFIG
class Commit:
    def __init__(self, hash, message, name, date):
        self.hash = hash
        self.message = message
        self.name = name
        self.date = date
        self.valid, self.type, self.description = self.split_commit_msg(message, { 'improvement', 'refactor', 'grunt', 'feat', 'test', 'docs', 'fix', 'api' })

    def __str__(self) -> str:
        return f"{self.description} -> {self.hash}|{self.name}|{self.date}"

    # use with app config
    #def get_available_commits(self, available_commits_path):
    #    with open(available_commits_path, "r", encoding="utf-8") as file:
    #        content = file.read().split('|')
    #    return set(content)

    def split_commit_msg(self, message, available_types_dic):
        try:
            data = re.split("[\(:]", message)
            type, description = [ data[0], data[len(data) - 1].strip() ]
            if available_types_dic.__contains__(type) and re.match(type + "(\(.{3,15}\))?: .{10,}", message):
                return ( True, type, description )
            else:
                return ( False, '', '' )
        except:
            return ( False, '', '' )