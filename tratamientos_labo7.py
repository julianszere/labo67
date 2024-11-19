# -*- coding: utf-8 -*-
#%%
from water import WaterTreatment
from signals import SignalHandler, SignalReff, SignalZoom, Signals
import constants as c
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import curve_fit
from scipy import integrate
import uncertainties.unumpy as unp

params = {
    'figure.figsize': (10, 5),
    'axes.grid': True,
    'grid.linestyle': ':',
    'grid.linewidth': 0.5,
    'axes.axisbelow': True,
    'legend.fontsize': 15,
    'xtick.labelsize': 12.5,
    'ytick.labelsize': 12.5,
    'axes.labelsize': 17.5,
    'axes.prop_cycle': plt.cycler('color', ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"])
}

plt.rcParams.update(params)

def pp(folder):
    s = WaterTreatment(folder)
    s.plot_degradation(folder)
    plt.legend()
    print(s)
    

# %%
'''
Extrañas mediciones de potencia.
'''
print(Signals('22-08/e4'))
print(Signals('05-07/tratamiento-e4-e6-titanio'))
print(Signals('22-08/e4-e6'))
print(Signals('22-08/e4-e6-zoom'))

# %%
'''
Vemos que las mediciones de la última clase antes de las vacaciones tienen sentido si dividimos por diez.
'''
path = '05-07/tratamiento-e4-e6-vidrio/zoom/e4-e6-vidrio 2024-07-05 09h 34m 28s.csv'
sh = SignalHandler(path)
sz = SignalZoom(path,1)

plt.plot(sh.tI, sh.I/10, label='Original', color='red')
plt.plot(sz.t, sz.I/10, label='Filtro', color='blue')

path = '22-08/e4-e6/e4-e6 2024-08-22 11h 08m 31s.csv'
sh = SignalHandler(path)
sz = SignalZoom(path,1)

plt.plot(sh.tI, sh.I, color='green')
plt.plot(sz.t, sz.I, color='black')

plt.legend()

# %%
'''
Comparamos mediciones de teflón con vidrio, metal y nada; todo para el e4.
'''
pp('27-08/tratamiento-e4-aluminio')
pp('18-06/tratamiento-e4-vidrio')
pp('04-06/tratamiento-e4')

# %%
'''
Comparamos el vidrio solo con TiO2
'''
pp('25-06/tratamiento-e4-TiO2')
pp('18-06/tratamiento-e4-vidrio')
pp('13-06/tratamiento-e4-TiO2')

# %%
'''
Comparamos mediciones con recubrimiento grueso y fino de TiO2 y con metal solo.
'''
pp('29-08/tratamiento-e4-tio2_grueso/30-40 min')
pp('13-06/tratamiento-e4-TiO2')
pp('27-08/tratamiento-e4-aluminio')

# %%
''' 
Vemos que el reactor de mati también da mal porque la fuente de continua no llega a dar los 10kV.
'''
print(Signals('29-08/reactor mati'))

# %%
'''
Comparamos mediciones sin y con recubrimiento (grueso) (y sin recubrimiento de otra clase).
Vemos que antes tratábamos más y que aumentar el voltaje de ac no sirvió.
'''
pp('03-09/tratamiento-e4-Vidrio-10ppm-150ml/30-60 min')
pp('03-09/tratamiento-e4-VidrioTiO2Grueso-10ppm-150ml')
pp('18-06/tratamiento-e4-vidrio')

# %%
'''
Comparamos mediciones sin nada y con metal. Sin nada dio mejor.
'''
pp('24-09/tratamiento_e4-10ppm-150ml')
pp('24-09/tratamiento_e4-Metal-10ppm-150ml')

# %%
'''
Comparamos dos teflones contra un teflón. Un solo teflón da mejor.
'''
pp('26-09/tratamiento_e4e6-10ppm-150ml')
pp('24-09/tratamiento_e4-10ppm-150ml')

# %%
'''
Dos teflones de nuevo
'''
pp('01-10/tratamiento-e4e6_Vidrio_10ppm_150ml')
pp('26-09/tratamiento_e4e6-10ppm-150ml')

# %%
'''
Ni con el e4 ni con el e6 pudimos tratar
Seguramente fuera porque no estaban cruzando los streamers
'''
pp('03-10/tratamiento_e4-1ppm-150ml')
pp('03-10/tratamiento_e6-1ppm-150ml')

# %%
'''
Comparamos tratamiento con metal y metal con TiO2
Las mediciones son super ruidosas a 1 ppm
'''
pp('08-10/tratamiento-e4_Metal_1ppm_150ml')
pp('08-10/tratamiento-e4_MetalTiO2Grueso_1ppm_150ml')

# %%
'''
Comparamos la degradación de 1ppm con la de 5ppm
'''
pp('15-10/tratamiento-e4_Metal_5ppm_150ml')
pp('08-10/tratamiento-e4_MetalTiO2Grueso_1ppm_150ml')

# %%
'''
Cambiamos la manguera y tomamos una medición de 1ppm que da como las de 10ppm
'''
pp('17-10/tratamiento_e6-150ml-1ppm')
pp('04-06/tratamiento-e4')
plt.xlim(-10,60)

# %%
'''
Comparamos dos electrodos a 15 kVpp contra un electrodo a 16kVpp y un electrodo a 15kVpp
Da más o menos parecido. Quizás sea porque en el de dos electrodos usamos caudal a 40% en vez de a 60% sin querer
'''
pp('17-10/tratamiento_e6-150ml-1ppm')
#pp('29-10/tratamiento_e4e6-150ml-1ppm') # Esta medición la vamos a descartar
pp('31-10/tratamiento_e4-150ml-1ppm')
pp('05-11/tratamiento_e4e6-150ml-1ppm')

# %%

path_e4 = c.ROOT + '/05-11/pH_e4-150ml-1ppm/pH_e4-150ml-1ppm.txt'
path_e4e6 = c.ROOT + '/05-11/pH_e4e6-150ml-1ppm/pH_e4e6-150ml-1ppm.txt'

datos_e4 = np.loadtxt(path_e4, skiprows=1).T  # or use sep='\t' for tab-separated
datos_e4e6 = np.loadtxt(path_e4e6, skiprows=1).T  # or use sep='\t' for tab-separated

t, pH1, pH_err1, pot_red1, pot_red_err1 = datos_e4  # Use 'Time' or any column you want for the x-axis
t, pH2, pH_err2, pot_red2, pot_red_err2 = datos_e4e6  # Use 'Time' or any column you want for the x-axis

# Step 3: Plot the data
plt.scatter(t, pH1, color='red')
plt.errorbar(t, pH1, yerr=pH_err1, label='pH-e4', color='red')
plt.scatter(t, pH2, color='blue')
plt.errorbar(t, pH2, yerr=pH_err2, label='pH-e4e6', color='blue')

plt.xlabel('t [min]')
plt.ylabel('pH')
plt.legend()
plt.show()

# %%

plt.scatter(t, pot_red1, color='red')
plt.errorbar(t, pot_red1, yerr=pot_red_err1, label='Potencial Redox-e4', color='red')
plt.scatter(t, pot_red2, color='blue')
plt.errorbar(t, pot_red2, yerr=pot_red_err2, label='Potencial Redox-e4e6', color='blue')

plt.xlabel('t [min]')
plt.ylabel('Potencial Redox [mV]')
plt.legend()
plt.show()

