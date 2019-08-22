# MIT License
#
# Copyright (c) 2019 Philip
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import argv

import urltools
from twitter import Twitter


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
    usernames = get_content()
    location = "./"
    t = Twitter(usernames=usernames, location=location)
    t.main(content)
