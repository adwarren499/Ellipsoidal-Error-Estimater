'''
Author: Adam Warren
This code is for the paper: Estimated Errors in Temperature between Spherical and Ellipsoidal Earth Models (2026)
submitted to Indiana Academy of Science: Science Talent Search

This code simulates conditions for the Earth for both a spherical and ellipsoidal geometry to calculate
shortwave and longwave radiation at the surface of the Earth, assuming the Earth is only water at sea level. 
Equilibrium temperatures for the surface and the atmosphere are then calculated from this radiation. This program 
outputs CSV files which can be read and graphed. The files are named based on the conditions (relative humidity, 
air temperature, relative sunlight duration), whether it is for water (wat) or air (air), whether it is for 
spherical (sp) or ellipsoidal (el) and whether it is shortwave (no gh) or longwave (gh).
'''

import numpy as np
import matplotlib.pyplot as plt
import math

R_SP = 6371008.8 # Spherical radius of Earth in m
R_SI = 6356752.3142 # Semi-minor radius of Earth (polar radius) in m
R_SA = 6378137.0 # Semi-major radius of Earth (equatorial radius) in m
E = 0.081819190842622 # Eccentricity of Earth
#L = 3.828e26 # Luminosity of the Sun
# Globally calibrated constants for Angstrom model (Yang and Koike)
B1 = 0.1715
B2 = 0.8419
B3 = -0.3206
A1 = 0.3139
A2 = 0.248
A3 = 0.1276
A4 = 0.1811
P0 = 101325.0 # Sea level atm pressure in Pa

#areas = []
s_normals = np.zeros((90, 3))
e_normals = np.zeros((90, 3))
deltaT_air_el = np.zeros((90, 365))
deltaT_air_sp = np.zeros((90, 365))
deltaT_w_sp = np.zeros((90, 365))
deltaT_w_el = np.zeros((90, 365))
Qarray_el = np.zeros((90, 365))
Qarray_sp = np.zeros((90, 365))
normal_dot_flux = []
total_flux = []

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
            vmax=1
        )

    fig.colorbar(im, ax=ax)
    plt.xlabel("Day")
    plt.ylabel("Latitude")
    if case == False:
        plt.title(title)
    elif case == True:
        plt.title(title)
    plt.tight_layout()

def r(theta):
    # Calculates the distance from the center of an ellipse to a point on the ellipse given the angle theta 
    # between the "positive" semi-major axis and r
    r = (R_SI)/(math.sqrt(1 - (E * math.cos(theta))**2))

    return r

def s_get_normals(time_seconds):
    global s_normals
    # Gets normal vector of each sector on spherical Earth as a function of time
    OMEGA = 7.27220521664e-5  # Earth's solar rotation speed (rad/s)

    lat1 = -89.0
    
    # Calculate the new common longitude for the entire strip as it rotates
    lon_rad = 0.0
    lon_rad += OMEGA * time_seconds

    p = 0
    while p < 90:
        # Compute Cartesian coordinates for all 90 patches
        lat1_rad = math.radians(lat1)
        x = R_SP * np.cos(lat1_rad) * np.cos(lon_rad)
        y = R_SP * np.cos(lat1_rad) * np.sin(lon_rad)
        z = R_SP * np.sin(lat1_rad)

        norm = np.array([x, y, z])

        n_hat = norm / R_SP
        # Lists are organized by South Pole to Equator to North Pole
        s_normals[p] = [-n_hat[0], -n_hat[1], -n_hat[2]]
        
        lat1 += 2
        p += 1
    return s_normals

