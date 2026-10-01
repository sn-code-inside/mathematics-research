# load functions from packages
from numpy import matrix
from numpy.linalg import det, inv

# construct matrix
X = matrix([[2,1],
            [1,3]])

# compute inverse of X
X_inv = inv(X)

# compute determinant of X
X_det = det(X)

# print results
print('example 14 results (computing matrix inverse)\n')
print('X:\n',X,'\n')
print('X inverse:\n',X_inv,'\n')
print('X determinant\n',X_det,'\n')