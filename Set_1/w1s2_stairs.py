import sys

def print_stairs(height):
    s = ''
    for h in range(1, height + 1):
        for l in range(height - h + 1):
            s = ' ' * l  + ( '#' * h )
        print(s)


if __name__ == '__main__':
    height = int(sys.argv[1])
    print_stairs(height)
