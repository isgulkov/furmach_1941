from sys import argv, exit

from solution import display_sample_analyses
from variants import get_prng_by_variant_number

if __name__ == '__main__':
    if len(argv) != 2:
        print "Usage: python problem2018-2 [x], x - varik number"
        exit()
    
    prng = get_prng_by_variant_number(int(argv[1]))

    display_sample_analyses(prng)
