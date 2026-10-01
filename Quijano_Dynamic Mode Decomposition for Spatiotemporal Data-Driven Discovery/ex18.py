# load functions from packages
from numpy import matrix, cumsum, where, linspace, around
from numpy.linalg import svd
from pandas import read_csv, DataFrame, melt
from matplotlib.pyplot import subplots
from matplotlib.patches import Circle
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from seaborn import lineplot, heatmap, color_palette

# load basic DMD algorithm script file
import dmd

# load dataset
## read data
sim_data = read_csv('data/ex2-data.csv') # read csv file
## convert longform data into x-t matrix form
sim_data = sim_data.pivot(index='x', columns='t', values='u')
x_vec = sim_data.index # discretized x
t_vec = sim_data.columns # discretized t
## extract data size information
n = x_vec.shape[0] # size of spatial dimension
m = t_vec.shape[0] # number of data snapshots
delta_t = t_vec[1] - t_vec[0] # compute delta t
## arrange dataset into X and X'
X = matrix(sim_data)[:,0:m-1]
X_prime = matrix(sim_data)[:,1:m]

# cumulative variance ratio for choosing r
## compute SVD of X
U, Sigma, VH = svd(X,full_matrices=False)
## compute cumulative variance ratio
Sigma_sqrd = [s**2 for s in Sigma]
var_ratio = Sigma_sqrd / sum(Sigma_sqrd)
cum_var_ratio = cumsum(var_ratio)
## choosing r for a defined cumulative variance ratio
rho_r = 1
r_star = len(where(cum_var_ratio < rho_r)[0])
rho_r_star = sum(var_ratio[0:r_star])

# apply basic DMD algorithm
## set rank
r = r_star
## compute dmd modes and eigenvalues
Phi, Omega, Lambda, V = dmd.basic(X, X_prime, r, delta_t)
## reconstruct data and predict future solution
x_0 = X[:,0] # initial state vector
n_t = 51 # number of time points
t_0 = 0 # start time
T = 1 # end time
X_DMD, b, t_p = dmd.basic_recon(Phi, Omega, x_0, n_t, t_0, T)
## convert reconstruction to dataframe
rec_data = DataFrame(X_DMD.real)
rec_data.index = x_vec
rec_data.columns = linspace(t_0,T,num=n_t)
## print results
print('example 18 (reconstructing example 2 data)\n')
print('rank of A:\n',r,'\n')
print('variance ratio:\n',rho_r_star,'\n')
print('disc A eigenvalues:\n',Lambda,'\n')
print('cont A eigenvalues:\n',Omega,'\n')
print('simulated data:\n',sim_data,'\n')
print('reconstructed data:\n',rec_data,'\n')

# plot singular values and variance ratio assessment
fig1, axs1 = subplots(nrows=3, ncols=3, figsize=(9,5))
## set-up values for plotting
vr_df = DataFrame({'vr': var_ratio, 'cvr': cum_var_ratio})
vr_df = vr_df.melt(ignore_index=False).reset_index()
vr_df.columns = ['i','type','value']
lambda_df = DataFrame({'real': Lambda.real,
                       'imag': Lambda.imag})
omega_df = DataFrame({'real': Omega.real,
                      'imag': Omega.imag})
v_df = DataFrame(V.real)
v_df['t'] = t_vec.values[:-1].reshape(-1)
phi_df = DataFrame(Phi.real)
phi_df['x'] = x_vec.values.reshape(-1)
## (a) plot singular values
lineplot(ax=axs1[0,0], data=vr_df, x='i', y='value', hue='type',
         linestyle='-', linewidth=2, legend=True)
x_ticks = linspace(0,len(Sigma),num=6)
x_ticklabels = linspace(1,len(Sigma),num=6).astype(int)
handles, labels = axs1[0,0].get_legend_handles_labels()
new_labels = ['singular values','cumulative']
axs1[0,0].legend(handles=handles, labels=new_labels, 
          title='', loc='right')
axs1[0,0].grid(True)
axs1[0,0].set_title('(a) Singular Values')
axs1[0,0].set_xlabel('$i$')
axs1[0,0].set_xticks(x_ticks)
axs1[0,0].set_xticklabels(x_ticklabels, rotation='horizontal')
axs1[0,0].set_ylabel('variance ratio')
## (b) plot eigenvalues of discrete-time A (real and imaginary)
lineplot(ax=axs1[0,1], data=lambda_df, x='real', y='imag',
         marker='.', markersize=18,
         linestyle='none', legend=False, errorbar=None)
unit_circle1 = Circle((0, 0), radius=1, fill=False,
                      edgecolor='gray', linestyle='--')
