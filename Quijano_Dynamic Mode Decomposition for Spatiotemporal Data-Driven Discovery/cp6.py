# load functions from packages
from numpy import exp, sin, pi, linspace, meshgrid
from numpy.random import randn

# generate simulated data
## function to generate spatiotemporal data
def f(x,t):
	return exp(-2*t)*sin(3*x)
## create x-t grid
x_vec = linspace(-3,3,num=100)
t_vec = linspace(0,1,num=50)
x_grid, t_grid = meshgrid(x_vec, t_vec)
## apply function to generate the data
F = f(x_grid,t_grid)
## add scaled random noise to the data
FW = F.T + 0.1 * randn(100,50)