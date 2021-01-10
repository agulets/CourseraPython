import os.path
import tempfile
import uuid


class File:
    def __init__(self, path_to_file):
        self.path = path_to_file
        if not os.path.isfile(self.path):
            with open(self.path, "a+"):
                pass

    def read(self):
        with open(self.path, "r") as file:
            return file.read()

    def write(self, data):
        with open(self.path, "w") as file:
            file.write(data)
        return len(data)

    def __add__(self, another_file):
        result_file_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid1()}")
        result_file_data = self.read() + another_file.read()
        result_file = File(result_file_path)
        result_file.write(result_file_data)
        return result_file

    def __str__(self):
        return self.path

    def __iter__(self):
        self.iter_file = open(self.path)
        return self

    def __next__(self):
        return self.iter_file.__next__()


if __name__ == "__main__":
    path_to_file = "test"
    print(os.path.exists(path_to_file))
    file_obj = File(path_to_file)
    print(os.path.exists(path_to_file))
    file_obj.read()
    file_obj.write('some text')
    file_obj.read()
    file_obj.write('other text')
    file_obj_1 = File(path_to_file + '_1')
    file_obj_2 = File(path_to_file + '_2')
    file_obj_1.write('line 1\n')
    file_obj_2.write('line 2\n')
    new_file_obj = file_obj_1 + file_obj_2
    print(isinstance(new_file_obj, File))
    print(new_file_obj)
    for line in new_file_obj:
        print(ascii(line))

