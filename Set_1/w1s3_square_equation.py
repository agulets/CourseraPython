import sys


def print_equation_result(a, b, c):
    print(int((-b + (b * b - 4 * a * c) ** (0.5))/(2 * a)))
    print(int((-b - (b * b - 4 * a * c) ** (0.5))/(2 * a)))


if __name__ == '__main__':
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])
    print_equation_result(a, b, c)
