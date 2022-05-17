import cantera as ct
import matplotlib.pyplot as plt

# initial conditions
print('Set up initial conditions:')
T0 = float(input("temperature [K]: T_0= "))
p0 = float(input("pressure [Pa]: p_0= "))
# defining gas mixture
gas = ct.Solution('gri30.yaml')

gas.set_equivalence_ratio(0.9, "C2H6", {"O2": 1.0, "N2": 3.76})
gas()
# flame simulation conditions
d = 0.1  # [m]
flame = ct.FreeFlame(gas, width=d)
flame.set_refine_criteria(ratio=2, slope=0.1, curve=0.1)
lev = 1  # flag that "defines" solution accuracy. higher levels will highly increase computation time.

# solve
flame.solve(loglevel=lev, refine_grid=True, auto=True)

print(f"Flame velocity is: {100 * flame.velocity[0]:.2f} cm/s")
print(f"Max temperature is: {max(flame.T):.2f}")
plt.figure()
plt.title("Temperature plot")
plt.plot(flame.grid * 100, flame.T, "-")
plt.xlabel("y [cm]")
plt.ylabel("T [K]")
plt.show()

plt.figure()
plt.title("Velocity plot")
plt.plot(flame.grid * 100, 100 * flame.velocity, "-")
plt.xlabel("y [cm]")
plt.ylabel("Su [cm/s]")
plt.show()

# for i, specie in enumerate(gas.species()): #used to get specific spieces indexes. function is enabled just once when mixture (fuel) is changed
# print(f"{i}. {specie}")
x_fuel = flame.X[26]  # based on for above
x_co2 = flame.X[15]
x_h2o = flame.X[5]
x_o2 = flame.X[3]
# plotting
plt.plot(flame.grid * 100, x_fuel, "-", label="$C_{2}H_{6}$")  # flame.grid*100 rescale to cm
plt.plot(flame.grid * 100, x_co2, "-", label="$CO_{2}$")
plt.plot(flame.grid * 100, x_h2o, "-", label="$H_{2}O$")
plt.plot(flame.grid * 100, x_o2, "-", label="$O_{2}$")

plt.legend(loc=1)
plt.xlabel("y [cm]")
plt.ylabel("mole_fractions")
plt.show()
