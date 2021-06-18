import re
import io
import os
import git
from git.objects import commit

class Commit:
    def __init__(self, hash, message, name, date):
        self.hash = hash
        self.message = message
        self.name = name
        self.date = date
        self.type, self.message = self.__get_message_info(message)

    def __str__(self) -> str:
        return f"{self.name}"

    def __get_message_info(self, message):
        data = re.split("[\(:]", message)[0]
        return [ data[0], data[len(data) - 1] ]

def get_available_commits():
    with open("C:\\Users\\guilherme.turtera\\Desktop\\au\\.git\\hooks\Help\\available-commit-msg.txt", "r", encoding="utf-8") as file:
        content = file.read().split('|')
    return content

def get_commit_type(message):
    return re.split("[\(:]", message)[0]

def get_last_release_date(g):
    return g.log("-n 1", "--grep=release", "--oneline", "--pretty=%cs")

def get_last_commits_log(g):
    return g.log("--date=short", f"--since={get_last_release_date(g)}", "--oneline", "--pretty=%h|%s|%cn %ce|%cs")

# get it by a relative path
branch_path = os.path.abspath("..")

g = git.Git(branch_path)

commits_data = get_last_commits_log(g).split('\n')

#changelog_path = os.path.abspath("..\\changelog.md")
#with open(changelog_path, "r", encoding="utf-8") as file:
#    changelog_content = file.read()

available_types = get_available_commits()
dic = {}

buf = io.StringIO()
for log in commits_data:
    commit_list = log.split('|') # hash|message|name lastname|short style date 
    aux = Commit(commit_list[0], commit_list[1], commit_list[2], commit_list[3])
    dic[aux.type].append(Commit(commit_list))

print(buf.getvalue())

