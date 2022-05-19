import cantera as ct
import matplotlib.pyplot as plt
import numpy as np
import os
# initial conditions
print('Set up initial conditions:')
T0 = float(input("temperature [K]: T_0= "))
p0 = float(input("pressure [Pa]: p_0= "))

#plots style config
plt.style.use("ggplot")
plt.style.use("seaborn-deep")

Tmax = []
V = []
x = []
help_me1 = np.arange(start=0.5, stop=1.3, step=0.1)
help_me2 = np.arange(start=1.3, stop=3, step=0.4)
help_me3 = np.append(x, np.arange(start=3, stop=8, step=1))
x = np.concatenate((help_me1, help_me2, help_me3))  # different step based on the intensity of the value changes, the only method i found working
i = 0
for items in x:
    # defining gas mixture
    gas = ct.Solution('gri30.yaml')
    gas.set_equivalence_ratio(x[i], "C2H6", {"O2": 1.0, "N2": 3.76})
    print(f"Initial mole fraction of fuel: {x[i]}")

    # flame simulation conditions
    d = 0.1  # [m]
    flame = ct.FreeFlame(gas, width=d)
    flame.set_refine_criteria(ratio=2, slope=0.1, curve=0.1)
    lev = 1  # flag that "defines" solution accuracy. higher levels will highly increase computation time.

    # solve
    flame.solve(loglevel=lev, refine_grid=True, auto=True)
    Tmax.append(max(flame.T))
    V.append(flame.velocity[0])
    print(f"Flame velocity is: {100 * flame.velocity[0]:.2f} cm/s")
    print(f"Max temperature is: {max(flame.T):.2f} K")

    #plotting
    plt.figure()
    plt.title(f"Temperature plot x={x[i]:.2f}")
    plt.plot(flame.grid * 100, flame.T, "-")
    plt.xlabel("y [cm]")
    plt.ylabel("T [K]")
    #plt.show()
    plt.savefig(f"/Users/michalsiniarski/venv_komp_spal/results_all/temperature_{x[i]:.2f}.png")

    # plt.figure()
    # plt.title("Velocity plot")
    # plt.plot(flame.grid * 100, 100 * flame.velocity, "-")
    # plt.xlabel("y [cm]")
    # plt.ylabel("Su [cm/s]")
    # plt.show()

    # for i, specie in enumerate(gas.species()): #used to get specific spieces indexes. function is enabled just once when mixture (fuel) is changed
    # print(f"{i}. {specie}")
    x_fuel = flame.X[26]  # based on "for" above
    x_co2 = flame.X[15]
    x_h2o = flame.X[5]
    x_o2 = flame.X[3]

    plt.figure()
    plt.plot(flame.grid * 100, x_fuel, "-", label="$C_{2}H_{6}$")  # flame.grid*100 rescale to cm
    plt.plot(flame.grid * 100, x_co2, "-", label="$CO_{2}$")
    plt.plot(flame.grid * 100, x_h2o, "-", label="$H_{2}O$")
    plt.plot(flame.grid * 100, x_o2, "-", label="$O_{2}$")

    plt.legend(loc=1)
    plt.xlabel("y [cm]")
    plt.ylabel("mole_fractions")
    #plt.show()
    plt.savefig(f"/Users/michalsiniarski/venv_komp_spal/results_all/mole_fractions_{x[i]:.2f}.png")
    i += 1

# sum up plots
plt.figure()
plt.title("Max temperature plot")
plt.plot(x, Tmax, "-o")
plt.xlabel("Initial mole fractions of fuel")
plt.ylabel("Tmax [K]")
#plt.show()
plt.savefig(f"/Users/michalsiniarski/venv_komp_spal/results_all/SUMUP/temperature.png")

plt.figure()
plt.title("Flame velocity")
plt.plot(x, V, "-o")
plt.xlabel("Initial mole fractions of fuel")
plt.ylabel("V [m/s]")
#plt.show()
plt.savefig(f"/Users/michalsiniarski/venv_komp_spal/results_all/SUMUP/velocity.png")
