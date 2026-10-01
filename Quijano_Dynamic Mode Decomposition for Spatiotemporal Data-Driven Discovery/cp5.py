# load functions from packages
from numpy.random import seed, randn

# generate correlated dataset using random numbers
X = randn(100, 10) @ randn(10, 50)