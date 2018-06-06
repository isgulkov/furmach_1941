from sys import argv, exit
from os import path

from solution import display_results


if __name__ == '__main__':
    if len(argv) != 2:
        # print "Usage: python problem2018-4 [x], x - varik number"
        exit()

    display_results(
        path.join(
            path.dirname(__file__),
            'data/youtube_{:d}.csv'.format(int(argv[1]))
        )
    )
