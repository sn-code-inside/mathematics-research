# load functions from packages
from numpy import matrix, diag, log, around
from numpy.linalg import svd, eig, inv
from pandas import read_csv, DataFrame
from scipy.linalg import logm

# load dataset
## read data
sim_data = read_csv('data/ex1-data.csv') # read csv file
## extract data size information
m = sim_data.shape[0] # number of data snapshots

# DMD process to compute A
## arrange dataset into X and X'
X = matrix(sim_data[['x_1','x_2']][0:m-1]).T
X_prime = matrix(sim_data[['x_1','x_2']][1:m]).T
## compute SVD of X = U @ Sigma @ VH
U, Sigma, VH = svd(X, full_matrices=False)
## define matrix rank
r = U.shape[1]
## truncate SVD matrices
U_r = U[:,0:r]
Sigma_r = diag(Sigma)[0:r,0:r]
VH_r = VH[0:r,:]
## compute pseudoinverse of X using the SVD of X
X_psinv = VH_r.conj().T @ inv(Sigma_r) @ U.conj().T
## compute discrete-time A using the pseudoinverse of X
A_disc = X_prime @ X_psinv

# compute eigenvalues
## discrete-time A
evals_disc, evects_disc = eig(A_disc)
## continuous-time A using discrete-time A
delta_t = sim_data['t'][1] - sim_data['t'][0] # compute delta t
evals_cont = log(evals_disc) / delta_t

# compute continuous-time A using rounded discrete-time A
A_cont = logm(around(A_disc, 4)) / delta_t

# print results
print('example 1 results (horizontal spring-mass system)\n')
print('delta t:\n',delta_t,'\n')
print('X rank:\n',r,'\n')
print('disc A:\n',A_disc,'\n')
print('disc A eigenvalues:\n',evals_disc,'\n')
print('cont A:\n',A_cont,'\n')
print('cont A eigenvalues:\n',evals_cont,'\n')