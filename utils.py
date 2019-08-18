from blessings import Terminal


term = Terminal()


class Writer(object):
    def __init__(self, location):
        self.location = location

    def write(self, string):
        with term.location(*self.location):
            print(string)

    def flush(self):
        pass


def write_to_screen(x_pos, y_pos, string):
    location = (x_pos, y_pos)
    w = Writer(location)
    w.write(string)
