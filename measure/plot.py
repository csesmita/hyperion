import json
import numpy as np
import matplotlib.pyplot as plt
from palettable.colorbrewer.qualitative import Set2_7
import matplotlib.ticker as ticker
import matplotlib.font_manager as font_manager
#from mknapsack import solve_multiple_knapsack
import os

dirs = ['data/2024-04-19T20-32-46', 'data/2024-04-19T20-46-33', 'data/2024-04-19T21-09-42', 'data/2024-04-19T21-27-00', 'data/2024-04-19T21-46-23', 'data/2024-04-19T22-07-52', 'data/2024-04-19T22-31-27', 'data/2024-04-19T22-57-08', 'data/2024-04-19T23-24-56', 'data/2024-04-19T23-54-49']

pods = range(100, (len(dirs) + 1) * 100, 100)

metrics = {}
runs = range(1)

for i, dir in enumerate(dirs):
  with open(f'{dir}/consensus-{pods[i]}pods-1jobs-1top.json', 'r') as f:
    for line in f:
      metrics[pods[i]] = json.loads(line)
x = pods
y_time = []
y_setup = []

for p in pods:
  t1 = []
  for r in runs:
    r = str(r)
    t2 = np.array([metrics[p][r][name]['total time'] for name in metrics[p][r]])
    t1.append(np.mean(t2))
  # print(t1, np.std(t1))
  y_time.append([np.median(t1), np.percentile(t1, 25), np.percentile(t1, 75)])

  t2 = np.array([metrics[p]['0'][name]['setup time'] for name in metrics[p][r]])
  y_setup.append(np.mean(t2))


y_time = np.array(y_time)


pl_times = []
# jobs_size = []
for i, dir in enumerate(dirs):
  with open(f'{dir}/placement-{pods[i]}pods-1jobs-1top.json', 'r') as f:
    for l in f:
      pl = json.loads(l)
      ts = []
      js = []
      for j in runs:
        for k in pl[str(j)]:
          if k.startswith('my-controller'):
            ts.append(pl[str(j)][k]['time taken'])
      ts = np.array(ts)
      js = np.array(js)
      pl_times.append([np.median(ts), np.percentile(ts, 25), np.percentile(ts, 75)])

pl_times = np.array(pl_times) / 1e6
y_time = np.array(y_time) / 1e6


# Generate graphs
fig, ax1 = plt.subplots()
fig.set_size_inches(8, 5.5)

cs = Set2_7.mpl_colors
l1, =ax1.plot(x, y_time[:, 0], label='consensus', color=cs[0], marker='o', linewidth=2)
ax1.fill_between(x, y_time[:, 1], y_time[:, 2], alpha=0.25, color=cs[0])
ax1.set_ylabel('Consensus time (s)', color=cs[0])
ax1.tick_params(axis='y', labelcolor=cs[0])

ax2 = ax1.twinx()
l2,=ax2.plot(pods, pl_times[:,0], marker='x', linewidth=2, color=cs[1], label='placement')
ax2.fill_between(pods, pl_times[:,1], pl_times[:,2], alpha=0.25, linewidth=0, color=cs[1])
ax2.set_ylabel('Placement time (s)', color=cs[1])
ax2.tick_params(axis='y', labelcolor=cs[1])

#ax1.legend([l1, l2], ['Consensus', 'Placement'], loc='upper left', prop=font_manager.FontProperties(family='Times New Roman'))
ax1.legend([l1, l2], ['Consensus', 'Placement'], loc='upper left')

ax1.set_xlabel('Number of Schedulers')

ax1.set_xticks(pods)
fig.savefig(f'e2e-con-placement-latency.pdf')
