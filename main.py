import cantera as ct
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd

# initial conditions
print('Set up initial conditions:')
T0 = float(input("temperature [K]: T_0= "))
p0 = float(input("pressure [Pa]: p_0= "))

# defining gas mixture
gas = ct.Solution('gri30.yaml')
#gas.TPX = T0, p0, 'H2:2, 02:1, N2:3.76'
gas.set_equivalence_ratio(1.0, "CH4", {"O2": 1.0, "N2": 3.76})

#flame simulation conditions
d=0.03 #[m]
flame=ct.FreeFlame(gas, width=d)
#LOG LEVEL LOG LEVEL LOG LEVEL SPRAAAAAAAWDZ PLS
flame.set_refine_criteria(ratio=3, slope=0.1, curve=0.1)
lev=1

#solve
flame.solve(loglevel=lev, auto=True)
Su0=flame.velocity[0]
Su=Su0*100
print(f"Flame velocity is: {Su:.2f} cm/s")

plt.figure()
plt.title("Temperature plot")
plt.plot(flame.grid*100, flame.T, "-")
plt.xlabel("x [cm]")
plt.ylabel("T [K]")
plt.show()
