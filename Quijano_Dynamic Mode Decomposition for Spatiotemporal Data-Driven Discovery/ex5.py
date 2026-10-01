# load functions from packages
from numpy import matrix, multiply, dot

# construct matrices
A = matrix([[0,2],
            [-3,-1]])
B = matrix([[1,-3],
            [0,1]])

# element-wise matrix multiplication
AB_elementwise = multiply(A,B)

# standard matrix multiplication
AB_standard1 = A @ B
AB_standard2 = dot(A,B)

# print results
print('example 5 results (matrix multiplication)\n')
print('AB (element-wise using multiply):\n',AB_elementwise,'\n')
print('AB (standard using @):\n',AB_standard1,'\n')
print('AB (standard using dot):\n',AB_standard2,'\n')