def s_calc_flux(temp, rh, n):
    # Calculates flux of each sector based on the normal vector at each hour and flux vector at each day for spherical Earth
    global s_daily_Q, H_sp, Hs_hybrid, delta_t, deltaT_w_sp
    s_daily_Q = np.zeros((90, 365))
    H_sp = np.zeros((90, 365))
    Hs_hybrid = np.zeros((90, 365))
    delta_t = 3600
    for j in range(0, 365):
        # Calculate solar declination angle and flux vector by day
        solar_declination_angle = np.radians(23.45 * math.sin((360/365) * (float(j) + 284.0)*(math.pi/180))) # El Mghouchi et al.
        '''sol_cst = L/(4 * math.pi * (1 + 0.034 * math.cos(j - 2))**2)'''
        sol_cst = 1367 * (1/(1 + 0.034 * math.cos((j - 2)*math.pi/180)))**2 # El Mghouchi et al.
        x_f = sol_cst * math.cos(solar_declination_angle)
        z_f = sol_cst * math.sin(solar_declination_angle)
        flux_vector = np.array([x_f, 0, z_f])

        for t in range(0, 24):
            # Calculate normal vector of each sector every hour
            s_get_normals(t * delta_t)
            limit = math.pi/2.0
            for p in range(0, 90):
                # Calculate flux for each sector
                relative_angle = np.arccos(np.dot(flux_vector, s_normals[p])/sol_cst)

                if relative_angle < limit:
                    flux_0 = np.dot(flux_vector, s_normals[p])
                    s_daily_Q[p, j] += flux_0*delta_t
                    hybrid_model("sphere", flux_0, 2*p-89, j, temp, rh)
                    Hs_clear = R_clear*delta_t

                    if n > 0:
                        H_sp[p, j] = s_daily_Q[p, j] * (A1 + A2 * (n) + A3 * (n)**2) # Yang and Koike
                    else:
                        H_sp[p, j] = s_daily_Q[p, j] * A4 # Yang and Koike

                    if n > 0:
                        Hs_hybrid[p, j] += Hs_clear * (0.4560 + 0.3566 * n + 0.1874 * n**2) # Yang and Koike
                    else:
                        Hs_hybrid[p, j] += Hs_clear * 0.2640 # Yang and Koike
                deltaT_w_sp[p, j] = Hs_hybrid[p, j] * 0.97 / (3960 * 10250)
    #graph_main(Hs_hybrid, 'coolwarm', 'Sphere Hybrid')
    #graph_main(H_sp, 'coolwarm', 'Sphere Hourly Angstrom')
    
    return s_daily_Q, H_sp, Hs_hybrid, deltaT_w_sp

def e_get_normals(time_seconds):
    global e_normals
    OMEGA = 7.27220521664e-5  # Earth's solar rotation speed (rad/s)

    lat1 = -89.0
    
    # Calculate the new common longitude for the entire strip as it rotates
    lon_rad = 0.0
    lon_rad += OMEGA * time_seconds

    p = 0
    while p < 90:
        # Compute Cartesian coordinates for all 90 patches
        lat1_rad = math.radians(lat1)
        x = (r(lat1_rad) * np.cos(lat1_rad) * np.cos(lon_rad)) / R_SA**2
        y = (r(lat1_rad) * np.cos(lat1_rad) * np.sin(lon_rad)) / R_SA**2
        z = (r(lat1_rad) * np.sin(lat1_rad)) / R_SI**2

        norm = np.array([x, y, z])

        n_hat = norm / np.linalg.norm(norm)
        # Lists are organized by South Pole to Equator to North Pole
        e_normals[p] = [-n_hat[0], -n_hat[1], -n_hat[2]]
        
        lat1 += 2
        p += 1
    return e_normals

def e_calc_flux(temp, rh, n):
    global e_daily_Q, H_el, delta_t, He_hybrid, delta_t, deltaT_w_el
    e_daily_Q = np.zeros((90, 365))
    H_el = np.zeros((90, 365))
    He_hybrid = np.zeros((90, 365))
    delta_t = 3600
    for j in range(0, 365):
        solar_declination_angle = np.radians(23.45 * math.sin((360/365) * (float(j) + 284.0)*(math.pi/180))) # El Mghouchi et al.
        '''sol_cst = L/(4 * math.pi * (1 + 0.034 * math.cos(j - 2))**2)'''
        sol_cst = 1367 * (1/(1 + 0.034 * math.cos((j - 2)*math.pi/180)))**2 # El Mghouchi et al.
        x_f = sol_cst * math.cos(solar_declination_angle)
        z_f = sol_cst * math.sin(solar_declination_angle)
        flux_vector = np.array([x_f, 0, z_f])

        for t in range(0, 24):
            e_get_normals(t * delta_t)
            limit = math.pi/2.0
            for p in range(0, 90):
                cos_angle = np.dot(flux_vector, e_normals[p]) / sol_cst
                cos_angle = np.clip(cos_angle, -1.0, 1.0)

                relative_angle = np.arccos(cos_angle)

                if relative_angle < limit:
                    flux_0 = np.dot(flux_vector, e_normals[p])
                    e_daily_Q[p, j] += flux_0*delta_t
                    hybrid_model("ellipse", flux_0, 2*p-89, j, temp, rh)
                    He_clear = R_clear*delta_t

                    if n > 0:
                        H_el[p, j] = e_daily_Q[p, j] * (A1 + A2 * (n) + A3 * (n)**2) # Yang and Koike
                    else:
                        H_el[p, j] = e_daily_Q[p, j] * A4 # Yang and Koike

                    if n > 0:
                        He_hybrid[p, j] += He_clear * (0.4560 + 0.3566 * n + 0.1874 * n**2) # Yang and Koike
                    else:
                        He_hybrid[p, j] += He_clear * 0.2640 # Yang and Koike
                deltaT_w_el[p, j] = He_hybrid[p, j] * 0.97 / (3960 * 10250) # Temp change in first 10 m of water
    #graph_main(He_hybrid, 'coolwarm', 'Ellipse Hybrid')
    #graph_main(H_el, 'coolwarm', 'Ellipse Hourly Angstrom')

    return e_daily_Q, H_el, He_hybrid, deltaT_w_el

