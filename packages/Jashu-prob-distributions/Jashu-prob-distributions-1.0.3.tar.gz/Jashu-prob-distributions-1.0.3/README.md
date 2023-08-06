Project description

# Jashu-prob-distributions package


This package provides the Gaussian distribution and Binomial distribution classes.

* Gaussian - Gaussian distribution class for calculating and visualizing a Gaussian distribution.
Attributes:
mean (float) - representing the mean value of the distribution.
stdev (float) - representing the standard deviation of the distribution.
data_list (list of floats) - a list of floats extracted from the data file.

Methods:
calculate_mean() - Function to calculate the mean of the data set.

calculate_stdev() - Function to calculate the standard deviation of the data set.

plot_histogram() - Function to output a histogram of the instance variable data using matplotlib pyplot library.

read_data_file(filename) - Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute.

pdf(x) - Probability density function calculator for the gaussian distribution
Args:
x (float): point for calculating the probability density function
Returns:
float: probability density function output

plot_histogram_pdf(n_spaces = 50) - Function to plot the normalized histogram of the data and a plot of the probability density function along the same range
Args:
n_spaces (int): number of data points
Returns:
list: x values for the pdf plot
list: y values for the pdf plot

__add__(other) - Function to add together two Gaussian distributions
Args:
other (Gaussian): Gaussian instance
Returns:
Gaussian: Gaussian distribution

__repr__() - Function to output the characteristics of the Gaussian instance



* Binomial - Binomial distribution class for calculating and visualizing a Binomial distribution.
Attributes:
mean (float) representing the mean value of the distribution
stdev (float) representing the standard deviation of the distribution
data_list (list of floats) a list of floats to be extracted from the data file
p (float) representing the probability of an event occurring
n (int) number of trials

Methods:
calculate_mean() - Function to calculate the mean from p and n

calculate_stdev() - Function to calculate the standard deviation from p and n.

read_data_file(filename) - Function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute.

replace_stats_with_data() - Function to calculate p and n from the data set
Args:
None
Returns:
float: the p value
float: the n value

plot_bar() - Function to output a histogram of the instance variable data using matplotlib pyplot library.

pdf(k) - Probability density function calculator for the gaussian distribution.
Args:
x (float): point for calculating the probability density function
Returns:
float: probability density function output

plot_bar_pdf() - Function to plot the pdf of the binomial distribution
Args:
None
Returns:
list: x values for the pdf plot
list: y values for the pdf plot

__add__(other) - Function to add together two Binomial distributions with equal p
Args:
other (Binomial): Binomial instance
Returns:
Binomial: Binomial distribution

__repr__() - Function to output the characteristics of the Binomial instance.



# Files

* Generaldistribution.py - contains Distribution class, its attributes and methods being inherited by Gaussian and Binomial class.
* Gaussiandistribution.py - contains Gaussian class, its attributes and methods stated above in  Jashwanth-prob-distributions package summary.
* Binomialdistribution.py - contains Binomial class, its attributes and methods stated above in  Jashwanth-prob-distributions packagesummary.


# Installation
* The code should run with no issues using Python versions 3.*.
* No extra besides the built-in libraries from Anaconda needed to run this project
Math
matplotlib

Use the package manager pip to install pk_prob_distributions.
pip install Jashu-prob-distributions

open python IDE,
Try Usage,

from jashu_prob_distributions import Gaussian, Binomial

Gaussian(10, 7) #returns a Gaussian Distribution with mean  and standard deviation 

Binomial(.4,25) #returns a Binomial distribution with mean ,standard deviation,p,n


Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

