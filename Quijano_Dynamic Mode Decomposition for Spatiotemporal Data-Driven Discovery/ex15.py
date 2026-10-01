# load functions from packages
from numpy import matrix, diag
from numpy.linalg import det, svd, inv, pinv

# construct matrix
X = matrix([[2,4],
            [1,2]])

# compute SVD of X
U, Sigma, VH = svd(X, full_matrices=False)

# compute pseudoinverse of X using SVD
## define matrix rank
r = 1
## truncate SVD matrices
U_r = U[:,0:r]
Sigma_r = diag(Sigma)[0:r,0:r]
VH_r = VH[0:r,:]
## construct pseudoinverse
X_psinv = VH_r.conj().T @ inv(Sigma_r) @ U_r.conj().T

# compute determinant of X
X_det = det(X)

# check using property (X^+)^+ = X to reconstruct X
X_recon = pinv(X_psinv)

# print results
print('example 15 results',
      '(computing matrix pseudoinverse using SVD)\n')
print('X:\n',X,'\n')
print('X rank:\n',r,'\n')
print('X pseudoinverse:\n',X_psinv,'\n')
print('X determinant:\n',X_det,'\n')
print('X reconstruction:\n',X_recon,'\n')