'''
Author: Adam Warren
This code is for the paper: Estimated Errors in Temperature between Spherical and Ellipsoidal Earth Models (2026)
submitted to Indiana Academy of Science: Science Talent Search

This code takes the CSV files with equilibrium temperature data and plots them using matplotlib.pyplot. 
Differences between temperatures are also calculated and plotted for equal conditions between spherical and ellipsoidal
Earth models.
'''

import matplotlib.pyplot as plt
import numpy as np
# 1 is water, 2 is air

maxallTT1 = np.zeros((90,365))
maxallTT2 = np.zeros((90,365))
maxrhTT1 = np.zeros((90,365))
maxrhTT2 = np.zeros((90,365))
maxtTT1 = np.zeros((90,365))
maxtTT2 = np.zeros((90,365))
maxnTT1 = np.zeros((90,365))
maxnTT2 = np.zeros((90,365))
maxrhtTT1 = np.zeros((90,365))
maxrhtTT2 = np.zeros((90,365))
maxrhnTT1 = np.zeros((90,365))
maxrhnTT2 = np.zeros((90,365))
maxtnTT1 = np.zeros((90,365))
maxtnTT2 = np.zeros((90,365))
minTT1 = np.zeros((90,365))
minTT2 = np.zeros((90,365))
minnoghdeltaTT1 = np.zeros((90,365))
minnoghdeltaTT2 = np.zeros((90,365))
maxallnoghdeltaTT1 = np.zeros((90,365))
maxallnoghdeltaTT2 = np.zeros((90,365))
mednoghdeltaTT1 = np.zeros((90,365))
mednoghdeltaTT2 = np.zeros((90,365))
medTT1 = np.zeros((90,365))
medTT2 = np.zeros((90,365))

def graph_main(array, color, title, case=False):
    fig, ax = plt.subplots(figsize=(12, 5))

    if case == False:
        im = ax.imshow(
            array,
            cmap=color,
            aspect="auto",
            origin="lower",
            extent=[0.5, 365.5, -90, 90],
            interpolation="nearest",
        )
    if case == True:
        im = ax.imshow(
            array,
            cmap=color,
            aspect="auto",
            origin="lower",
            extent=[0.5, 365.5, -90, 90],
            interpolation="nearest",
            vmin=0,
            vmax=2
        )

    fig.colorbar(im, ax=ax)
    plt.xlabel("Day")
    plt.ylabel("Latitude")
    plt.title(title)
    plt.tight_layout()

