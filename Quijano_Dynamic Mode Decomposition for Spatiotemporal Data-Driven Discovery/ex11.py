# load functions from packages
from numpy import matrix
from numpy.linalg import eig

# construct matrix
A = matrix([[0,1],
            [-2,-1]])

# compute eigenvalues and eigenvectors of A
evals, evects = eig(A)

# print results
print('example 11 results',
      '(computing eigenvalues and eigenvectors)\n')
print('A:\n',A,'\n')
print('eigenvalues:\n',evals,'\n')
print('eigenvectors:\n',evects,'\n')