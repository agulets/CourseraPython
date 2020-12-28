# need rename to solution.py

class FileReader():

    def __init__(self, file_path):
        self._file_path = file_path

    def read(self):
        text = ""
        try:
            with open(self._file_path) as f:
                text = f.read()
        except IOError:
            return str()
        return text


if __name__ == '__main__':
    pass
