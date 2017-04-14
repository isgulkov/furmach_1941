from sys import argv

from solution import pr03
from variants import get_data_by_variant_number

if __name__ == '__main__':
    if len(argv) != 2:
        print "Usage: python problem_3 [x], x - varik number"
        exit()

    data = get_data_by_variant_number(int(argv[1]))

    pr03(data)
