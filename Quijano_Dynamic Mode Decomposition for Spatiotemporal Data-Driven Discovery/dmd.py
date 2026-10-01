############ DMD Basic Algorithm and Reconstruction #############

# load packages
from numpy import diag, log, zeros, linspace
from numpy.linalg import eig, svd, inv, pinv
from scipy.linalg import expm

# basic DMD algorithm
def basic(X, X_prime, r, delta_t):
    # INPUTS:
    # X = data matrix
    # X_prime = time-shifted data matrix
    # r = rank of X
    # delta_t = time step
    #
    # OUTPUTS:
    # Phi = the DMD modes
    # Omega = eigenvalues of continuous-time operator A
    # Lambda = eigenvalues of A_tilde
    # V = time dynamics
    
    ## data matrix sizes
    n = X.shape[0] # number of rows in X
    m = X.shape[1]+1 # number of time snapshots
    mm1 = X.shape[1] # number of columns in X
    
    ## Basic DMD algorithm
    ### reduced SVD of X
    U, Sigma, VH = svd(X,full_matrices=False)
    ### set rank
    r = min(r,U.shape[1])
    ### SVD truncation by rank r
    U_r = U[:,0:r]
    Sigma_r = diag(Sigma)[0:r,0:r]
    VH_r = VH[0:r,:]   
    ### compute A-tilde
    A_tilde = \
        U_r.conj().T @ X_prime @ VH_r.conj().T @ inv(Sigma_r)
    ### compute eigendecomposition of A-tilde
    Lambda, W = eig(A_tilde)    
    ### compute the DMD modes
    Phi = X_prime @ VH_r.conj().T @ inv(Sigma_r) @ W
    ### compute the continuous-time eigenvalues
    Omega = log(Lambda+0*1j)/delta_t
    ### compute time dynamics
    V = VH_r.T
    
    # return results
    return Phi, Omega, Lambda, V

# data reconstruction
def basic_recon(Phi, Omega, x_0, n_t, t_0, T):
    # INPUTS:
    # Phi = DMD modes
    # Omega = eigenvalues of continuous-time operator A
    # x_0 = initial state vector
    # n_t = number of time points
    # t_0 = starting time
    # T = ending time
    #
    # OUTPUTS:
    # t_p = time points
    # b = DMD mode magnitudes
    # X_DMD = reconstructed X

    ## DMD reconstruction and prediction
    ### compute the DMD mode magnitudes
    b = pinv(Phi) @ x_0
    ### set time points
    t_p = linspace(t_0,T,num=n_t)
    ### reconstruction
    #### empty 2D array to store values
    X_DMD = zeros((len(x_0),len(t_p)), dtype=float)+0*1j
    ### prediction loop
    for i, t in enumerate(t_p):
        X_DMD[:,[i]] = Phi @ expm(diag(Omega)*t) @ b

    # return results
    return X_DMD, b, t_p

#################################################################