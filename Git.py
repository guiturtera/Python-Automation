import re
import os
import git
from git.repo.base import Repo

branch_path = os.path.abspath("..")
print(branch_path)

# hash, message, name
g = git.Git(branch_path)
raw_log_content = g.log("-n 5", "--oneline", "--pretty=%H|%s|%cn %ce")
log_content = re.findall(".*\|.*\|.*", raw_log_content)


aux = tuple(re.split('\|', log_content[0]))
aux1 = (2, 3, 4)
for hash in aux1:
    print(hash)

print(log_content)