def angstrom_model(n):
    global H_sp_daily, H_el_daily
    H_sp_daily = np.zeros((90, 365))
    H_el_daily = np.zeros((90, 365))
    
    # Yang and Koike
    for j in range(0, 365):
        for p in range(0, 90):
            H_sp_daily[p, j] = s_daily_Q[p, j] * (B1 + B2 * (n) + B3 * (n)**2)
            H_el_daily[p, j] = e_daily_Q[p, j] * (B1 + B2 * (n) + B3 * (n)**2)
    #graph_main(H_el_daily, 'coolwarm', 'Ellipse Daily Angstrom')
    #graph_main(H_sp_daily, 'coolwarm', 'Sphere Daily Angstrom')

    return H_sp_daily, H_el_daily

def hybrid_model(shape, flux_0, lat1, j, temp, rh):
    global R_clear, deltaT_air_el, deltaT_air_sp, Qarray_el, Qarray_sp

    p = int((lat1 + 89) / 2)
    deg_to_rad = math.pi/180
    if shape == 'sphere':
        g = 9.80665 # Gravitational acceleration at sea level for sphere Earth in m/s^2
    elif shape == 'ellipse':
        g = 9.780327 * (1 + 0.0053024 * (math.sin(lat1 * deg_to_rad))**2 - 0.0000059 * (math.sin(2 * lat1 * deg_to_rad))**2) # International Gravity Formula 1967
        # Gravitational acceleration at sea level for elliptical Earth in m/s^2

    z = 0 # Surface elevation from sea level in m
    surface_pressure = P0 * math.exp(-z/((287 * temp)/g)) # Yang and Koike
    air_mass = surface_pressure/g

    temp_c = temp - 273.15
    e_s = 610.78 * math.exp((17.27 * temp_c)/(temp_c + 237.3)) # UAlberta Tetens equation
    e = e_s * rh/100
    r = (0.622 * e)/(surface_pressure - e)
    C_p = (1005 + 1845 * r)/(1 + r) # Given from dry air specific heat plus rh * specific heat of water vapor
    pwat = 0.00493 * (rh/temp) * math.exp(26.23 - (5416/temp)) # Yang and Koike

    # Julian day, given from Yang and Koike
    if j <= 300:
        d = j
    elif j > 300:
        d = j - 366

    ozone_thickness = 0.44 - 0.16 * math.sqrt(((abs(lat1) - 80) / 60)**2 + ((d - 120)/(263 - abs(lat1)))**2) # Yang and Koike

    turbidity_coef = (0.025 + 0.1 * (math.cos(lat1 * deg_to_rad))**2) * math.exp((-0.7 * z)/1000) # Yang and Koike

    s_dec = np.radians(23.45 * math.sin((360/365) * (float(j) + 284.0)*(math.pi/180))) # El Mghouchi et al.
    sol_cst = 1367 * (1/(1 + 0.034 * math.cos((j - 2)*math.pi/180)))**2 # El Mghouchi et al.
    x_f = sol_cst * math.cos(s_dec)
    z_f = sol_cst * math.sin(s_dec)
    flux_vector = np.array([x_f, 0, z_f])

    if shape == 'ellipse':
        h = math.pi/2 - np.arccos(np.dot(flux_vector, e_normals[p])/sol_cst) # Solar elevation angle in rad
    elif shape == 'sphere':
        h = math.pi/2 - np.arccos(np.dot(flux_vector, s_normals[p])/sol_cst) # Solar elevation angle in rad
    m = 1/(math.sin(h) + 0.15 / (57.296 * h + 3.885)**1.253) # Relative air mass given by Yang and Koike
    m_prime = m * (surface_pressure/1.013e5) # Pressure-corrected air mass given by Yang and Koike

    tau_g = math.exp(-0.0117 * m_prime**0.3139) # Broadband radiative transmittance due to permanent gas absorption, given by Yang and Koike

    tau_r = math.exp(-0.008735 * m_prime * (0.547 + 0.014 * m_prime - 0.00038 * m_prime**2 + 4.6*10**(-6)*m_prime**3)**-4.08) # Rayleigh scattering, given by Yang and Koike

    if rh != 0:
        tau_w = min(1.0, 0.909 - 0.036 * math.log(m * pwat)) # Water vapor absorption, given by Yang and Koike
    else:
        tau_w = 1

    tau_oz = math.exp(-0.0365 * (m * ozone_thickness)**0.7136) # Ozone absorption, given by Yang and Koike

    tau_a = math.exp(-m * turbidity_coef * (0.6777 + 0.1464 * m * turbidity_coef - 0.00626 * (m * turbidity_coef)**2)**-1.3) # Aerosol extinction, given by Yang and Koike

    tau_bclear = max(0, tau_oz * tau_w * tau_g * tau_r * tau_a - 0.013) # Broadband solar beam radiative transmittance on a clear day, given by Yang and Koike

    tau_dclear = 0.5 * (tau_oz * tau_g * tau_w * (1 - tau_a * tau_r) + 0.013) # Solar diffuse radiative transmittance on a clear day, given by Yang and Koike

    Qair = flux_0*((1-tau_w)+(1-tau_oz)+(1-tau_g))*delta_t

    if shape == 'ellipse':
        deltaT_air_el[p, j] += Qair / (C_p * air_mass)
        Qarray_el[p, j] += Qair
    elif shape == 'sphere':
        deltaT_air_sp[p, j] += Qair / (C_p * air_mass)
        Qarray_sp[p, j] += Qair


    '''if lat1 == 1 and j == 81:
        print("tau_b = ", tau_bclear)
        print("tau_d = ", tau_dclear)
        print("tau_g = ", tau_g)
        print("tau_w = ", tau_w)
        print("tau_oz = ", tau_oz)'''

    
    R_bclear = flux_0 * tau_bclear # Yang and Koike
    R_dclear = flux_0 * tau_dclear # Yang and Koike
    R_clear = R_bclear + R_dclear # Yang and Koike

    return R_clear, deltaT_air_sp, deltaT_air_el, Qarray_el, Qarray_sp