axs1[0,1].add_patch(unit_circle1)
axs1[0,1].set_aspect('equal', adjustable='box')
axs1[0,1].grid(True)
axs1[0,1].set_title('(b) Eigenvalues of $\mathbf{A}$')
axs1[0,1].set_xlim(-1.25, 1.25)
axs1[0,1].set_xlabel('$Re(\lambda_i)$')
axs1[0,1].set_ylim(-1.25, 1.25)
axs1[0,1].set_ylabel('$Im(\lambda_i)$')
## (c) plot eigenvalues of continuous-time A (real and imaginary)
lineplot(ax=axs1[0,2], data=omega_df, x='real', y='imag',
         marker='.', markersize=18,
         linestyle='none', legend=False, errorbar=None)
axs1[0,2].grid(True)
axs1[0,2].set_title('(c) Eigenvalues of $\mathit{A}$')
axs1[0,2].set_xlabel('$Re(\omega_i)$')
axs1[0,2].set_ylim(-1.25, 1.25)
axs1[0,2].set_ylabel('$Im(\omega_i)$')
## (d-f) plot dynamic modes
subfig_label1 = ['(d) Mode 1','(e) Mode 2','(f) Mode 3']
for i in range(0,3):
    lineplot(ax=axs1[1,i], data=phi_df, x='x', y=i,
             linestyle='-', linewidth=2,
             legend=False, errorbar=None)
    axs1[1,i].grid(True)
    axs1[1,i].set_title(subfig_label1[i])
    axs1[1,i].set_xlabel('$x$')
    axs1[1,i].set_ylabel('')
    axs1[1,i].set_ylim(-0.2,0.2)
## (h-i) plot time dynamics
subfig_label2 = ['(h) Mode Dynamics 1',
                 '(i) Mode Dynamics 2',
                 '(j) Mode Dynamics 3']
for i in range(0,3):
    lineplot(ax=axs1[2,i], data=v_df, x='t', y=i,
             linestyle='-', linewidth=2,
             legend=False, errorbar=None)
    axs1[2,i].grid(True)
    axs1[2,i].set_title(subfig_label2[i])
    axs1[2,i].set_xlabel('$t$')
    axs1[2,i].set_ylabel('')
## save plot to png file
fig1.tight_layout()
fig1.savefig('plot/ex18-modes.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex18-modes.png')

# plot data reconstruction
fig2, axs2 = subplots(nrows=1, ncols=2, figsize=(8,3))
## set-up reconstruction results for plotting
n_x= rec_data.shape[0] # number of x points
L = x_vec[-1]-x_vec[0] # length of rod
u_min = 0 # minimum u(x,t) value
u_max = 1 # maximum u(x,t) value
## (a) plot data in x and u(x,t) with color gradient as t
cmap1 = color_palette("icefire", as_cmap=True)
sm1 = ScalarMappable(cmap=cmap1, 
                     norm=Normalize(u_min,u_max))
heatmap(ax=axs2[0], data=sim_data, vmin=u_min, vmax=u_max,
        cmap=cmap1, cbar=False)
fig2.colorbar(sm1, ax=axs2[0],
              label='$u(x,t)$', location='right')
x_ticks = linspace(0.5, n_t-0.5, num=6)
x_ticklabels = around(linspace(0, T, num=6), 2)
y_ticks = linspace(0.5, n_x-0.5, num=6)
y_ticklabels = around(linspace(0, L, num=6), 2)
axs2[0].set_title('(a) Simulated Data')
axs2[0].set_xlabel('$t$')
axs2[0].set_xticks(x_ticks)
axs2[0].set_xticklabels(x_ticklabels, rotation='horizontal')
axs2[0].set_ylabel('$x$')
axs2[0].set_yticks(y_ticks)
axs2[0].set_yticklabels(y_ticklabels)
axs2[0].invert_yaxis()
## (b) plot data in t and x with color gradient as u(x,t)
cmap2 = color_palette("icefire", as_cmap=True)
sm2 = ScalarMappable(cmap=cmap2, 
                     norm=Normalize(u_min,u_max))
heatmap(ax=axs2[1], data=rec_data, vmin=u_min, vmax=u_max,
        cmap=cmap2, cbar=False)
fig2.colorbar(sm2, ax=axs2[1],
              label='$\widehat{u}(x,t)$', location='right')
x_ticks = linspace(0.5, n_t-0.5, num=6)
x_ticklabels = around(linspace(0, T, num=6), 2)
y_ticks = linspace(0.5, n_x-0.5, num=6)
y_ticklabels = around(linspace(0, L, num=6), 2)
axs2[1].set_title('(b) Reconstructed Data')
axs2[1].set_xlabel('$t$')
axs2[1].set_xticks(x_ticks)
axs2[1].set_xticklabels(x_ticklabels, rotation='horizontal')
axs2[1].set_ylabel('$x$')
axs2[1].set_yticks(y_ticks)
axs2[1].set_yticklabels(y_ticklabels)
axs2[1].invert_yaxis()
## save plot to png file
fig2.tight_layout()
fig2.savefig('plot/ex18-recon.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex18-recon.png')