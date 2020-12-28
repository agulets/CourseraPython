import sys

def get_digits_sum(_str):
    sum = 0
    for i in range(len(_str)):
        sum = sum + int(_str[i:i+1])
    return sum


if __name__ == '__main__':
    _str = sys.argv[1]
    print(get_digits_sum(_str)) 
