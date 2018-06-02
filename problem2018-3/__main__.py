from sys import argv, exit

from solution import display_results
from variants import get_dist_by_variant_number


if __name__ == '__main__':
    if len(argv) != 2:
        print "Usage: python problem2018-3 [x], x - varik number"
        exit()

    Dist = get_dist_by_variant_number(int(argv[1]))

    display_results(Dist)
