from scipy.stats import rv_continuous, chi2, ttest_1samp
import numpy as np

from matplotlib import pyplot as plt, gridspec, mlab

class SuperDistVarik7:
    def __init__(self, n):
        self._chi2 = chi2(n)

    def rvs(self, size=None):
        return self._chi2.rvs(size=size) / 2.0

def mean_within_confidence_interval(sample, mean, alpha=0.05):
    # Check whether the given `mean` is within confidence interval for the mean of the distribution represented by `sample`

    t_stat, p_value = ttest_1samp(sample, 3)

    return p_value < alpha

def pr02a():
    xi = SuperDistVarik7(6)

    total_expetiments = 10000
    times_rejected = 0

    print "\tconducting %d t-tests..." % (total_expetiments, )

    for i in xrange(total_expetiments):
        sample = xi.rvs(size=8)

        if mean_within_confidence_interval(sample, 3):
            times_rejected += 1


    print "Null hypothesis was rejected %d times out of %d, so the P false positive is %f" % (times_rejected, total_expetiments, 1.0 * times_rejected / total_expetiments)

def pr02b():
    plt.title("Probability of rejection")

    for sample_size in [8, 50]:
        mean_prob_xs = []
        mean_prob_ys = []

        for mean in np.arange(1.0, 5.01, 0.5):
            theta = int(mean * 2)

            psi = SuperDistVarik7(theta)

            total_expetiments = 1000
            times_rejected = 0

            print "\tconducting %d t-tests, sample size %d, true mean %.1f..." % (total_expetiments, sample_size, mean, )

            for i in xrange(total_expetiments):
                sample = psi.rvs(size=sample_size)

                if mean_within_confidence_interval(sample, 3):
                    times_rejected += 1

            mean_prob_xs.append(mean)
            mean_prob_ys.append(1.0 * times_rejected / total_expetiments)

        plt.plot(mean_prob_xs, mean_prob_ys, label="Sample size %d" % (sample_size, ))

    plt.show()

if __name__ == '__main__':
    pr02a()
    pr02b()

