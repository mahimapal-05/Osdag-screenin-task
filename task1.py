# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 22:02:38 2026

@author: swaro
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


ds = xr.open_dataset(r"C:\Users\swaro\Downloads\screening_task.nc")


central_elements = [15, 24, 33, 42, 51, 60, 69, 78, 83]


Mz_i = ds.forces.sel(Element=central_elements, Component="Mz_i").values
Mz_j = ds.forces.sel(Element=central_elements, Component="Mz_j").values

Vy_i = ds.forces.sel(Element=central_elements, Component="Vy_i").values
Vy_j = ds.forces.sel(Element=central_elements, Component="Vy_j").values


Mz_nodes = np.concatenate(([Mz_i[0]], Mz_j))
Vy_nodes = np.concatenate(([Vy_i[0]], Vy_j))

x = np.arange(len(Mz_nodes)) 

plt.figure(figsize=(8, 4))
plt.plot(x, Mz_nodes, marker="o")
plt.title("Bending Moment Diagram (Central Girder)")
plt.xlabel("Position along girder")
plt.ylabel("Mz (Bending Moment)")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(x, Vy_nodes, marker="o")
plt.title("Shear Force Diagram (Central Girder)")
plt.xlabel("Position along girder")
plt.ylabel("Vy (Shear Force)")
plt.grid(True)
plt.tight_layout()
plt.show()
