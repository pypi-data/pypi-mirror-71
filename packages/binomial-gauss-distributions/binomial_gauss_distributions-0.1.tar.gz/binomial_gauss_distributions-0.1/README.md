# **Project Description**
# **Gaussian and Binomial Distributions**

A basic package for calculating and visualizing Gaussian and Binomial Distributions. This is only a test.

# How to import the classes using the interpret

~~~python
$ python
>>> from gauss_binom_test import Gaussian, Binomial
~~~

# Features

* Calculate the Gaussian and Binomial pdf of a data set
* Calculate the mean and standard deviation
* Calculate the sum of two pdfs
* Plot the histogram of data points and normalizdd histogram of the pdf

# Example

Open the Python interpreter:

**Create a standard normal distribution (zero mean and standard deviation equal to one)**

~~~python
>>> gaussian_normal = Gaussian()
>>> gaussian_normal
mean 0, standard deviation 1
~~~

**Create a Gaussian distribution with mean=5 and stdv=2**

~~~python
>>> gaussian_one = Gaussian(5,2)
mean 5, standard deviation 2
~~~

**Addition of two Gaussian distributions**

~~~python
>>> gaussian_sum = gaussian_normal + gaussian_one
>>> gaussian_sum.mean()
5
>>> sample stdev
>>> gaussian_sum.stdev()
2.2360679
~~~

**Addition of three Gaussian distributions**

~~~python
>>> gaussian_sum = Gaussian(1,2) + Gaussian(2,3) + Gaussian(3,4)
>>> gaussian_sum
>>> mean 6, standard deviation 5.3851648
~~~

**Calculate the value of the Gaussian distribution function at a given point**

~~~python
>>> gaussian_one = Gaussian(5,2)
>>> gaussian_one.pdf(6)
0.17603266338
~~~

**Generate a Binomial distribution of 20 trials and 0.5 probability of an event occurring**

~~~python
>>> binom_one = Binomial(.5, 20)
>>> binom_one
mean 10.0, standard deviation 2.23606797749979, p 0.5, n 20
~~~

**Calculate the probability of occurring 5 successes for a Binomial distribution of 20 trials and p=0.5**

~~~python
>>> Binomial(.5, 20).pdf(5)
0.0147857666015625
~~~

**Adding two binomial distributions**

~~~python
>>> binom_sum = Binomial(.5, 20) + Binomial(.5, 10)
mean 15.0, standard deviation 2.7386127875258306, p 0.5, n 30
~~~