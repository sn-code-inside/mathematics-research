# load functions from packages
from numpy import linspace, around, array, meshgrid
from numpy import pi, exp, cos, sin, min, max
from numpy.random import randn
from pandas import DataFrame
from matplotlib.pyplot import subplots
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from seaborn import heatmap, color_palette
from pydmd import DMD
from pydmd.plotter import plot_summary
from pydmd.preprocessing import hankel_preprocessing

# create simulated data
## define parameters
alpha_1 = -0.2
alpha_2 = -0.1
beta_1 = 2
beta_2 = 1
## define functions
def f1(x,t):
    return exp(alpha_1*t)*cos(beta_1*x)
def f2(x,t):
    return exp(alpha_2*x)*sin(beta_2*t)
## define x-t grid resolutions
### x
n = 400 # number of x points
x_start = -4 # start
x_end = 4 # end
x_vec = linspace(x_start,x_end,num=n)
### t
m = 200 # number of t points
t_start = 0 # start
t_end = 4*pi # end
t_vec = linspace(t_start,t_end,num=m)
## extract time step
delta_t = t_vec[1]-t_vec[0]
## create x-t grid
x_grid, t_grid = meshgrid(x_vec,t_vec)
## generate data using the functions
F1 = f1(x_grid,t_grid)
F2 = f2(x_grid,t_grid)
F = F1 + F2
## add noise to the simulated data
scale = 0.10
FW = F.T + scale * randn(n,m)
## convert data into an array
FW = array(FW).T

# apply DMD using pyDMD functions
## build DMD with 3 modes
dmd = DMD(svd_rank=3)
## data preprocessing
d = 2 # number of delays
delay_dmd = hankel_preprocessing(dmd, d=d)
## fit DMD
delay_dmd.fit(FW.T)
## extract data reconstruction
FW_recon = delay_dmd.reconstructed_data.real

# plot DMD summary
plot_summary(dmd, x=x_vec, t=delta_t, d=d, figsize=(10,6),
             filename='plot/ex20-dmd-summary.png', dpi=300)
print('plot saved to plot/ex20-dmd-summary.png')

# plot reconstructed data
fig1, axs1 = subplots(nrows=1, ncols=2, figsize=(7,3))
# set-up data for plotting
FW = DataFrame(FW).T
FW_recon = DataFrame(FW_recon)
f_min = min(FW)
f_max = max(FW)
## (a) plot FW data
cmap1 = color_palette("viridis", as_cmap=True)
sm1 = ScalarMappable(cmap=cmap1, norm=Normalize(f_min, f_max))
heatmap(ax=axs1[0], data=FW, vmin=f_min, vmax=f_max,
        cmap=cmap1, cbar=False)
fig1.colorbar(sm1, ax=axs1[0],
              label='$f(x,t)$', location='right')
x_ticks = linspace(0.5, m-0.5, num=3)
x_ticklabels = around(linspace(t_start, t_end, num=3), 2)
y_ticks = linspace(0.5, n-0.5, num=3)
y_ticklabels = around(linspace(x_start, x_end, num=3), 2)
axs1[0].set_title('(a) Simulated Data')
axs1[0].set_xlabel('$t$')
axs1[0].set_xticks(x_ticks)
axs1[0].set_xticklabels(x_ticklabels, rotation='horizontal')
axs1[0].set_ylabel('$x$')
axs1[0].set_yticks(y_ticks)
axs1[0].set_yticklabels(y_ticklabels)
axs1[0].invert_yaxis()
## (b) plot FW reconstructed data
cmap2 = color_palette("viridis", as_cmap=True)
sm2 = ScalarMappable(cmap=cmap2, norm=Normalize(f_min, f_max))
heatmap(ax=axs1[1], data=FW_recon, vmin=f_min, vmax=f_max,
        cmap=cmap2, cbar=False)
fig1.colorbar(sm2, ax=axs1[1],
              label='$\widehat{f}(x,t)$', location='right')
