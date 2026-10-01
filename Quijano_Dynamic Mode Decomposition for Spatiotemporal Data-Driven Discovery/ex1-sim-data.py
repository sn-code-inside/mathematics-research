# load functions from packages
from numpy import zeros, matrix, linspace, diag
from numpy.linalg import inv, eig
from pandas import DataFrame
from scipy.linalg import expm
from matplotlib.pyplot import subplots
from seaborn import lineplot

# parameters
mu_m = 1 # mass
mu_k = 2 # spring constant
mu_c = 1 # friction coefficient

# initial conditions
x0_1 = 1 # position
x0_2 = 0 # velocity
x0 = [x0_1,x0_2] # initial state

# time discretizations
## time length
T_exac = 8 # exact solution
T_data = 4 # data sample
## for the exact solution
pts_exac = 100
t_exac = linspace(0, T_exac, num=pts_exac)
## for the data sample
pts_data = 9
t_data = linspace(0, T_data, num=pts_data)

# exact solution function
#  of the horizontal spring-mass system of odes,
#   velocity:     x'_1 = x_2,
#   acceleration: x'_2 = -(mu_k/mu_m)*x_1-(mu_c/mu_m)*x_2,
#  with initial conditions x_1 = x0_1 and x_2 = x0_2.
def hsm_sys_sol(t, x_0):
    ## create coefficient matrix A
    A = matrix([[0,1],[-(mu_k/mu_m),-(mu_c/mu_m)]])
    ## compute eigenvalues and eigenvectors of A
    e_vals, e_vects = eig(A)
    ## solve specific solution
    b = inv(e_vects) @ matrix(x_0).T
    x_sol = e_vects @ expm(diag(e_vals * t)) @ b
    return x_sol.squeeze().real

# generate exact solution values
## empty array to store x_1 and x_2 exact solution
x_exac = zeros([2,t_exac.shape[0]])
## loop through t of the exact solution
for i, t in enumerate(t_exac):
    x_exac[:, i] = hsm_sys_sol(t,x0)
## convert exact solution to dataframe
x_exac = DataFrame(x_exac).T
x_exac.columns = ['x_1','x_2']
x_exac['t'] = t_exac

# generate data samples using the exact solution
## empty array to store x_1 and x_2 data samples
x_data = zeros([2,t_data.shape[0]])
## loop through t of the exact solution
for i, t in enumerate(t_data):
    x_data[:, i] = hsm_sys_sol(t,x0)
## convert data sample to dataframe
x_data = DataFrame(x_data).T
x_data.columns = ['x_1','x_2']
x_data['t'] = t_data
## print data samples
print('example 1 simulated data',
      '(horizontal spring-mass system)\n')
print('parameters:\n',
      'mu_m = ',mu_m,'\n','mu_k = ',mu_k,'\n','mu_c = ',mu_c,'\n')
print('x_1(t) and x_2(t) results: \n',x_data,'\n')
## save data samples to csv file
x_data.to_csv('data/ex1-data.csv', sep=',', index=False)
print('data saved to data/ex1-data.csv')

# plot exact solution and data samples
## set-up the data for plotting
df_exac = x_exac.melt(id_vars=['t'], value_name='x')
df_data = x_data.melt(id_vars=['t'], value_name='x')
## set-up the figure
fig, p1 = subplots(nrows=1, ncols=1, figsize=(7,2))
## exact solution plot
lineplot(ax=p1,data=df_exac, x='t', y='x', hue='variable',
         linewidth=2, palette=['#27ae60','#e74c3c'])
## data samples plot
lineplot(ax=p1,data=df_data, x='t', y='x', hue='variable', 
         linewidth=2, linestyle='--', marker='.', markersize=12,
         palette=['#104626','#68150d'])
## assign plot legends and axis labels
handles, labels = p1.get_legend_handles_labels()
new_labels = ['$x_1$','$x_2$','$x^{(data)}_1$','$x^{(data)}_2$']
p1.legend(handles=handles, labels=new_labels, 
          title='', loc='upper right')
p1.grid(True)
p1.set_xlabel('t')
p1.set_ylabel('$\mathbf{x}$')
## save plot to png file
fig.savefig('plot/ex1-data.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex1-data.png')