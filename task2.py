# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 22:05:31 2026

@author: swaro
"""


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize

ds = xr.open_dataset("screening_task (1).nc")

girders = {
    1: [13, 22, 31, 40, 49, 58, 67, 76, 81],
    2: [14, 23, 32, 41, 50, 59, 68, 77, 82],
    3: [15, 24, 33, 42, 51, 60, 69, 78, 83],
    4: [16, 25, 34, 43, 52, 61, 70, 79, 84],
    5: [17, 26, 35, 44, 53, 62, 71, 80, 85],
}

girder_z = {1: -4, 2: -2, 3: 0, 4: 2, 5: 4}

Mz_all, Vy_all = {}, {}

for g, elems in girders.items():
    Mz_i = ds.forces.sel(Element=elems, Component="Mz_i").values
    Mz_j = ds.forces.sel(Element=elems, Component="Mz_j").values
    Vy_i = ds.forces.sel(Element=elems, Component="Vy_i").values
    Vy_j = ds.forces.sel(Element=elems, Component="Vy_j").values

    Mz_all[g] = np.concatenate(([Mz_i[0]], Mz_j))
    Vy_all[g] = np.concatenate(([Vy_i[0]], Vy_j))

x = np.arange(10)

def plot_colored_line(ax, x, y, z, cmap, lw=4):
    norm = Normalize(vmin=y.min(), vmax=y.max())
    for i in range(len(x) - 1):
        ax.plot(
            x[i:i+2],
            y[i:i+2],
            [z, z],
            color=cmap(norm(np.mean(y[i:i+2]))),
            linewidth=lw
        )

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

cmap = cm.plasma

for g in girders:
    z = girder_z[g]

    ax.plot(x, np.zeros_like(x), z, color="gray", linewidth=2, alpha=0.4)

    plot_colored_line(ax, x, Mz_all[g], z, cmap)

ax.set_title("3D Bending Moment Diagram (MIDAS Style)", fontsize=14)
ax.set_xlabel("Bridge Length")
ax.set_ylabel("Bending Moment (Mz)")
ax.set_zlabel("Girder Position")

ax.view_init(elev=22, azim=-60)
ax.grid(False)

mappable = cm.ScalarMappable(norm=Normalize(
    vmin=min(v.min() for v in Mz_all.values()),
    vmax=max(v.max() for v in Mz_all.values())
), cmap=cmap)
fig.colorbar(mappable, ax=ax, shrink=0.6, label="Bending Moment (Mz)")

plt.tight_layout()
plt.show()

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

cmap = cm.viridis

for g in girders:
    z = girder_z[g]

    ax.plot(x, np.zeros_like(x), z, color="gray", linewidth=2, alpha=0.4)

    plot_colored_line(ax, x, Vy_all[g], z, cmap)

ax.set_title("3D Shear Force Diagram (MIDAS Style)", fontsize=14)
ax.set_xlabel("Bridge Length")
ax.set_ylabel("Shear Force (Vy)")
ax.set_zlabel("Girder Position")

ax.view_init(elev=22, azim=-60)
ax.grid(False)

mappable = cm.ScalarMappable(norm=Normalize(
    vmin=min(v.min() for v in Vy_all.values()),
    vmax=max(v.max() for v in Vy_all.values())
), cmap=cmap)
fig.colorbar(mappable, ax=ax, shrink=0.6, label="Shear Force (Vy)")

plt.tight_layout()
plt.show()
