import csv
from pathlib import Path

CAR = "car"
TRUCK = "truck"
SPEC_MACHINE = "spec_machine"
PHOTO_FILE_EXT = [".jpg", ".jpeg", ".png", ".gif"]


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)
        self.car_type = car_type

    def get_photo_file_ext(self):
        return Path(self.photo_file_name).suffix


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(car_type=CAR, brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(car_type=TRUCK, brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.body_width = 0.0
        self.body_height = 0.0
        self.body_length = 0.0
        if body_whl:
            try:
                length, width, height = body_whl.split('x')
                self.body_width = float(width)
                self.body_height = float(height)
                self.body_length = float(length)
            except ValueError:
                pass

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(car_type=SPEC_MACHINE, brand=brand, photo_file_name=photo_file_name, carrying=carrying)
        self.extra = extra


def check_photo_file_name(photo_file_name):
    if photo_file_name[-4::] in PHOTO_FILE_EXT:
        return len(photo_file_name) > 4

    if photo_file_name[-5::] in PHOTO_FILE_EXT:
        return len(photo_file_name) > 5

    return False


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def get_car_by_row(row):
    car = None

    if len(row) != 7 \
            or row[0] not in [CAR, TRUCK, SPEC_MACHINE] \
            or not row[1] \
            or not row[3] \
            or not check_photo_file_name(row[3]) \
            or not row[5]:
        return None

    car_type = row[0]
    passenger_seats_count = row[2]
    brand = row[1]
    photo_file_name = row[3]
    body_whl = row[4]
    extra = row[6]

    try:
        carrying = float(row[5])
    except ValueError:
        return car

    if car_type == CAR:
        try:
            passenger_seats_count = int(passenger_seats_count)
        except ValueError:
            return car
        car = Car(brand=brand,
                  photo_file_name=photo_file_name,
                  carrying=carrying,
                  passenger_seats_count=passenger_seats_count)
    elif car_type == TRUCK:
        car = Truck(brand=brand,
                    photo_file_name=photo_file_name,
                    carrying=carrying,
                    body_whl=body_whl)
    elif car_type == SPEC_MACHINE:
        if extra and not is_digit(extra):
            car = SpecMachine(brand=brand,
                              photo_file_name=photo_file_name,
                              carrying=carrying,
                              extra=extra)

    return car


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)
        for row in reader:
            car = get_car_by_row(row)
            if car is not None:
                car_list.append(car)

    return car_list


if __name__ == "__main__":
    print(get_car_list("/Users/abelov/PROJECTS/CourseraPython/Set_1/w3s2_cars.csv"))