# Loads all CSV files into 2d arrays that can be plotted
maxallT1s = np.loadtxt('100_305_1.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxallT2s = np.loadtxt('100_305_1.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxallT1e = np.loadtxt('100_305_1.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxallT2e = np.loadtxt('100_305_1.0_air_el_gh.csv', delimiter=',', ndmin=2)

maxrhT1s = np.loadtxt('100_273_0.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxrhT2s = np.loadtxt('100_273_0.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxrhT1e = np.loadtxt('100_273_0.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxrhT2e = np.loadtxt('100_273_0.0_air_el_gh.csv', delimiter=',', ndmin=2)

maxtT1s = np.loadtxt('0_305_0.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxtT2s = np.loadtxt('0_305_0.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxtT1e = np.loadtxt('0_305_0.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxtT2e = np.loadtxt('0_305_0.0_air_el_gh.csv', delimiter=',', ndmin=2)

maxnT1s = np.loadtxt('0_273_1.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxnT2s = np.loadtxt('0_273_1.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxnT1e = np.loadtxt('0_273_1.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxnT2e = np.loadtxt('0_273_1.0_air_el_gh.csv', delimiter=',', ndmin=2)

maxrhtT1s = np.loadtxt('100_305_0.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxrhtT2s = np.loadtxt('100_305_0.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxrhtT1e = np.loadtxt('100_305_0.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxrhtT2e = np.loadtxt('100_305_0.0_air_el_gh.csv', delimiter=',', ndmin=2)

maxrhnT1s = np.loadtxt('100_273_1.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxrhnT2s = np.loadtxt('100_273_1.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxrhnT1e = np.loadtxt('100_273_1.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxrhnT2e = np.loadtxt('100_273_1.0_air_el_gh.csv', delimiter=',', ndmin=2)

maxtnT1s = np.loadtxt('0_305_1.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
maxtnT2s = np.loadtxt('0_305_1.0_air_sp_gh.csv', delimiter=',', ndmin=2)
maxtnT1e = np.loadtxt('0_305_1.0_wat_el_gh.csv', delimiter=',', ndmin=2)
maxtnT2e = np.loadtxt('0_305_1.0_air_el_gh.csv', delimiter=',', ndmin=2)

minT1s = np.loadtxt('0_273_0.0_wat_sp_gh.csv', delimiter=',', ndmin=2)
minT2s = np.loadtxt('0_273_0.0_air_sp_gh.csv', delimiter=',', ndmin=2)
minT1e = np.loadtxt('0_273_0.0_wat_el_gh.csv', delimiter=',', ndmin=2)
minT2e = np.loadtxt('0_273_0.0_air_el_gh.csv', delimiter=',', ndmin=2)

minnoghdeltaT1s = np.loadtxt('0_273_0.0_wat_sp.csv', delimiter=',', ndmin=2)
minnoghdeltaT2s = np.loadtxt('0_273_0.0_air_sp.csv', delimiter=',', ndmin=2)
minnoghdeltaT1e = np.loadtxt('0_273_0.0_wat_el.csv', delimiter=',', ndmin=2)
minnoghdeltaT2e = np.loadtxt('0_273_0.0_air_el.csv', delimiter=',', ndmin=2)

maxallnoghdeltaT1s = np.loadtxt('100_305_1.0_wat_sp.csv', delimiter=',', ndmin=2)
maxallnoghdeltaT2s = np.loadtxt('100_305_1.0_air_sp.csv', delimiter=',', ndmin=2)
maxallnoghdeltaT1e = np.loadtxt('100_305_1.0_wat_el.csv', delimiter=',', ndmin=2)
maxallnoghdeltaT2e = np.loadtxt('100_305_1.0_air_el.csv', delimiter=',', ndmin=2)

mednoghdeltaT1s = np.loadtxt('50_289_0.5_wat_sp.csv', delimiter=',', ndmin=2)
mednoghdeltaT2s = np.loadtxt('50_289_0.5_air_sp.csv', delimiter=',', ndmin=2)
mednoghdeltaT1e = np.loadtxt('50_289_0.5_wat_el.csv', delimiter=',', ndmin=2)
mednoghdeltaT2e = np.loadtxt('50_289_0.5_air_el.csv', delimiter=',', ndmin=2)

medT1s = np.loadtxt('50_289_0.5_wat_sp_gh.csv', delimiter=',', ndmin=2)
medT2s = np.loadtxt('50_289_0.5_air_sp_gh.csv', delimiter=',', ndmin=2)
medT1e = np.loadtxt('50_289_0.5_wat_el_gh.csv', delimiter=',', ndmin=2)
medT2e = np.loadtxt('50_289_0.5_air_el_gh.csv', delimiter=',', ndmin=2)

# Makes every condition graph for spherical and ellipsoidal that plots the change in temperature accounting for
# longwave re-radiation
'''graph_main(maxallT1s, 'coolwarm', 'Maximum of all Conditions on the Water of a Spherical Earth')
graph_main(maxallT2s, 'coolwarm', 'Maximum of all Conditions on the Air of a Spherical Earth')
graph_main(maxallT1e, 'coolwarm', 'Maximum of all Conditions on the Water of an Ellipsoidal Earth')
graph_main(maxallT2e, 'coolwarm', 'Maximum of all Conditions on the Air of an Ellipsoidal Earth')

graph_main(maxrhT1s, 'coolwarm', 'Maximum of Relative Humidity on the Water of a Spherical Earth')
graph_main(maxrhT2s, 'coolwarm', 'Maximum of Relative Humidity on the Air of a Spherical Earth')
graph_main(maxrhT1e, 'coolwarm', 'Maximum of Relative Humidity on the Water of an Ellipsoidal Earth')
graph_main(maxrhT2e, 'coolwarm', 'Maximum of Relative Humidity on the Air of an Ellipsoidal Earth')

graph_main(maxtT1s, 'coolwarm', 'Maximum of Surface Temperature on the Water of a Spherical Earth')
graph_main(maxtT2s, 'coolwarm', 'Maximum of Surface Temperature on the Air of a Spherical Earth')
graph_main(maxtT1e, 'coolwarm', 'Maximum of Surface Temperature on the Water of an Ellipsoidal Earth')
graph_main(maxtT2e, 'coolwarm', 'Maximum of Surface Temperature on the Air of an Ellipsoidal Earth')

graph_main(maxnT1s, 'coolwarm', 'Maximum of Sunlight Duration on the Water of a Spherical Earth')
graph_main(maxnT2s, 'coolwarm', 'Maximum of Sunlight Duration on the Air of a Spherical Earth')
graph_main(maxnT1e, 'coolwarm', 'Maximum of Sunlight Duration on the Water of an Ellipsoidal Earth')
graph_main(maxnT2e, 'coolwarm', 'Maximum of Sunlight Duration on the Air of an Ellipsoidal Earth')

graph_main(maxrhtT1s, 'coolwarm', 'Maximum of Relative Humidity and Surface Temperature on the Water of a Spherical Earth')
graph_main(maxrhtT2s, 'coolwarm', 'Maximum of Relative Humidity and Surface Temperature on the Air of a Spherical Earth')
graph_main(maxrhtT1e, 'coolwarm', 'Maximum of Relative Humidity and Surface Temperature on the Water of an Ellipsoidal Earth')
graph_main(maxrhtT2e, 'coolwarm', 'Maximum of Relative Humidity and Surface Temperature on the Air of an Ellipsoidal Earth')

graph_main(maxrhnT1s, 'coolwarm', 'Maximum of Relative Humidity and Sunlight Duration on the Water of a Spherical Earth')
graph_main(maxrhnT2s, 'coolwarm', 'Maximum of Relative Humidity and Sunlight Duration on the Air of a Spherical Earth')
graph_main(maxrhnT1e, 'coolwarm', 'Maximum of Relative Humidity and Sunlight Duration on the Water of an Ellipsoidal Earth')
graph_main(maxrhnT2e, 'coolwarm', 'Maximum of Relative Humidity and Sunlight Duration on the Air of an Ellipsoidal Earth')

graph_main(maxtnT1s, 'coolwarm', 'Maximum of Surface Temperature and Sunlight Duration on the Water of a Spherical Earth')
graph_main(maxtnT2s, 'coolwarm', 'Maximum of Surface Temperature and Sunlight Duration on the Air of a Spherical Earth')
graph_main(maxtnT1e, 'coolwarm', 'Maximum of Surface Temperature and Sunlight Duration on the Water of an Ellipsoidal Earth')
graph_main(maxtnT2e, 'coolwarm', 'Maximum of Surface Temperature and Sunlight Duration on the Air of an Ellipsoidal Earth')

graph_main(minT1s, 'coolwarm', 'Minimum of all Conditions on the Water of a Spherical Earth')
graph_main(minT2s, 'coolwarm', 'Minimum of all Conditions on the Air of a Spherical Earth')
graph_main(minT1e, 'coolwarm', 'Minimum of all Conditions on the Water of an Ellipsoidal Earth')
graph_main(minT2e, 'coolwarm', 'Minimum of all Conditions on the Air of an Ellipsoidal Earth')'''

# This calculates the difference between the spherical and ellipsoidal models for the same conditions
for p in range(0, 90):
    for j in range(0, 365):
        maxallTT1[p, j] = maxallT1s[p, j] - maxallT1e[p, j]
        maxallTT2[p, j] = maxallT2s[p, j] - maxallT2e[p, j]
        maxrhTT1[p, j] = maxrhT1s[p, j] - maxrhT1e[p, j]
        maxrhTT2[p, j] = maxrhT2s[p, j] - maxrhT2e[p, j]
        maxtTT1[p, j] = maxtT1s[p, j] - maxtT1e[p, j]
        maxtTT2[p, j] = maxtT2s[p, j] - maxtT2e[p, j]
        maxnTT1[p, j] = maxnT1s[p, j] - maxnT1e[p, j]
        maxnTT2[p, j] = maxnT2s[p, j] - maxnT2e[p, j]
        maxrhtTT1[p, j] = maxrhtT1s[p, j] - maxrhtT1e[p, j]
        maxrhtTT2[p, j] = maxrhtT2s[p, j] - maxrhtT2e[p, j]
        maxrhnTT1[p, j] = maxrhnT1s[p, j] - maxrhnT1e[p, j]
        maxrhnTT2[p, j] = maxrhnT2s[p, j] - maxrhnT2e[p, j]
        maxtnTT1[p, j] = maxtnT1s[p, j] - maxtnT1e[p, j]
        maxtnTT2[p, j] = maxtnT2s[p, j] - maxtnT2e[p, j]
        minTT1[p, j] = minT1s[p, j] - minT1e[p, j]
        minTT2[p, j] = minT2s[p, j] - minT2e[p, j]

        minnoghdeltaTT1[p, j] = minnoghdeltaT1s[p, j] - minnoghdeltaT1e[p, j]
        minnoghdeltaTT2[p, j] = minnoghdeltaT2s[p, j] - minnoghdeltaT2e[p, j]
        maxallnoghdeltaTT1[p, j] = maxallnoghdeltaT1s[p, j] - maxallnoghdeltaT1e[p, j]
        maxallnoghdeltaTT2[p, j] = maxallnoghdeltaT2s[p, j] - maxallnoghdeltaT2e[p, j]
        mednoghdeltaTT1[p, j] = mednoghdeltaT1s[p, j] - mednoghdeltaT1e[p, j]
        mednoghdeltaTT2[p, j] = mednoghdeltaT2s[p, j] - mednoghdeltaT2e[p, j]
        medTT1[p, j] = medT1s[p, j] - medT1e[p, j]
        medTT2[p, j] = medT2s[p, j] - medT2e[p, j]

# Calculates and plots the average temperature for median conditions
medavgwat = np.zeros((90))
medavgair = np.zeros((90))
l = np.zeros((90))
for p in range(0, 90):
    medavgwat[p] = np.average(medTT1[p])
    medavgair[p] = np.average(medTT2[p])
    l[p] = 2*p - 89

def graph_avg(array, title):
    plt.xlabel('Latitude Tile')
    plt.ylabel('Temperature')
    plt.title(title)
    plt.xlim(-90, 90)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.plot(l, array)

graph_avg(medavgwat, r'$ΔT^{b}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')
plt.show()
graph_avg(medavgair, r'$ΔT^{b}_{a}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')
plt.show()

# Plots the differences in spherical and ellipsoidal models for max, min, and median conditions
graph_main(maxallTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = N$, $T = 305$ (K), $rh = 100$)', case=True)
graph_main(maxallTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = N$, $T = 305$ (K), $rh = 100$)', case=True)

graph_main(minTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = 0$, $T = 273$ (K), $rh = 0$)', case=True)
graph_main(minTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = 0$, $T = 273$ (K), $rh = 0$)', case=True)

graph_main(medTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)', case=True)
graph_main(medTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)', case=True)

'''graph_main(maxrhTT1, 'coolwarm', 'Maximum of Relative Humidity on Water', case=True)
graph_main(maxrhTT2, 'coolwarm', 'Maximum of Relative Humidity on Air', case=True)

graph_main(maxtTT1, 'coolwarm', 'Maximum of Surface Temperature on Water', case=True)
graph_main(maxtTT2, 'coolwarm', 'Maximum of Surface Temperature on Air', case=True)

graph_main(maxnTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = N$, $T = 273$ K, $rh = 0$)', case=True)
graph_main(maxnTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = N$, $T = 273$ K, $rh = 0$)', case=True)

graph_main(maxrhtTT1, 'coolwarm', 'Maximum of Relative Humidity and Surface Temperature on Water', case=True)
graph_main(maxrhtTT2, 'coolwarm', 'Maximum of Relative Humidity and Surface Temperature on Air', case=True)

graph_main(maxrhnTT1, 'coolwarm', 'Maximum of Relative Humidity and Sunlight Duration on Water', case=True)
graph_main(maxrhnTT2, 'coolwarm', 'Maximum of Relative Humidity and Sunlight Duration on Air', case=True)

graph_main(maxtnTT1, 'coolwarm', 'Maximum of Surface Temperature and Sunlight Duration on Water', case=True)
graph_main(maxtnTT2, 'coolwarm', 'Maximum of Surface Temperature and Sunlight Duration on Air', case=True)

graph_main(minnoghdeltaTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = 0$, $T = 273$ (K), $rh = 0$)', case=True)
graph_main(minnoghdeltaTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = 0$, $T = 273$ (K), $rh = 0$)', case=True)

graph_main(maxallnoghdeltaTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = N$, $T = 305$ (K), $rh = 100$)', case=True)
graph_main(maxallnoghdeltaTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = N$, $T = 305$ (K), $rh = 100$)', case=True)

graph_main(mednoghdeltaTT1, 'coolwarm', r'$ΔT^{b}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')
graph_main(mednoghdeltaTT2, 'coolwarm', r'$ΔT^{b}_{a}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')

graph_main(medT1s, 'coolwarm', r'$T^{s}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')
graph_main(medT1e, 'coolwarm', r'$T^{e}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')

graph_main(mednoghdeltaT1s, 'coolwarm', r'$T^{s}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')
graph_main(mednoghdeltaT1e, 'coolwarm', r'$T^{e}_{w}$ ($n = 0.5N$, $T = 289$ (K), $rh = 50$)')'''