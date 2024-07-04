# -*- coding: utf-8 -*-
#%%
from tratamiento import Señal, SeñalReff, SeñalZoom, SeñalProm, Concentracion, Tratamiento
import tests
import constantes as c
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.optimize import curve_fit

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
teflon = SeñalProm('10-05/13.0V') 
plt.errorbar(teflon.V_max / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red', label='Teflón')

teflon = SeñalProm('10-05/12.5V') 
plt.errorbar(teflon.V_max / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')

teflon = SeñalProm('10-05/12.0V') 
plt.errorbar(teflon.V_max / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')

teflon = SeñalProm('10-05/11.5V') 
plt.errorbar(teflon.V_max / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')


acrili = SeñalProm('10-05/14.5V-e2') 
plt.errorbar(acrili.V_max / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue', label='Acrílico')

acrili = SeñalProm('10-05/14.0V-e2')
plt.errorbar(acrili.V_max / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')

acrili = SeñalProm('10-05/13.5V-e2')
plt.errorbar(acrili.V_max / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')

acrili = SeñalProm('10-05/13.0V-e2')
plt.errorbar(acrili.V_max / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')



plt.xlabel('Voltaje de entrada [kV]', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)
plt.legend()

#%%
'''
Ploteamos señales de referencia
'''
s = SeñalReff(f'{c.ROOT}/10-05/13.0V/reff-agua-vidrio_1e_electrodoCuatro 2024-05-10 13h 12m 39s.csv')

fig, ax1 = plt.subplots()

ax1.plot(s.tV * 1000, s.V / 1000, 'b', label='Voltaje')
ax1.set_xlabel('Tiempo [ms]', fontsize=20)
ax1.set_ylabel('Voltaje [kV]', fontsize=20)

ax2 = ax1.twinx()
ax2.plot(s.tI * 1000, s.I * 1000, 'r', label='Corriente')
ax2.set_ylabel('Corriente [mA]', fontsize=20)

ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.savefig('C:/Users/USER/Downloads/VoltajeYCorrienteVsTiempo.pdf')

#%%
'''
Y también mostramos el filtro
'''

sr = SeñalReff(f'{c.ROOT}/25-04/sin_ventana/aire_1e 2024-04-25 09h 48m 54s.csv')
sz = SeñalZoom(f'{c.ROOT}/25-04/con_ventana/aire_1e 2024-04-25 09h 46m 47s.csv', s.T)
tests.filtro(sz)

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
print(Tratamiento('04-06'))

#%%
'''
Vemos cómo se ven las corrientes porque una medición se tomó mal
'''
señales = SeñalProm('06-06').señalesZoom
for s in señales:
    plt.plot(s.t, s.I)
    
#%%
'''
Comparamos las mediciones con vidrio, las de teflón y las de acrílico
'''
teflon = Tratamiento('04-06/tratamiento-e4')
vidrio = Tratamiento('06-06/tratamiento-e5')
acrilico = Tratamiento('11-06/tratamiento-e3')
teflon.plot_eficiencia(label='Teflón')
vidrio.plot_eficiencia(label='Vidrio')
acrilico.plot_eficiencia(label='Acrílico')
plt.legend()

#%%

teflon_solo = Tratamiento('04-06/tratamiento-e4')
teflon_vidr = Tratamiento('18-06/tratamiento-e4-vidrio')
teflon_tio2 = Tratamiento('13-06/tratamiento-e4-TiO2')

teflon_solo.plot_concentracion(label='Teflón sin vidrio')
teflon_vidr.plot_concentracion(label='Teflón con vidrio')
teflon_tio2.plot_concentracion(label='Teflón con recubrimiento TiO$_2$')
plt.legend()

print(teflon_solo)
print(teflon_vidr)
print(teflon_tio2)

#%%
#teflon_solo = Tratamiento('04-06/tratamiento-e4')
#teflon_solo.plot2(label='Teflón sin vidrio')

teflon_solo_vidrio = Tratamiento('18-06/tratamiento-e4-vidrio', V_0=180)
teflon_solo_vidrio.plot_eficiencia(label='Teflón con vidrio')

teflon_tio2_original = Tratamiento('13-06/tratamiento-e4-TiO2')
teflon_tio2_original.plot_eficiencia(label='Teflón con recubrimiento TiO$_2$')

teflon_tio2_repetida = Tratamiento('25-06/tratamiento-e4-titanio')
teflon_tio2_repetida.plot_eficiencia(label='Teflón con TiO$_2$ repetida')

plt.legend()



# %%
concentracion, absorbancia = np.loadtxt(os.path.join(c.ROOT, '27-06/concentracion-absorbancia.txt'), skiprows=1).T
plt.scatter(absorbancia, concentracion, label='Mediciones', c='blue')

def lineal(x, m, b):
    return m*x + b

popt, pcov = curve_fit(lineal, absorbancia, concentracion)
perr = np.sqrt(np.diag(pcov))
m, b = popt
m_err, b_err = perr

plt.plot(absorbancia, lineal(absorbancia, m, b), label='Ajuste lineal', c='red')

plt.xlabel('Absorbancia', fontsize=20)
plt.ylabel('Concentración [mg/L]', fontsize=20)