x_ticks = linspace(0.5, m-0.5, num=3)
x_ticklabels = around(linspace(t_start, t_end, num=3), 2)
y_ticks = linspace(0.5, n-0.5, num=3)
y_ticklabels = around(linspace(x_start, x_end, num=3), 2)
axs1[1].set_title('(b) Reconstructed Data')
axs1[1].set_xlabel('$t$')
axs1[1].set_xticks(x_ticks)
axs1[1].set_xticklabels(x_ticklabels, rotation='horizontal')
axs1[1].set_ylabel('$x$')
axs1[1].set_yticks(y_ticks)
axs1[1].set_yticklabels(y_ticklabels)
axs1[1].invert_yaxis()
## save plot to png file
fig1.tight_layout()
fig1.savefig('plot/ex20-recon.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex20-recon.png')

# plot generated data
fig2, axs2 = subplots(nrows=1, ncols=3, figsize=(10,3))
# set-up data for plotting
F1 = DataFrame(F1).T
F2 = DataFrame(F2).T
## (a) plot F1 data
cmap1 = color_palette("viridis", as_cmap=True)
sm1 = ScalarMappable(cmap=cmap1, norm=Normalize(f_min, f_max))
heatmap(ax=axs2[0], data=F1, vmin=f_min, vmax=f_max,
        cmap=cmap1, cbar=False)
fig2.colorbar(sm1, ax=axs2[0],
              label='$f_1(x,t)$', location='right')
x_ticks = linspace(0.5, m-0.5, num=3)
x_ticklabels = around(linspace(t_start, t_end, num=3), 2)
y_ticks = linspace(0.5, n-0.5, num=3)
y_ticklabels = around(linspace(x_start, x_end, num=3), 2)
axs2[0].set_title('(a) $f_1$')
axs2[0].set_xlabel('$t$')
axs2[0].set_xticks(x_ticks)
axs2[0].set_xticklabels(x_ticklabels, rotation='horizontal')
axs2[0].set_ylabel('$x$')
axs2[0].set_yticks(y_ticks)
axs2[0].set_yticklabels(y_ticklabels)
axs2[0].invert_yaxis()
## (b) plot F2 data
cmap2 = color_palette("viridis", as_cmap=True)
sm2 = ScalarMappable(cmap=cmap2, norm=Normalize(f_min, f_max))
heatmap(ax=axs2[1], data=F2, vmin=f_min, vmax=f_max,
        cmap=cmap2, cbar=False)
fig2.colorbar(sm2, ax=axs2[1],
              label='$f_2(x,t)$', location='right')
x_ticks = linspace(0.5, m-0.5, num=3)
x_ticklabels = around(linspace(t_start, t_end, num=3), 2)
y_ticks = linspace(0.5, n-0.5, num=3)
y_ticklabels = around(linspace(x_start, x_end, num=3), 2)
axs2[1].set_title('(b) $f_2$')
axs2[1].set_xlabel('$t$')
axs2[1].set_xticks(x_ticks)
axs2[1].set_xticklabels(x_ticklabels, rotation='horizontal')
axs2[1].set_ylabel('$x$')
axs2[1].set_yticks(y_ticks)
axs2[1].set_yticklabels(y_ticklabels)
axs2[1].invert_yaxis()
## (c) plot FW data
cmap3 = color_palette("viridis", as_cmap=True)
sm3 = ScalarMappable(cmap=cmap3, norm=Normalize(f_min, f_max))
heatmap(ax=axs2[2], data=FW, vmin=f_min, vmax=f_max,
        cmap=cmap1, cbar=False)
fig2.colorbar(sm3, ax=axs2[2],
              label='$f(x,t)$', location='right')
x_ticks = linspace(0.5, m-0.5, num=3)
x_ticklabels = around(linspace(t_start, t_end, num=3), 2)
y_ticks = linspace(0.5, n-0.5, num=3)
y_ticklabels = around(linspace(x_start, x_end, num=3), 2)
axs2[2].set_title('(c) $f$')
axs2[2].set_xlabel('$t$')
axs2[2].set_xticks(x_ticks)
axs2[2].set_xticklabels(x_ticklabels, rotation='horizontal')
axs2[2].set_ylabel('$x$')
axs2[2].set_yticks(y_ticks)
axs2[2].set_yticklabels(y_ticklabels)
axs2[2].invert_yaxis()
## save plot to png file
fig2.tight_layout()
fig2.savefig('plot/ex20-data.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/ex20-data.png')