# -*- coding: utf-8 -*-
#%%
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
    'axes.prop_cycle': plt.cycler('color', ["#b30000", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"])
}

plt.rcParams.update(params)

def plot_uv(path, label=None, control_path=None):
    ruta = path.replace("tratamiento-uv_", "")
    t, A = np.loadtxt(os.path.join(c.ROOT, f'{path}.txt'), skiprows=1).T
    A = unp.uarray(A, np.ones(len(A)) * c.A_ERR)
    C = (1 - A / A[0]) * 100
    
    # Choose a color for the error bars (grey)
    error_color = 'grey'
    
    # Plot the curve with the specified color and grey error bars
    if label is None:
        plt.errorbar(t, unp.nominal_values(C), unp.std_devs(C), label=ruta, 
                     marker='d', markersize=8, linestyle='none', ecolor=error_color, 
                     capsize=5, elinewidth=2, zorder=10)
    else:
        plt.errorbar(t, unp.nominal_values(C), unp.std_devs(C), label=label, 
                     marker='d', markersize=8, linestyle='none', ecolor=error_color, 
                     capsize=5, elinewidth=2, zorder=10)
    
    print(f'C_f {C[-1]:.2f} {label}')
    
    # Add a grid with transparency and improve readability
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.xlabel('t [min]')
    plt.ylabel('DE [%]')
    
    # Enhance plot aesthetics
    plt.tight_layout()
# %%
plot_uv('01-10/tratamiento-uv_TiO2-grueso-vidrio_1ppm')
plot_uv('01-10/tratamiento-uv_TiO2-grueso-vidrio_10ppm')

# %%
plot_uv('01-10/tratamiento-uv_TiO2-grueso-vidrio_10ppm')
plot_uv('01-10/tratamiento-uv_TiO2-grueso-vidrio_1ppm')
plot_uv('03-10/tratamiento-uv_SOLO_1ppm')
plot_uv('08-10/tratamiento-uv_TiO2-grueso-vidrio_1ppm')
plot_uv('08-10/tratamiento-uv_TiO2-grueso-vidrio_5ppm')
plot_uv('08-10/tratamiento-uv_SOLO-vidrio_1ppm')
plot_uv('15-10/tratamiento-uv_TiO2-fino-vidrio_1ppm')
plot_uv('15-10/tratamiento-uv_TiO2-grueso-vidrio_2.5ppm')
plot_uv('15-10/tratamiento-uv_TiO2-grueso-metal_1ppm')
#plot_uv('17-10/tratamiento-uv_TiO2-grueso-metal_1ppm')

#%%

files = [
    '01-10/tratamiento-uv_TiO2-grueso-vidrio_10ppm',
    '01-10/tratamiento-uv_TiO2-grueso-vidrio_1ppm',
    '03-10/tratamiento-uv_SOLO_1ppm',
    '08-10/tratamiento-uv_TiO2-grueso-vidrio_1ppm',
    '08-10/tratamiento-uv_TiO2-grueso-vidrio_5ppm',
    '08-10/tratamiento-uv_SOLO-vidrio_1ppm',
    '15-10/tratamiento-uv_TiO2-fino-vidrio_1ppm',
    '15-10/tratamiento-uv_TiO2-grueso-vidrio_2.5ppm',
    '15-10/tratamiento-uv_TiO2-grueso.metal_1ppm',
    '24-10/tratamiento-uv_TiO2-grueso-vidrio_1ppm',
    '29-10/tratamiento-uv_TiO2_fino_vidrio'
]

labels = ['24-09/TiO2-grueso-vidrio_10ppm']
concentrations = [0.077]

for file in files:
    label = file.replace("tratamiento-uv_", "")
    t, A = np.loadtxt(os.path.join(c.ROOT, f'{file}.txt'), skiprows=1).T
    C = 1 - A/A[]
    last_concentration = C[-1]
    print(f'C_f {last_concentration:.2f} {label}')
    labels.append(label)
    concentrations.append(last_concentration)

    
# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(labels, concentrations, color='skyblue')
plt.ylabel('DE [%]')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()


# %%

t, A1, A2, A3, A_avg = np.loadtxt(os.path.join(c.ROOT, '15-10/no-tratamiento.txt'), skiprows=1).T
plt.plot(t,A1,color='red')
plt.plot(t,A1,'o',color='red',label='Medición 1')
plt.plot(t,A2,color='blue')
plt.plot(t,A2,'o',color='blue',label='Medición 2')
plt.plot(t,A3,color='green')
plt.plot(t,A3,'o',color='green',label='Medición 3')
plt.plot(t,A_avg,color='black')
plt.plot(t,A_avg,'o',color='black',label='Promedio')
plt.legend()
plt.xlabel('Tiempo [min]')
plt.ylabel('Absorbancia')

'''
POST CAMBIO DE LÁMPARA
'''
# %%
plot_uv('31-10/tratamiento-uv_TiO2_fino-vidrio-1ppm')
plot_uv('05-11/tratamiento-uv_TiO2_fino-vidrio-1ppm')
# %%
''' 
Medimos con cuidado de que los frascos estén limpios y sin burbujas
'''
#plot_uv('19-11/tratamiento-uv_TiO2_grueso-metal-1ppm')
#plot_uv('19-11/tratamiento-uv_TiO2_fino-vidrio-1ppm')


plot_uv('31-10/tratamiento-uv_TiO2_fino-vidrio-1ppm', label='Tratamiento UV con TiO$_2$')
plot_uv('31-10/control-uv_TiO2_fino_vidrio', label='Tratamiento UV control')
#plot_uv('05-11/tratamiento-uv_TiO2_fino-vidrio-1ppm')
#plot_uv('05-11/control-uv_TiO2_fino_vidrio')
plt.savefig('Tratamiento UV estanco.pdf')

# %%
files = [
    '31-10/tratamiento-uv_TiO2_fino-vidrio-1ppm',
    '31-10/control-uv_TiO2_fino_vidrio',
    '05-11/tratamiento-uv_TiO2_fino-vidrio-1ppm',
    '05-11/control-uv_TiO2_fino_vidrio',
    '19-11/tratamiento-uv_TiO2_grueso-metal-1ppm'
]

concentrations = []
for file in files:
    t, A = np.loadtxt(os.path.join(c.ROOT, f'{file}.txt'), skiprows=1).T
    C = 1 - A/A[1] # Tomamos la segunda medición como inicial?
    last_concentration = C[-1]
    print(f'C_f {last_concentration:.2f} {file}')
    concentrations.append(last_concentration)

    
# Create a bar chart

plt.figure(figsize=(10, 6))
plt.bar(files, concentrations, color='skyblue')
plt.ylabel('DE [%]')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()

# %%
'''
Ploteamos el espectro de la lámpara uv y vemos que saturó apenas
'''
wavelength1, counts1 = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/led/1.4s-10.5V-1.txt'), skiprows=2).T
wavelength2, counts2 = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/led/1.4s-10.5V-2.txt'), skiprows=2).T
wavelength3, counts3 = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/led/1.4s-10.5V-3.txt'), skiprows=2).T

wavelength = np.mean(np.stack([wavelength2, wavelength3]), axis=0)
counts = np.mean(np.stack([counts2, counts3]), axis=0)
plt.plot(wavelength, counts / np.max(counts))

# %%
'''
Repetimos lo anterior para tiempo de exposición de 1.3s
'''
wavelength, counts = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/led/1.3s-10.5V.txt'), skiprows=2).T
plt.plot(wavelength, counts / np.max(counts), '.', label='Espectro del led UV', color='green', markersize=4)
plt.xlim(320,420)
plt.xlabel('$\lambda$ [nm]')
plt.ylabel('Intensidad')
plt.legend()

# %%
wavelength, counts = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/plasma/5s-16V-seco.txt'), skiprows=2).T
plt.plot(wavelength, counts / np.max(counts), '.', label='Espectro del reactor', color='cyan', markersize=4)
#plt.axvline(wavelength[np.argmax(counts)], label=f'$\lambda_{{max}} = {wavelength[np.argmax(counts)]}$', color='blue')
wavelength, counts = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/plasma/5s-16V-agua.txt'), skiprows=2).T
plt.xlim(290,410)
plt.plot(wavelength, counts / np.max(counts), '.', label='Espectro del reactor con agua', color='blue', markersize=4)
#plt.axvline(wavelength[np.argmax(counts)], label=f'$\lambda_{{max}} = {wavelength[np.argmax(counts)]}$', color='blue')
plt.xlabel('$\lambda$ [nm]')
plt.ylabel('Intensidad')
plt.legend()











# %%                               %%% INFORME %%%


# %%

plot_uv('31-10/tratamiento-uv_TiO2_fino-vidrio-1ppm', label='Tratamiento UV con TiO$_2$')
plot_uv('31-10/control-uv_TiO2_fino_vidrio', label='Tratamiento UV control')
plt.savefig('Tratamiento UV estanco.pdf')

# %%
wavelength, counts = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/led/1.3s-10.5V.txt'), skiprows=2).T
plt.plot(wavelength, counts / np.max(counts), '.', label='Espectro del led UV', color='green', markersize=4)
max_wavelength = wavelength[np.argmax(counts)]
plt.axvline(max_wavelength, label=f'$\lambda_{{max}}$ = {max_wavelength:.0f}')
plt.xlim(320,420)
plt.xlabel('$\lambda$ [nm]')
plt.ylabel('Intensidad')
plt.legend()
plt.savefig('Espectro led UV.pdf')

# %%
wavelength, counts = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/plasma/5s-16V-seco.txt'), skiprows=2).T
plt.plot(wavelength, counts / np.max(counts), '.', label='Espectro del reactor', color='cyan', markersize=4)
wavelength, counts = np.loadtxt(os.path.join(c.ROOT, '07-11/espectro-uv/plasma/5s-16V-agua.txt'), skiprows=2).T
plt.plot(wavelength, counts / np.max(counts), '.', label='Espectro del reactor con agua', color='blue', markersize=4)
plt.xlim(290,410)
plt.xlabel('$\lambda$ [nm]')
plt.ylabel('Intensidad')
plt.legend()
plt.savefig('Espectro reactor plasma.pdf')



# %%
