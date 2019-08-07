# Copyright (C) 2019 Philip Woldhek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from twitter import Twitter
import urltools
from sys import argv


def get_list():
    print("Enter/Paste your links")
    contents = []
    while True:
        line = input()
        if line:
            contents.append(line)
        else:
            break
    if contents:
        return contents
    else:
        print("Enter/Paste urls")
        exit(1)


def get_content():
    if len(argv) < 2:
        content = get_list()
        return content
    else:
        file = argv[1]
        try:
            content = []
            list1 = list(open(file, "r"))
            links = list1[:] = [line.rstrip('\n') for line in list1]
            for item in links:
                if item:
                    url_info = urltools.extract(item)
                    if url_info[4] == str("twitter"):
                        item = url_info[7].replace("/", "")
                        content.append(item)
            return content
        except FileNotFoundError:
            print("File {0} not found!".format(argv[1]))
            exit(1)


if __name__ == "__main__":
    t = Twitter(output=True)
    content = get_content()
    t.main(content)
