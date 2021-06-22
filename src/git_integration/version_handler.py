from os import write
import re

class VersionHandler():
    def __init__(self, versioninfo_path, dic_commits):
        self.versioninfo_path = versioninfo_path

        self.old_version = self.__get_current_version(versioninfo_path)
        self.new_version = self.__get_next_version(self.old_version, dic_commits)

    def apply(self):
        with open(self.versioninfo_path, 'w', encoding='utf-8') as f:
            f.write(self.new_version)

    def __get_current_version(self, version_info_path):
        with open(version_info_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().lower()

        if re.match('^v([0-9]*\.){2}[0-9]*$', content):
            return content
        else:
            raise Exception('Version info path invalid! Format must be vx.y.z')

    def __get_next_version(self, old_version, dic_commits):
        x, y, z = self.__get_xyz(old_version)

        if dic_commits.__contains__('api'):
            return self.__format_xyz(int(x) + 1, 0, 0)
        elif dic_commits.__contains__('feat'):
            return self.__format_xyz(x, int(y) + 1, 0)
        elif dic_commits.__contains__('fix'):
            return self.__format_xyz(x, y, int(z) + 1)

        return self.__format_xyz(x, y, z)

    def __get_xyz(self, string_version):
        string_version = string_version[1:]
        return string_version.split('.')

    def __format_xyz(self, x, y, z):
        return f"v{x}.{y}.{z}"
