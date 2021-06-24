import io
import os

from click.decorators import version_option
from git_integration.version_handler import VersionHandler

class ChangelogHandler():
    def __init__(self, changelog_path, commits_dic, version_info: VersionHandler) -> None:
        self.changelog_path = changelog_path
        self.commits_dic = commits_dic
        self.version_info = version_info
        version_info.set_dic_commit(commits_dic)
        new_version = version_info.get_next_version_for_changelog()

        self.__changelog_content = self.__load_changelog(changelog_path)
        self.new_text_to_append = self.__changelog_text_to_append(commits_dic, new_version)

    def apply(self):
        with open(self.changelog_path, 'w', encoding='utf-8') as f:
            f.write(f"{self.new_text_to_append}\n{self.__changelog_content}")

    def __load_changelog(self, changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def __changelog_text_to_append(self, commits_dic, new_version):
        buffer = io.StringIO()
        buffer.write('## [')
        buffer.write(new_version)
        buffer.write('] \n')
        for commit_type in commits_dic.keys():
            if not commit_type == 'improvement':
                buffer.write('### ')
                buffer.write(commit_type)
                buffer.write('\n')
                for commit in commits_dic[commit_type]:
                    buffer.write('  - ')
                    buffer.write(commit.__str__())
                    buffer.write('\n')
        return buffer.getvalue()