import os
import sys
import tempfile
import json
import argparse


STORAGE = os.path.join(tempfile.gettempdir(), 'storage.data')


def get_all_data(storage_file=STORAGE):
    if not os.path.exists(STORAGE) or os.path.getsize(STORAGE) == 0:
        return dict()
    with open(storage_file, 'r') as data_file:
        data = data_file.read()
        j_data = json.loads(data) 
        return j_data


def write_all_data(j_data, storage_file=STORAGE):
    with open(storage_file, 'w') as data_file:
        data = json.dumps(j_data)
        data_file.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action="store", dest="key", type=str)
    parser.add_argument('--val', action="store", dest="value", default='', type=str)

    args = parser.parse_args()
    key, value = args.key, args.value

    data_in_file = get_all_data()

    if value:
        existing_value = data_in_file.get(key)
        if existing_value:
            value = f"{existing_value}, {value}"
        data_in_file.update([(key, value)])
        write_all_data(data_in_file)
    else:
        print(data_in_file.get(key))
