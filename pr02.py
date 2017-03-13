from scipy.stats import rv_continuous, chi2, ttest_1samp
import numpy as np

from matplotlib import pyplot as plt, gridspec, mlab

from os import system

class SuperDistVarik7:
    def __init__(self, n):
        self._chi2 = chi2(n)

    def rvs(self, size=None):
        return self._chi2.rvs(size=size) / 2.0

    @classmethod
    def from_mean(cls, mean):
        return cls(int(mean * 2))

def mean_within_confidence_interval(sample, expected_mean, alpha=0.05):
    # Returns true if the given `expected_mean` is within confidence interval for the mean of the distribution
    # represented by `sample`, false otherwise

    t_stat, p_value = ttest_1samp(sample, expected_mean)

    # As the p-value is the minimum alpha such that `expected_mean` is in the confidence interval, to accept the the
    # hypothesis, the alpha in question must be less than the p-value
    return alpha < p_value

def pr02a():
    xi = SuperDistVarik7.from_mean(3.0)

    total_expetiments = 10000
    times_rejected = 0

    print "\tconducting %d t-tests..." % (total_expetiments, )

    for i in xrange(total_expetiments):
        sample = xi.rvs(size=8)

        if not mean_within_confidence_interval(sample, 3):
            times_rejected += 1

    print "Null hypothesis was rejected %d times out of %d, so the P false positive is %f" % (times_rejected,
        total_expetiments, 1.0 * times_rejected / total_expetiments)

def pr02b(expected_mean=3.0):
    plt.title("Probability of rejection")
    plt.xlabel("True mean")

    for sample_size in [8, 50]:
        mean_prob_xs = []
        mean_prob_ys = []

        for true_mean in np.arange(1.0, 2.0 * expected_mean - 1.0 + 0.01, 0.5):
            psi = SuperDistVarik7.from_mean(true_mean)

            total_expetiments = 1000
            times_rejected = 0

            print "\tconducting %d t-tests, sample size %d, true mean %.1f..." % (total_expetiments, sample_size,
                true_mean, )

            for i in xrange(total_expetiments):
                sample = psi.rvs(size=sample_size)

                if not mean_within_confidence_interval(sample, expected_mean):
                    times_rejected += 1

            mean_prob_xs.append(true_mean)
            mean_prob_ys.append(1.0 * times_rejected / total_expetiments)

        plt.plot(mean_prob_xs, mean_prob_ys, label="Sample size %d" % (sample_size, ))

    plt.legend()
    plt.savefig("~figure.png")

    system("open ./~figure.png")

if __name__ == '__main__':
    pr02a()
    pr02b()

