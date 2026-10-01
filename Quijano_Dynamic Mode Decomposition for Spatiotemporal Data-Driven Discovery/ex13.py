# load functions from packages
from numpy import matrix

# construct matrix
X = matrix([[2+1j,0-2j,1+3j],
            [1-2j,2+0j,0-3j]])

# compute conjugate transpose of X
XCT = X.conj().T

# compute transpose of X
XT = X.T

# print results
print('example 13 results',
      '(computing matrix conjugate transpose)\n')
print('X:\n',X,'\n')
print('X conjugate transpose:\n',XCT,'\n')
print('X transpose:\n',XT,'\n')