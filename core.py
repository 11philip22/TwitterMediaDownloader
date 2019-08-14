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
