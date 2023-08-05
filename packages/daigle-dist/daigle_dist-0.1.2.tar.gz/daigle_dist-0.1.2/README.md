# Distribution Analyzer
This package allows a user to perform some simple analysis of basic elements of Gaussian and Binomial Distributions.

This package is primarily meant as a test case/POC for loading packages to PyPi, but may also be useful for some other people.

To use this package:
1. `pip install <PACKAGE_NAME>`
2. run Python
3. enter `from distributions import Gaussian, Binomial`<br>
3a. `Gaussian(mean, stdev)`<br>
3b. `Binomial(mean,stdev)`
4. Attributes include:
> * `read_data_file()`: assigns the distribution object some data from a .txt file
> * `mean`: returns the distribution object's mean
> * `stdev`: returns the distribution object's standard deviation
> * `calculate_mean()`: assigns and returns a distribution object's mean
> * `calculate_stdev()`: assigns and returns a distribution object's standard deviation
> * `replace_stats_with_data()`: update attributes of p and n of binomial distribution object
> * `plot_bar`: bar chart plot of the outcomes and frequencies of a distribution object
> * `pdf()`: calculates the probability density function for a distribution object
> * `plot_bar_pdf`: bar chart plot of the probability density function of a distribution object
5. Magic Methods include:
> * `__add__`: allows two distribution objects to be added to each other as well as calculate the mean and standard deviation of each other
> * `__repr__`: outputs the characteristics of a distribution object
