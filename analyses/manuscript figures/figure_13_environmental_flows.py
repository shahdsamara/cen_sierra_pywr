#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date

# In[18]:


sns.set_style('whitegrid')
sns.set_palette('Set1')

# basin = 'upper_san_joaquin'
# node = 'IFR bl Millerton Lake'
basin = 'stanislaus'
# node = 'IFR bl Sand Bar Div'
# node = 'IFR bl McKays Point Div'
# node = 'IFR bl Collierville PH discharge'
# node = 'IFR bl Goodwin Reservoir'
node = 'IFR bl Beardsley Afterbay'

file_suffix = date.today().strftime('%Y-%m-%d')
suffix = ' - {}'.format(file_suffix) if file_suffix else ''
output_dir = os.environ['SIERRA_RESULTS_PATH']

climate_scenario = 'historical/Livneh'

fig, ax = plt.subplots(1, 1, figsize=(12, 4))

start = '1992-10-01'
end = '1994-09-03'

data_path = os.environ['SIERRA_DATA_PATH']
obs_path = Path(data_path, 'Stanislaus River/gauges/streamflow_cfs.csv')
df_obs = pd.read_csv(obs_path, index_col=0, parse_dates=True)
df_obs = df_obs['USGS 11292900 MF STANISLAUS R BL BEARDSLEY DAM CA'][start:end] / 35.315


def get_df(scenario, var, label=None):
    csv_path = Path(output_dir, scenario + suffix, basin, climate_scenario)
    path = Path(csv_path, f'InstreamFlowRequirement_{var}_mcm.csv')
    _df = pd.read_csv(path, index_col=0, parse_dates=True, header=0)[node][start:end].to_frame()
    _df = _df * 1e6 / 24 / 60 / 60
    _df.index.name = 'Date'
    _df['Variable'] = label or var
    return _df


scen = 'planning'
df_flow = get_df(scen, 'Flow')
df_min = get_df(scen, 'Min Flow')
df_range = get_df(scen, 'Max Flow')
df_max = df_min + df_range
df_max['Variable'] = 'Max Flow'

df_flow_no_rr = get_df('planning - no rr', 'Flow', label='No RR')

ax.plot(df_min.index, df_min[node].values, color='red', linewidth=4, alpha=0.75, linestyle='--',
        label='Min. flow req\'t w/ ramping limit')
ax.plot(df_obs.index, df_obs.values, color='black', linewidth=3.5, alpha=0.75, label='Observed flow')
ax.plot(df_flow.index, df_flow_no_rr[node].values, color='orange', label='Sim. flow w/o ramping limit')
# ax.fill_between(df_min.index, df_min[node].values, df_max[node].values, alpha=0.2, label='Maximum flow (range)')
ax.plot(df_flow.index, df_flow[node].values, color='green', label='Sim. flow w/ ramping limit')
ax.set_yscale('log')
# ax.set_ylim(bottom=0, top=3)
ax.set_ylabel(r'Flow (m$^3$/s) [log scale]', fontsize=11)
ax.legend(loc='upper right', fontsize=11)

fig.savefig('figure - flow below Beardsley Afterbay.png', dpi=600, bbox_inches='tight')

plt.show()

# In[ ]:
