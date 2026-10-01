# load functions from packages
from numpy import matrix
from pandas import read_csv, DataFrame
from matplotlib.pyplot import subplots
from seaborn import lineplot

# load basic DMD algorithm script file
import dmd

# load dataset
## read data
sim_data = read_csv('data/ex1-data.csv') # read csv file
## extract data size information
m = sim_data.shape[0] # number of data snapshots
delta_t = sim_data['t'][1] - sim_data['t'][0] # compute delta t
## arrange dataset into X and X'
X = matrix(sim_data[['x_1','x_2']][0:m-1]).T
X_prime = matrix(sim_data[['x_1','x_2']][1:m]).T

# apply basic DMD algorithm
## set rank
r = 2
## compute dmd modes and eigenvalues
Phi, Omega, Lambda, V = dmd.basic(X, X_prime, r, delta_t)
## reconstruct data and predict future solution
x_0 = X[:,0] # initial state vector
n_t = 100 # number of time points
t_0 = 0 # start time
T = 8 # end time
X_DMD, b, t_p = dmd.basic_recon(Phi, Omega, x_0, n_t, t_0, T)
## convert reconstruction to dataframe
rec_data = DataFrame(X_DMD.real).T
rec_data.columns = ['x_1','x_2']
rec_data['t'] = t_p
## print results
print('example 17 (reconstructing example 1 data)\n')
print('rank of A:\n',r,'\n')
print('disc A eigenvalues:\n',Lambda,'\n')
print('cont A eigenvalues:\n',Omega,'\n')
print('DMD modes:\n',Phi,'\n')
print('DMD magnitudes:\n',b,'\n')
print('reconstruction:\n',rec_data,'\n')

# plot data and the reconstruction
fig, p1 = subplots(nrows=1, ncols=1, figsize=(7,2))
## set-up the results for plotting
df_data = sim_data.melt(id_vars=['t'], value_name='x')
df_recd = rec_data.melt(id_vars=['t'], value_name='x')
## data samples plot
lineplot(ax=p1,data=df_data, x='t', y='x', hue='variable', 
         linewidth=2, linestyle='--', marker='.', markersize=12,
         palette=['#104626','#68150d'])
## reconstruction plot
lineplot(ax=p1,data=df_recd, x='t', y='x', hue='variable',
         linewidth=2, linestyle='-', 
         palette=['#68c690','#ee8277'])
## assign plot legends and axis labels
handles, labels = p1.get_legend_handles_labels()
new_labels = ['$x^{(data)}_1$','$x^{(data)}_2$',
              '$\widehat{x}_1$','$\widehat{x}_2$']
p1.legend(handles=handles, labels=new_labels, 
          title='', loc='upper right')
p1.grid(True)
p1.set_xlabel('t')
p1.set_ylabel('$\mathbf{x}$')
## save plot to png file
fig.savefig('plot/ex17-recd.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex17-recd.png')