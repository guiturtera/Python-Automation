import re
import os
import sys
import git
from datetime import datetime
from git.repo.base import Repo

## CREATE AN APP CONFIG
class Commit:
    def __init__(self, hash, message, name, date):
        self.hash = hash
        self.message = message
        self.name = name
        self.date = date
        self.type, self.message = self._get_message_info(message)

    def __str__(self) -> str:
        return f"{self.hash}|{self.name}|{self.date} -> {self.message}"

    def _get_message_info(self, message):
        data = re.split("[\(:]", message)
        return [data[0], data[len(data) - 1].strip()]

def get_branch_path():
    if len(sys.argv) == 2 and Repo(sys.argv[1]):
        return sys.argv[1]
    else:
        return "."

def get_organized_commits_dic(commits_data):
    available_types = get_available_commits()
    dic = {}
    for type in available_types:
        dic.setdefault(type, [])

    # buf = io.StringIO()
    for log in commits_data:
        commit_list = log.split('|')  # hash|message|name lastname|date
        # print(commit_list)
        aux = Commit(commit_list[0], commit_list[1], commit_list[2], commit_list[3])
        dic[aux.type].append(aux.__str__())
    
    return dic

def get_available_commits():
    with open(".\\available-commit-msg.txt", "r", encoding="utf-8") as file:
        content = file.read().split('|')
    return content

def get_last_release_date(gitHandler):
    strIso = (gitHandler.log("-n 1", "--grep=release", "--oneline", "--pretty=%ci")).replace(" -0300", "")   # default -0300 from git
    aux = datetime.fromisoformat(strIso) # git default
    aux = aux.replace(second = aux.second + 1)
    return aux

def get_last_commits_log(gitHandler):
    return gitHandler.log("--date=short", f"--since={get_last_release_date(gitHandler)}", "--oneline", "--pretty=%h|%s|%cN|%ci")

def main():   
    gitHandler = git.Git(get_branch_path())

    commits_data = get_last_commits_log(gitHandler).split('\n')
    organized_commits = get_organized_commits_dic(commits_data)

    print(organized_commits)
