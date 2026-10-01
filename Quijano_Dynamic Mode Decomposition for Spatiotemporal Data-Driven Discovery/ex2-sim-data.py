## load functions from packages
from numpy import zeros, linspace, exp, pi, sin, around
from pandas import DataFrame, melt
from scipy.integrate import quad
from matplotlib.pyplot import subplots
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from seaborn import lineplot, heatmap, color_palette

# parameters
L = 1 # rod length
alpha = 0.1 # thermal diffusivity

# discretizations
## for x
n_x = 100 # number of x points
x_vec = linspace(0, L, num=n_x)
## for t
T = 1 # end time
n_t = 51 # number of t points
t_vec = linspace(0, T, num=n_t)
## for the infinite sum
N = 100 # number of sums to add

# fixed boundary conditions (Dirichlet)
u_x0 = 1 # left-end temperature
u_xL = 1 # right-end temperature

# fixed initial temperature for g(x)
u_t0 = 0

# exact solution of the heat equation u_tt = alpha u_xx
#  with initial temperature distribution u(x,1) = g(x),
#  and boundary conditions u(0,t) = beta_1 and u(L,t) = beta_2
## initial temperature distribution
def g(x):
    return u_t0 # fixed
## equilibrium solution
def heat_eq_e(x):
    return (((u_xL - u_x0) / L) * x) + u_x0
## integrand for solving the coefficients B_m
def B_m_integrand(x, m):
    return (g(x) - heat_eq_e(x)) * sin((m * pi * x) / L)
## heat equation exact solution
def heat_eq_soln(x, t):
    ### solve non-trivial solution
    v_sol = 0
    #### loop through n values of the infinite sum
    for n in range(1, N+1):
        ##### integrate B_m integrand
        I, error = quad(B_m_integrand, 0, L, args=(n,))
        ##### compute B_m coefficient
        B_m = (2 / L) * I
        ##### solve specific solution
        v_sol += (B_m * 
                  exp(-(((n * pi) / L) ** 2) * alpha * t) * 
                  sin(((n * pi * x) / L)))
    ### create full solution
    u_sol = v_sol + heat_eq_e(x)
    return u_sol

# generate data samples using the exact solution
## empty array to store u(x,t) data samples
u_data = zeros([x_vec.shape[0],t_vec.shape[0]])
## loop through x and t of the exact solution
for t_i, t in enumerate(t_vec):
    for x_i, x in enumerate(x_vec):
        u_data[x_i,t_i] = heat_eq_soln(x, t)
## convert data samples to dataframe
u = u_data # for the heatmap
u_data = DataFrame(u_data)
u_data['x'] = x_vec
u_data = u_data.set_index('x')
u_data.columns = t_vec
u_data = u_data.melt(ignore_index=False).reset_index()
u_data.columns = ['x','t','u']
u_min = min(u_data['u']) # minimum u(x,t) value
u_max = max(u_data['u']) # maximum u(x,t) value
## print data samples
print('example 2 simulated data (heat diffusion)\n')
print('Parameters:\n','L = ',L,'\n','alpha = ',alpha,'\n')
print('u(x,t) results:\n',u_data,'\n')
## save data samples to csv file
u_data.to_csv('data/ex2-data.csv', sep=',', index=False)
print('data saved to data/ex2-data.csv')

# plot exact solution and data samples
fig, axs = subplots(nrows=1, ncols=2, figsize=(8,3))
## (a) plot data in x and u(x,t) with color gradient as t
cmap1 = color_palette("viridis", as_cmap=True)
sm1 = ScalarMappable(cmap=cmap1, norm=Normalize(0,T))
lineplot(ax=axs[0], data=u_data, x='x', y='u', hue='t',
         palette=cmap1, legend=False)
fig.colorbar(sm1, ax=axs[0], label='$t$', location='right')
axs[0].grid(True)
axs[0].set_title('(a) $u(x,t)$ in $x$-$u$ Perspective')
axs[0].set_xlabel('$x$')
axs[0].set_ylabel('$u(x,t)$')
## (b) plot data in t and x with color gradient as u(x,t)
cmap2 = color_palette("icefire", as_cmap=True)
sm2 = ScalarMappable(cmap=cmap2,norm=Normalize(u_min,u_max))
heatmap(ax=axs[1], data=u, cmap=cmap2, cbar=False)
fig.colorbar(sm2, ax=axs[1], label='$u(x,t)$', location='right')
x_ticks = linspace(0.5, n_t-0.5, num=6)
x_ticklabels = around(linspace(0, T, num=6), 2)
y_ticks = linspace(0.5, n_x-0.5, num=6)
y_ticklabels = around(linspace(0, L, num=6), 2)
axs[1].set_title('(b) $u(x,t)$ in $t$-$x$ Perspective')
axs[1].set_xlabel('$t$')
axs[1].set_xticks(x_ticks)
axs[1].set_xticklabels(x_ticklabels, rotation='horizontal')
axs[1].set_ylabel('$x$')
axs[1].set_yticks(y_ticks)
axs[1].set_yticklabels(y_ticklabels)
axs[1].invert_yaxis()
## save plot to png file
fig.tight_layout()
fig.savefig('plot/ex2-data.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex2-data.png')