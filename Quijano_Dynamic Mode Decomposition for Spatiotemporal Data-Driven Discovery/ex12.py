# load functions from packages
from numpy import matrix
from numpy.linalg import svd

# construct matrix
X = matrix([[0,1],
            [1,0],
            [1,1]])

# compute the svd of X
U, Sigma, VT = svd(X, full_matrices=False)

# print results
print('example 12 results (computing svd)\n')
print('X:\n',X,'\n')
print('U:\n',U,'\n')
print('Sigma:\n',Sigma,'\n')
print('VT:\n',VT,'\n')