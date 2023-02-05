import os
import traceback


class File:
    def __init__(self, filename, default):
        self.filename = filename
        self.default = default
        self.__create_if_not_exists()
        read = self.__read()
        try:
            self.data = eval(read)
        except Exception:
            traceback.print_exc()
            self.recreate()

    def __create_if_not_exists(self):
        if not os.path.exists(self.filename):
            self.create()

    def __read(self):
        with open(self.filename, encoding='utf8') as f:
            return f.read()

    def recreate(self):
        with open("old_" + self.filename, 'w', encoding='utf8') as f:
            f.write(self.__read())
        self.create()

    def create(self):
        with open(self.filename, 'w', encoding='utf8') as f:
            f.write(self.default)

    def write(self, data):
        with open(self.filename, 'w', encoding='utf8') as f:
            f.write(str(data))