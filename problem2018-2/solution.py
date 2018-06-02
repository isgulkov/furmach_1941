
from os import system
from itertools import product
from functools import partial

from sample_analysis import SampleAnalysis


def take_unique(it, max_unique, max_total=None):
    if max_total is None:
        max_total = max_unique * 100

    seen = set()

    for i, x in enumerate(it):
        if i >= max_total:
            break

        if x not in seen:
            seen.add(x)

            yield x

            if len(seen) == max_unique:
                return


def display_sample_analyses(prng, sizes=(100, 10000), find_examples=True):
    analyses = [
        SampleAnalysis(
            prng.get_sample(n, first=True),
            "First ${:d}$ states".format(n)
        ) for n in sizes
    ]

    if analyses[0].is_positive():
        unique = list(take_unique(prng.forever(first=True), 100))

        while SampleAnalysis.will_result_positive(unique) and len(unique) > 2:
            unique.pop()

        analyses.insert(0,
            SampleAnalysis(
                unique,
                "First ${:d}$ unique states".format(len(unique))
            )
        )

    if not analyses[-1].is_positive():
        n_repeat = 2
        xs = []

        for n_repeat, size in product(xrange(2, 10), (10000, 100)):
            xs = prng.get_sample(size, first=True)

            if SampleAnalysis.will_result_positive(xs * n_repeat):
                break

        analyses.append(
            SampleAnalysis(
                xs * n_repeat,
                "First ${:d}$ states ${:d}$ times over".format(len(xs), n_repeat)
            )
        )

    fig = SampleAnalysis.draw_all(
        analyses,
        suptitle="Fitness of $R(0; 1)$ to samples from %s" % prng.description
    )

    fig.savefig("~figure.png", dpi=300)
    system("open ./~figure.png")
