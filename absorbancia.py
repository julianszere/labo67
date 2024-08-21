# -*- coding: utf-8 -*-
#%%
"""
Created on Tue Apr 30 17:06:12 2024

@author: USER
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, sqrt
import tratamiento.constantes as c
params = {
    'figure.figsize': (11, 6),
    'axes.grid': True,
    'grid.linestyle': ':',
    'grid.linewidth': 1.5,
    'axes.axisbelow': True,
    'legend.fontsize': 20,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
}

plt.rcParams.update(params)

#%%

# cantAgua: Cantidad de agua pura [L]
# cantAguaAzul: Cantidad de agua con azul de metileno [L]
# polvo: Cantidad de azul de metileno [kg]
polvo = 10 # polvo de azul de metileno
def calcConcent(cantAgua, cantAguaAzul):
    return cantAguaAzul * polvo / (cantAguaAzul + cantAgua)


C_aguametileno, delta_aguametileno, C_metileno, delta_metileno, C_agua, delta_agua = symbols('C_aguametileno delta_aguametileno C_metileno delta_metileno C_agua delta_agua')

C = C_metileno * C_aguametileno / (C_aguametileno + C_agua)
result = sqrt((diff(C, C_agua) * delta_agua)**2 + (diff(C, C_aguametileno) * delta_aguametileno)**2 + (diff(C, C_metileno) * delta_metileno)**2)


# En mililitros, y miligramos
def delta_C(cantAgua, cantAguaMetileno):
    values = {
        C_aguametileno: cantAguaMetileno*1e-3,  
        delta_aguametileno: 1/2*1e-3, 
        C_metileno: polvo*1e-6, 
        delta_metileno: 0.01*1e-6,
        C_agua: cantAgua*1e-3, 
        delta_agua: 1/2*1e-3
    }
    return values

def eval_delta_C(cantAguas, cantAguaMetileno):
    delta_C_eval = []
    for cantAgua in cantAguas:
        delta = delta_C(cantAgua, cantAguaMetileno)
        delta_C_eval.append(result.subs(delta))
    return np.array(delta_C_eval)


#%%
long, A1, A2, A3, A4, A5 = np.loadtxt(c.ROOT + '/30-04/azul.txt', skiprows=1).T

plt.plot(long, A3, label='Frasco con agua', c='green')
plt.plot(long, A5, label='Frasco sin agua')
plt.plot(long, A1, label='Muestra 1', c='blue')
plt.plot(long, A2, label='Muestra 2', c='red')
plt.plot(long, A4, label='Muestra 2 sin referencia')

longMax1 = long[A1 == np.max(A1[200:-100])] 
plt.axvline(longMax1, c='blue')
longMax2 = long[A2 == np.max(A2[200:-100])] 
plt.axvline(longMax2, c='red')
print((longMax1 + longMax2) / 2)

long, A = np.loadtxt(c.ROOT + '/07-05/espectroAbsorbancia.txt', skiprows=1).T

longMax = long[A == np.max(A)][0] 
plt.axvline(longMax, label=f'$\lambda_{{max}} = {longMax}$')

plt.plot(long, A)

plt.xlabel(r'$\lambda$ [nm]', fontsize=20)
plt.ylabel(r'Absorbancia', fontsize=20)
plt.legend()
plt.xlim(250, 1000)
plt.ylim(0,1)

#%%

long, A = np.loadtxt(c.ROOT + '/07-05/espectroAbsorbancia.txt', skiprows=1).T

longMax = long[A == np.max(A)][0] 
plt.axvline(longMax, label=f'$\lambda_{{max}} = {longMax}$')

plt.plot(long, A)
plt.xlabel(r'$\lambda$ [nm]', fontsize=20)
plt.ylabel(r'Absorbancia', fontsize=20)
plt.legend()

#%%

'''
Tenemos una concentración de 10 mg / L de azul de metileno y la vamos diluyendo de a 10 ml
'''
agua, absorb = np.loadtxt(c.ROOT + '/07-05/concentracionAbsorbancia.txt', skiprows=1).T
concent = calcConcent(agua, 20)

plt.scatter(concent, absorb)
plt.xlabel('Concentración [mg/L]', fontsize=20)
plt.ylabel('Absorbancia', fontsize=20)

#%%
'''
Volvemos a medir concentración de 10 mg / L
'''

cantAgua, absorb = np.loadtxt(c.ROOT + '/10-05/concentracionAbsorbancia2.txt', skiprows=1).T
concent = calcConcent(cantAgua, 10)

plt.errorbar(concent, absorb, absorb*3/100, eval_delta_C(cantAgua, 20)*1e6, marker='o', label='Medición 10-05')

cantAgua, absorb = np.loadtxt(c.ROOT + '/07-05/concentracionAbsorbancia.txt', skiprows=1).T
concent = calcConcent(cantAgua)
plt.errorbar(concent, absorb, absorb*3/100, eval_delta_C(cantAgua, 10)*1e6, marker='o', label='Medición 07-05')


plt.legend()
plt.xlabel('Concentración [mg/L]', fontsize=20)
plt.ylabel('Absorbancia', fontsize=20)

#%%
'''
Medimos concentración en función del tiempo con el reactor a dos electrodos
'''

tiempo, absorb = np.loadtxt(c.ROOT + '/21-05/concentracionAbsorbancia2.txt', skiprows=1).T
plt.plot(tiempo, absorb)

# %%
