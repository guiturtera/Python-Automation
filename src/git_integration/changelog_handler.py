import io
import os

class ChangelogHandler():
    def __init__(self, changelog_path, commits_dic, version_info) -> None:
        #self.changelog_path = changelog_path
        #self.commits_dic = commits_dic
        new_version = version_info.new_version

        self.changelog_content = self.__load_changelog(changelog_path)
        self.text_to_append = self.__changelog_text_to_append(commits_dic, new_version)

    def __load_changelog(self, changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def __changelog_text_to_append(self, commits_dic, new_version):
        buffer = io.StringIO()
        buffer.write('\n')
        buffer.write('## [')
        buffer.write(new_version)
        buffer.write('] \n')
        for commit_type in commits_dic.keys():
            buffer.write('### ')
            buffer.write(commit_type)
            buffer.write('\n')
            for commit in commits_dic[commit_type]:
                buffer.write(commit.__str__())
                buffer.write('\n')
                print(buffer.getvalue())
        buffer.write('\n')
        return buffer.getvalue()