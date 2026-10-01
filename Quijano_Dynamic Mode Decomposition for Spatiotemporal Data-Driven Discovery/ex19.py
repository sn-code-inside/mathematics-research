# load functions from packages
from numpy import array
from pandas import read_csv
from pydmd import DMD

# load dataset
## read data
sim_data = read_csv('data/ex1-data.csv') # read csv file
## convert data into an array
D = array(sim_data[['x_1','x_2']]).T

# apply DMD using pyDMD functions
## build DMD with 2 modes
dmd = DMD(svd_rank=2)
## fit DMD
dmd.fit(D)
## get eigenvalues of discrete-time A
evals_disc = dmd.eigs

# print results
print('example 19 (using the pyDMD package basically)\n')
print('disc A eigenvalues:\n',evals_disc,'\n')