# load functions from packages
from numpy import linspace
from pandas import DataFrame
from scipy.integrate import solve_ivp
from matplotlib.pyplot import subplots
from seaborn import lineplot

# parameters
beta = 0.3 # transmission rate
gamma = 0.1 # recovery rate
RN = beta/gamma # basic reproductive number

# initial conditions
S0 = 0.99
I0 = 0.01
R0 = 0
x0 = [S0, I0, R0]  # initial conditions (% of population)

# time discretizations
n_t = 500 # number of time points
t_0 = 0 # start time
T = 100 # end time
t_vec = linspace(t_0, T, n_t)

# define the SIR system of differential equations
def sir_model(t, x):
    S, I, R = x
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

# generate simulated data
## solve ODE using numerical method
sim_data = solve_ivp(sir_model, (t_0,T), x0, t_eval=t_vec)
## convert results into a dataframe
sim_data_df = DataFrame({'t': sim_data.t,
                         'S': sim_data.y[0],
                         'I': sim_data.y[1],
                         'R': sim_data.y[2]})
## print data samples
print('research project 5 simulated data (SIR model)\n')
print('parameters:\n',
      'beta = ',beta,'\n','gamma = ',gamma,'\n')
print('R_0:\n',RN,'\n')
print('SIR results: \n',sim_data_df,'\n')
## save data samples to csv file
sim_data_df.to_csv('data/rp5-data.csv', sep=',', index=False)
print('data saved to data/rp5-data.csv')

# plot simulated data
## set-up the data for plotting
sim_df = sim_data_df.melt(id_vars=['t'], value_name='x')
## set-up the figure
fig, p1 = subplots(nrows=1, ncols=1, figsize=(7,2))
## solution plot
lineplot(ax=p1,data=sim_df, x='t', y='x', hue='variable',
         linewidth=2, palette=['#000000','#ff0000','#ffe100'])
## assign plot legends and axis labels
handles, labels = p1.get_legend_handles_labels()
new_labels = ['Susceptible (S)','Infected (I)','Recovered (R)']
p1.legend(handles=handles, labels=new_labels, 
          title='', loc='right')
p1.grid(True)
p1.set_xlabel('t')
p1.set_ylabel('% of population')
## save plot to png file
fig.tight_layout()
fig.savefig('plot/rp5-data.png', bbox_inches='tight', dpi=600)
print('plot saved to plot/rp5-data.png')