# load functions from packages
from numpy import matrix

# construct matrices
A = matrix([[0,2],
            [-3,-1]])
B = matrix([[1,-3],
            [0,1]])

# matrix addition
ApB = A+B

# matrix subtraction
BmA = B-A

# print results
print('example 4 results (matrix operations)\n')
print('A+B:\n',ApB,'\n')
print('B-A:\n',BmA,'\n')