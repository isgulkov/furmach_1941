from sys import argv

from solution import pr02a, pr02b
from variants import get_dist_by_variant_number

if __name__ == '__main__':
    if len(argv) != 2:
        print "Usage: python problem_2 [x], x - varik number"
    else:
        Dist = get_dist_by_variant_number(int(argv[1]))

	    pr02a(Dist)
	    pr02b(Dist)
