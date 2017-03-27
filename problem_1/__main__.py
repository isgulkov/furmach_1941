from sys import argv

from solution import pr01
from variants import get_dist_by_variant_number

if __name__ == '__main__':
    if len(argv) != 2:
        print "Usage: python problem_1 [x], x - varik number"
    else:
        Dist = get_dist_by_variant_number(int(argv[1]))

        pr01(Dist)
