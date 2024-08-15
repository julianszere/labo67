# -*- coding: utf-8 -*-
#%%
from tratamiento import Señal, SeñalReff, SeñalZoom, SeñalProm, Concentracion, Tratamiento
#from helper import plot_all
import constantes as c
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import curve_fit
from scipy import integrate

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
}

plt.rcParams.update(params)
#%%
'''
Calculo las potencias en aire y en agua-vidrio y las comparo para distinto número de electrodos
'''

aire_1e = SeñalProm('30-04/electrodoUno') 
agua_1e = SeñalProm('30-04/agua-vidrio_electrodoUno') 
plt.errorbar('Uno', aire_1e.P_avg, aire_1e.P_std, c='red', label='Mediciones en aire')
plt.errorbar('Uno', agua_1e.P_avg, agua_1e.P_std, c='blue', label='Mediciones en agua con vidrio')

aire_2e = SeñalProm('30-04/electrodoDos') 
agua_2e = SeñalProm('30-04/agua-vidrio_electrodoDos') 
plt.errorbar('Dos', aire_2e.P_avg, aire_2e.P_std, c='red')
plt.errorbar('Dos', agua_2e.P_avg, agua_2e.P_std, c='blue')

aire_3e = SeñalProm('30-04/electrodoTres') 
agua_3e = SeñalProm('30-04/agua-vidrio_electrodoTres') 
plt.errorbar('Tres', aire_3e.P_avg, aire_3e.P_std, c='red')
plt.errorbar('Tres', agua_3e.P_avg, agua_3e.P_std, c='blue')

plt.legend()
plt.xlabel('Cantidad de electrodos', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)

#%%
'''
Analizamos la evolución temporal
'''

plt.plot([señal.P_avg for señal in aire_1e.señalesZoom], c='violet', label='Electrodo uno')
plt.plot([señal.P_avg for señal in agua_1e.señalesZoom][:5], c='violet')

plt.plot([señal.P_avg for señal in aire_2e.señalesZoom], c='purple', label='Electrodo dos')
plt.plot([señal.P_avg for señal in agua_2e.señalesZoom], c='purple')

plt.plot([señal.P_avg for señal in aire_3e.señalesZoom], c='pink', label='Electrodo tres')
plt.plot([señal.P_avg for señal in agua_3e.señalesZoom], c='pink')

plt.legend(loc='upper right')
plt.xlabel('Número de medición', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)
plt.xticks(range(0, 5))
plt.show()

