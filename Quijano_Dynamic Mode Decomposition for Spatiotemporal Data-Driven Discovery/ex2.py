# load functions from packages
from numpy import matrix, diag, log, repeat, linspace
from numpy.linalg import svd, eig, inv
from pandas import read_csv, DataFrame
from matplotlib.pyplot import subplots
from matplotlib.patches import Circle
from seaborn import lineplot, color_palette

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

# DMD process to compute A
## arrange dataset into X and X'
X = matrix(sim_data)[:,0:m-1]
X_prime = matrix(sim_data)[:,1:m]
## compute SVD of Y = U @ Sigma @ VH
U, Sigma, VH = svd(X, full_matrices=False)
## define matrix rank
r = 9
## truncate SVD matrices
U_r = U[:,0:r]
Sigma_r = diag(Sigma)[0:r,0:r]
VH_r = VH[0:r,:]
## compute pseudoinverse of X using the SVD of X
X_psinv = VH_r.conj().T @ inv(Sigma_r) @ U_r.conj().T
## compute discrete-time A using the pseudoinverse of X
A_disc = X_prime @ X_psinv

# compute eigenvalues and eigenvectors
## discrete-time A
evals_disc, evects_disc = eig(A_disc)
evals_magn_disc = abs(evals_disc) # magnitude
evals_disc_df = DataFrame({'real': evals_disc.real,
                           'imag': evals_disc.imag})
evects_disc_df = DataFrame(evects_disc.real)
## continuous-time A using discrete-time A
delta_t = t_vec[1]-t_vec[0] # compute delta t
evals_cont = log(evals_disc) / delta_t
evals_cont_df = DataFrame({'real': evals_cont.real,
                           'imag': evals_cont.imag})

# print results (rounded for display purposes)
print('example 2 results (heat diffusion)\n')
print('delta t:\n',delta_t,'\n')
print('disc A eigenvalues:\n',evals_disc_df,'\n')
print('disc A eigenvectors (real):\n',evects_disc_df,'\n')
print('cont A eigenvalues:\n',evals_cont_df,'\n')

# plot eigenvalues and eigenvectors
fig, axs = subplots(nrows=2, ncols=3, figsize=(8,4))
## set up data for plotting
top_n = 3 # choose top 3 eigenvalues for plotting
evals_disc_df['ith'] = range(1,n+1)
evals_disc_df['rank'] = repeat(top_n+1,n)
evals_disc_df.loc[range(0,top_n),"rank"] = range(1,top_n+1)
evects_disc_df['x'] = x_vec
evals_cont_df['rank'] = evals_disc_df['rank']
cmap = color_palette("Set1", as_cmap=True)
top_n_colors = [cmap(i) for i in range(top_n)]
top_n_colors.append(cmap(8))
## (a) plot eigenvalues of discrete-time A (real only)
axs[0,0].axhline(y=1, color='gray', linestyle='--')
axs[0,0].axhline(y=-1, color='gray', linestyle='--')
lineplot(ax=axs[0,0],
         data=evals_disc_df,
         x='ith', y='real', hue='rank',
         marker='.', markersize=8, markeredgecolor='none',
         palette=top_n_colors,
         linestyle='none', legend=False, errorbar=None)
lineplot(ax=axs[0,0],
         data=evals_disc_df[evals_disc_df['rank']!=top_n+1],
         x='ith', y='real', hue='rank',
         marker='.', markersize=18, markeredgecolor='none',
         palette=top_n_colors[0:top_n],
         linestyle='none', legend=False)
x_ticks = linspace(0,n,num=6)
x_ticklabels = linspace(1,n,num=6).astype(int)
axs[0,0].grid(True)
axs[0,0].set_title('(a) Eigenvalues of $\mathbf{A}$')
axs[0,0].set_xlabel('$i$')
axs[0,0].set_xticks(x_ticks)
axs[0,0].set_xticklabels(x_ticklabels, rotation='horizontal')
axs[0,0].set_ylim(-1.25, 1.25)
axs[0,0].set_ylabel('$Re(\lambda_i)$')
## (b) plot eigenvalues of discrete-time A (real and imaginary)
lineplot(ax=axs[0,1],
         data=evals_disc_df,
         x='real', y='imag', hue='rank',
         marker='.', markersize=8, markeredgecolor='none',
         palette=top_n_colors,
         linestyle='none', legend=False, errorbar=None)
lineplot(ax=axs[0,1],
         data=evals_disc_df[evals_disc_df['rank']!=top_n+1],
         x='real', y='imag', hue='rank',
         marker='.', markersize=18, markeredgecolor='none',
         palette=top_n_colors[0:top_n],
         linestyle='none', legend=False)
unit_circle1 = Circle((0, 0), radius=1, fill=False,
                      edgecolor='gray', linestyle='--')
axs[0,1].add_patch(unit_circle1)
axs[0,1].set_aspect('equal', adjustable='box')
axs[0,1].grid(True)
axs[0,1].set_title('(b) Eigenvalues of $\mathbf{A}$')
axs[0,1].set_xlim(-1.25, 1.25)
axs[0,1].set_xlabel('$Re(\lambda_i)$')
axs[0,1].set_ylim(-1.25, 1.25)
axs[0,1].set_ylabel('$Im(\lambda_i)$')
## (c) plot eigenvalues of continuous-time A (real and imaginary)
lineplot(ax=axs[0,2],
         data=evals_cont_df,
         x='real', y='imag', hue='rank',
         marker='.', markersize=8, markeredgecolor='none',
         palette=top_n_colors,
         linestyle='none', legend=False, errorbar=None)
lineplot(ax=axs[0,2],
         data=evals_cont_df[evals_disc_df['rank']!=top_n+1],
         x='real', y='imag', hue='rank',
         marker='.', markersize=18, markeredgecolor='none',
         palette=top_n_colors[0:top_n],
         linestyle='none', legend=False)
axs[0,2].grid(True)
axs[0,2].set_title('(c) Eigenvalues of $\mathit{A}$')
axs[0,2].set_xlim(-10, 1.25)
axs[0,2].set_xlabel('$Re(\omega_i)$')
axs[0,2].set_ylim(-1.25, 1.25)
axs[0,2].set_ylabel('$Im(\omega_i)$')
## (d-f) plot eigenvectors of discrete-time A
subfig_label = ['(d) Eigenvector 1',
                '(e) Eigenvector 2',
                '(f) Eigenvector 3']
for i in range(0,top_n):
    lineplot(ax=axs[1,i], data=evects_disc_df, x='x', y=i,
             linewidth=2, color=top_n_colors[i])
    axs[1,i].grid(True)
    axs[1,i].set_title(subfig_label[i])
    axs[1,i].set_xlabel('x')
    axs[1,i].set_ylabel('')
    axs[1,i].set_ylim(-0.2,0.2)
## save plot to png file
fig.tight_layout()
fig.savefig('plot/ex2-dmd-evals.png', dpi=600)
print('plot saved to plot/ex2-dmd-evals.png')