import cantera as ct
import matplotlib.pyplot as plt

# initial conditions
print('Set up initial conditions:')
T0 = float(input("temperature [K]: T_0= "))
p0 = float(input("pressure [Pa]: p_0= "))
# defining gas mixture
gas = ct.Solution('gri30.yaml')
gas.set_equivalence_ratio(0.1, "C2H6", {"O2": 1.0, "N2": 3.76})

# flame simulation conditions
d = 0.05  # [m]
flame = ct.FreeFlame(gas, width=d)
# LOG LEVEL LOG LEVEL LOG LEVEL SPRAAAAAAAWDZ PLS
flame.set_refine_criteria(ratio=3, slope=0.1, curve=0.1)
lev = 1

# solve
flame.solve(loglevel=lev, auto=True)
Su0 = flame.velocity[0]
Su = Su0 * 100
print(f"Flame velocity is: {Su:.2f} cm/s")

plt.figure()
plt.title("Temperature plot")
plt.plot(flame.grid * 100, flame.T, "-")
plt.xlabel("y [cm]")
plt.ylabel("T [K]")
plt.show()


#for i, specie in enumerate(gas.species()): #used to get specific spieces indexes. function is enabled just once when mixture (fuel) is changed
    #print(f"{i}. {specie}")
x_fuel = flame.X[26]    #based on for above
x_co2 = flame.X[15]
x_h2o = flame.X[5]
x_o2 = flame.X[3]

#plotting
plt.plot(flame.grid * 100, x_fuel, "-", label="$C_{2}H_{6}$") #flame.grid*100 rescale to cm
plt.plot(flame.grid * 100, x_co2, "-", label="$CO_{2}$")
plt.plot(flame.grid * 100, x_h2o, "-", label="$H_{2}O$")
plt.plot(flame.grid * 100, x_o2, "-", label="$O_{2}$")
for items in flame.grid:

plt.legend(loc=1)
plt.xlabel("y [cm]")
plt.ylabel("mole_fractions")
plt.show()