#%%
'''
Comparamos la potencia del teflón y el acrílico ante distintos voltajes
'''
teflon = SeñalProm('10-05/e4/13.0V') 
plt.errorbar(teflon.V_vpp / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red', label='Teflón')
teflon = SeñalProm('10-05/e4/12.5V') 
plt.errorbar(teflon.V_vpp / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')
teflon = SeñalProm('10-05/e4/12.0V') 
plt.errorbar(teflon.V_vpp / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')
teflon = SeñalProm('10-05/e4/11.5V') 
plt.errorbar(teflon.V_vpp/ 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')

acrili = SeñalProm('10-05/e2/14.5V') 
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue', label='Acrílico')
acrili = SeñalProm('10-05/e2/14.0V')
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')
acrili = SeñalProm('10-05/e2/13.5V')
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')
acrili = SeñalProm('10-05/e2/13.0V')
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')

plt.xlabel('Voltaje de entrada [kV]', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)
plt.legend()

#%%
'''
Ploteamos voltaje y corriente de referencia (se podría hacer un inplot con el zoom)
'''
s = Señal(f'{c.ROOT}/10-05/e4/13.0V/reff-agua-vidrio_1e_electrodoCuatro 2024-05-10 13h 12m 39s.csv')

fig, ax1 = plt.subplots()

ax1.plot(s.tV * 1000, s.V / 1000, 'b', label='Voltaje')
ax1.set_xlabel('Tiempo [ms]', fontsize=20)
ax1.set_ylabel('Voltaje [kV]', fontsize=20)

ax2 = ax1.twinx()
ax2.plot(s.tI * 1000, s.I * 1000, 'r', label='Corriente')
ax2.set_ylabel('Corriente [mA]', fontsize=20)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

#%%
'''
Y también mostramos el filtro
(está roto por la funci{on find peaks)
'''
sr = SeñalReff(f'{c.ROOT}/25-04/sin_ventana/aire_1e 2024-04-25 09h 48m 54s.csv')
sz = SeñalZoom(f'{c.ROOT}/25-04/con_ventana/aire_1e 2024-04-25 09h 46m 47s.csv', sr.T)
s = Señal(f'{c.ROOT}/25-04/con_ventana/aire_1e 2024-04-25 09h 46m 47s.csv')

plt.plot(s.tI*1000, s.I*1000, c='blue', label='Filtrada')
plt.plot(sz.tI*1000, sz.I*1000, c='red', label='Original')
plt.xlabel('T [ms]', fontsize=20)
plt.ylabel('I [mA]', fontsize=20)
plt.legend()


plt.xlim(0.368, 0.378)

#%%
'''
Vemos si el período de la señal cambia durante el tratamiento del agua
'''
def freq(medicion):
    print()
    print(medicion)
    folder_path = f'{c.ROOT}/28-05/{medicion}'
    for file in os.listdir(folder_path):
        if file.endswith('.csv') and 'reff' in file:
            señalReff = SeñalReff(os.path.join(folder_path, file))
            print(1/señalReff.T)
            
       
freq('30min')
freq('60min')
freq('90min')

#%%
'''
Evaluamos la potencia del tratamiento del 28/05
'''
s = SeñalProm('28-05/30min')
print(f'{s.P_avg} +- {s.P_std}')
s = SeñalProm('28-05/60min')
print(f'{s.P_avg} +- {s.P_std}')
s = SeñalProm('28-05/90min')
print(f'{s.P_avg} +- {s.P_std}')

#%%
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(wspace=0.05)
def plot(folder, color, label=None):
    s = SeñalProm(folder)
    señales = s.señalesZoom
    #plt.errorbar(señales[2].t, señales[2].I, label=volt)
    #plt.errorbar(s.I_avg * 1000, s.P_avg, s.P_std, s.I_std * 1000, c=color, label=label)
    #plt.errorbar(s.V_vpp / 1000, s.P_avg, s.P_std, s.V_std / 1000, c=color, label=label)
        
    axs[0].errorbar(s.I_avg * 1000, s.P_avg, s.P_std, c=color, label=label)
    axs[0].set_xlabel('Corriente [mA]', fontsize=20)
    axs[0].set_ylabel('Potencia [W]', fontsize=20)
    axs[0].legend()
    
    axs[1].errorbar(s.V_vpp / 1000, s.P_avg, s.P_std, s.V_std / 1000, c=color, label=label)
    axs[1].set_xlabel('Voltaje [kV]', fontsize=20)
    axs[1].set_yticklabels([])


plot('10-05/e2/13.0V', 'red', 'Acrílico (e2)')
plot('10-05/e2/13.5V', 'red')
plot('10-05/e2/14.0V', 'red')
plot('10-05/e2/14.5V', 'red')

plot('10-05/e4/11.5V', 'green', 'Teflón (e4)')
plot('10-05/e4/12.0V', 'green')
plot('10-05/e4/12.5V', 'green')
plot('10-05/e4/13.0V', 'green')

plot('28-05/vidrio/12.0', 'blue', 'Vidrio (e5)')
plot('28-05/vidrio/12.5', 'blue')
plot('28-05/vidrio/13.0', 'blue')
plot('28-05/vidrio/13.5', 'blue')
plot('28-05/vidrio/14.0', 'blue')
plot('28-05/vidrio/14.5', 'blue')
plot('28-05/vidrio/15.0', 'blue')

#%%
''' 
Mostramos los resultados del tratamiento de hoy
'''
Tratamiento('04-06/tratamiento-e4')

#%%
'''
Vemos cómo se ven las corrientes porque una medición se tomó mal
'''
señales = SeñalProm('06-06/tratamiento-e5').señalesZoom
for s in señales:
    plt.plot(s.t, s.I)
    
#%%
'''
Comparamos las mediciones con vidrio, las de teflón y las de acrílico
'''
teflon = Tratamiento('04-06/tratamiento-e4')
teflon.color = '#4277BD'
acrilico = Tratamiento('11-06/tratamiento-e3')
acrilico.color = '#BD4277'
vidrio = Tratamiento('06-06/tratamiento-e5')
vidrio.color = '#77BD42'


teflon.plot_concentracion('Sistema de teflón')
acrilico.plot_concentracion('Sistema de acrílico')
vidrio.plot_concentracion('Sistema de vidrio')

plt.legend()
plt.savefig('Tratamiento_Dielectricos.pdf', dpi=300, bbox_inches='tight')

#%%
'''
Comparamos teflón sin vidrio, con vidrio y con vidrio y dióxido de titanio
'''
#teflon_solo = Tratamiento('04-06/tratamiento-e4')
teflon_vidr = Tratamiento('18-06/tratamiento-e4-vidrio')
teflon_tio2 = Tratamiento('13-06/tratamiento-e4-TiO2')
teflon_tio2_repe = Tratamiento('25-06/tratamiento-e4-titanio')

teflon_vidr.color = '#4277BD'
teflon_vidr.plot_concentracion('Sin $TiO_2$')
teflon_tio2.color = '#BD4277'
teflon_tio2.plot_concentracion('Con $TiO_2$')
teflon_tio2_repe.color = '#77BD42'
teflon_tio2_repe.plot_concentracion('Con $TiO_2$')
plt.legend()
plt.savefig('TiO2.pdf', dpi=300, bbox_inches='tight')
#plot_all([teflon_solo, teflon_vidr, teflon_tio2], ['Sin vidrio', 'Con vidrio', 'Vidrio y TiO$_2$'])


#%%
#teflon_solo = Tratamiento('04-06/tratamiento-e4')
#teflon_solo.plot2(label='Teflón sin vidrio')

#teflon_solo_vidrio = Tratamiento('18-06/tratamiento-e4-vidrio', V_0=180)
#teflon_solo_vidrio.plot_eficiencia(label='Teflón con vidrio')

teflon_tio2_original = Tratamiento('13-06/tratamiento-e4-TiO2')
teflon_tio2_original.plot_concentracion(label='Teflón con recubrimiento TiO$_2$')

teflon_tio2_repetida = Tratamiento('25-06/tratamiento-e4-titanio')
teflon_tio2_repetida.plot_concentracion(label='Teflón con TiO$_2$ repetida')

plt.legend()



# %%
'''
Hacemos un ajuste lineal de la concentración en función de la absorbancia
'''
absor = np.loadtxt(os.path.join(c.ROOT, '04-06/400-720 nm, 2 nm.txt'), skiprows=1).T
long = np.arange(400, 722, 2)
concent_azul, absorb_azul = np.loadtxt(os.path.join(c.ROOT, '27-06/concentracion-absorbancia.txt'), skiprows=1).T

def lineal(x, m, b):
    return m * x + b
popt, pcov = curve_fit(lineal, concent_azul, absorb_azul, sigma=absorb_azul*c.A_ERR, absolute_sigma=True)
perr = np.sqrt(np.diag(pcov))
m, b = popt
m_err, b_err = perr

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(15, 6))

ax1.axvline(662, color='red', label='$\lambda_{max}$')
ax1.errorbar(long, absor, np.abs(absor)*c.A_ERR, label='Espectro', c='#006bb3', fmt='o')
ax1.set_xlabel('$\lambda$ [nm]')
ax1.legend()
ax2.errorbar(concent_azul, absorb_azul, absorb_azul*c.A_ERR, label='Concentraciones', c='#006bb3', fmt='o')
ax2.plot(concent_azul, lineal(concent_azul, m, b), label='Ajuste lineal', c='red')
ax2.set_xlabel('$C$ [mg/L]')
ax2.legend()

ax1.set_ylabel('$A$', color='black')
plt.subplots_adjust(wspace=0.05)
plt.savefig('Absorbancia.pdf', dpi=300, bbox_inches='tight')
# %%
path = c.ROOT + '/05-07/tratamiento-e4-e6-vidrio/zoom/'
sr = SeñalReff(path+'reff-e4-e6-vidrio 2024-07-05 08h 49m 21s.csv')
sz = SeñalZoom(path+'e4-e6-vidrio 2024-07-05 08h 54m 32s.csv', sr.T)
plt.plot(sz.t, sz.I)
# %%
s = Señal(path+'e4-e6-vidrio 2024-07-05 08h 54m 32s.csv')
plt.plot(s.tV, s.V)
plt.plot(s.tI, s.I*100000)

# %%
SeñalProm('05-07/tratamiento-e4-e6-vidrio')
# %%
path = c.ROOT + '/05-07/tratamiento-e4-e6-vidrio/'
sr = SeñalReff(path+'reff-e4-e6-vidrio 2024-07-05 10h 11m 39s.csv')
sz = SeñalZoom(path+'e4-e6-vidrio 2024-07-05 10h 12m 55s.csv', sr.T)
s = Señal(path+'e4-e6-vidrio 2024-07-05 10h 12m 55s.csv')
#plt.plot(sr.tI*1000, sr.I*1000, color='red', label='Señal sin filtrar')
plt.plot(s.tI*1000, s.I*1000, color='red', label='Señal sin filtrar')
plt.plot(sz.t*1000, sz.I*1000, color='blue', label='Señal filtrada')

print(sz.P_avg)
print(integrate.simpson(s.I * s.V, x=s.tI) / sr.T)

plt.xlabel('$t$ [ms]')
plt.ylabel('$I$ [mA]')
plt.legend()
plt.savefig('Filtro_3.pdf', dpi=300, bbox_inches='tight')
# %%
teflones_tio2 = Tratamiento('05-07/tratamiento-e4-e6-titanio')
teflones_tio2.plot_degradacion(label='Dos teflones TiO2')
#teflones_tio2.plot_eficiencia(label='Dos teflones TiO2')

teflones_vidr = Tratamiento('05-07/tratamiento-e4-e6-vidrio/zoom')
teflones_vidr.plot_degradacion(label='Dos teflones')
#teflones_vidr.plot_eficiencia(label='Dos teflones')

teflon_vidr = Tratamiento('18-06/tratamiento-e4-vidrio')
teflon_vidr.plot_degradacion(label='Un teflón')
#teflon_vidr.plot_eficiencia(label='Un teflón')
plt.legend()
# %%