SIGMA = 5.670374419E-8 # Boltzmann constant in W/(m^2 * K^4)
EPSILON = 0.78
temp_s_sp = np.zeros((90, 365))
temp_a_sp = np.zeros((90, 365))
temp_s_el = np.zeros((90, 365))
temp_a_el = np.zeros((90, 365))

def greenhouse(shape):
    for p in range(0, 90):
        for j in range(0, 365):
            if shape == 'Sphere':
                Qarray_sp[p, j] /= 86400
                Qwat = 3960 * 10250 * deltaT_w_sp[p, j] / 86400
                temp_s_sp[p, j] = ((2 * Qwat + Qarray_sp[p, j]) / (2 * SIGMA - EPSILON * SIGMA))**(1/4)
                temp_a_sp[p, j] = (((temp_s_sp[p, j]**4) / EPSILON) - (Qwat / (SIGMA * EPSILON)))**(1/4)
            elif shape == 'Ellipse':
                Qarray_el[p, j] /= 86400
                Qwat = 3960 * 10250 * deltaT_w_el[p, j] / 86400
                temp_s_el[p, j] = ((2 * Qwat + Qarray_el[p, j]) / (2 * SIGMA - EPSILON * SIGMA))**(1/4)
                temp_a_el[p, j] = (((temp_s_el[p, j]**4) / EPSILON) - (Qwat / (SIGMA * EPSILON)))**(1/4)

    return temp_s_sp, temp_a_sp, temp_s_el, temp_a_el

for rh in range(0, 5):
    rh = rh * 25

    for temp in range(0, 5):
        temp = temp * 8 + 273

        for n in range(0, 3):
            n = n / 2

            # Reset for each independent simulation
            temp_s_sp.fill(0.0)
            temp_a_sp.fill(0.0)
            temp_s_el.fill(0.0)
            temp_a_el.fill(0.0)
            Qarray_sp.fill(0.0)
            Qarray_el.fill(0.0)

            e_calc_flux(temp, rh, n)
            s_calc_flux(temp, rh, n)
            angstrom_model(n)
            greenhouse('Ellipse')
            greenhouse('Sphere')

            np.savetxt(
                f'{rh}_{temp}_{n}_wat_el_gh.csv',
                temp_s_el, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_air_el_gh.csv',
                temp_a_el, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_wat_sp_gh.csv',
                temp_s_sp, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_air_sp_gh.csv',
                temp_a_sp, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_wat_el.csv',
                deltaT_w_el, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_air_el.csv',
                deltaT_air_el, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_wat_sp.csv',
                deltaT_w_sp, delimiter=','
            )
            np.savetxt(
                f'{rh}_{temp}_{n}_air_sp.csv',
                deltaT_air_sp, delimiter=','
            )