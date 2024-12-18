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
}

plt.rcParams.update(params)
#%%
'''
Calculo las potencias en aire y en agua-vidrio y las comparo para distinto número de electrodos
'''

aire_1e = Signals('30-04/electrodoUno') 
agua_1e = Signals('30-04/agua-vidrio_electrodoUno') 
plt.errorbar('Uno', unp.nominal_values(aire_1e.P_avg), unp.std_devs(aire_1e.P_avg), c='red', label='Mediciones en aire')
plt.errorbar('Uno', unp.nominal_values(agua_1e.P_avg), unp.std_devs(agua_1e.P_avg), c='blue', label='Mediciones en agua con vidrio')

aire_2e = Signals('30-04/electrodoDos') 
agua_2e = Signals('30-04/agua-vidrio_electrodoDos') 
plt.errorbar('Dos', unp.nominal_values(aire_2e.P_avg), unp.std_devs(aire_2e.P_avg), c='red')
plt.errorbar('Dos', unp.nominal_values(agua_2e.P_avg), unp.std_devs(agua_2e.P_avg), c='blue')

aire_3e = Signals('30-04/electrodoTres') 
agua_3e = Signals('30-04/agua-vidrio_electrodoTres') 
plt.errorbar('Tres', unp.nominal_values(aire_3e.P_avg), unp.std_devs(aire_3e.P_avg), c='red')
plt.errorbar('Tres', unp.nominal_values(agua_3e.P_avg), unp.std_devs(agua_3e.P_avg), c='blue')

plt.legend()
plt.xlabel('Número de electrodo', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)

#%%
'''
Analizamos la evolución temporal
'''

plt.plot([señal.P_avg for señal in aire_1e.signals_zoom], c='violet', label='Electrodo uno')
plt.plot([señal.P_avg for señal in agua_1e.signals_zoom][:5], c='violet')

plt.plot([señal.P_avg for señal in aire_2e.signals_zoom], c='purple', label='Electrodo dos')
plt.plot([señal.P_avg for señal in agua_2e.signals_zoom], c='purple')

plt.plot([señal.P_avg for señal in aire_3e.signals_zoom], c='pink', label='Electrodo tres')
plt.plot([señal.P_avg for señal in agua_3e.signals_zoom], c='pink')

plt.legend(loc='upper right')
plt.xlabel('Número de medición', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)
plt.xticks(range(0, 5))
plt.show()

#%%
'''
Comparamos la potencia del teflón y el acrílico ante distintos voltajes
'''
teflon = Signals('10-05/e4/13.0V') 
plt.errorbar(teflon.V_vpp / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red', label='Teflón')
teflon = Signals('10-05/e4/12.5V') 
plt.errorbar(teflon.V_vpp / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')
teflon = Signals('10-05/e4/12.0V') 
plt.errorbar(teflon.V_vpp / 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')
teflon = Signals('10-05/e4/11.5V') 
plt.errorbar(teflon.V_vpp/ 1000, teflon.P_avg, teflon.P_std, teflon.V_std / 1000, c='red')

acrili = Signals('10-05/e2/14.5V') 
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue', label='Acrílico')
acrili = Signals('10-05/e2/14.0V')
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')
acrili = Signals('10-05/e2/13.5V')
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')
acrili = Signals('10-05/e2/13.0V')
plt.errorbar(acrili.V_vpp / 1000, acrili.P_avg, acrili.P_std, acrili.V_std / 1000, c='blue')

plt.xlabel('Voltaje de entrada [kV]', fontsize=20)
plt.ylabel('Potencia [W]', fontsize=20)
plt.legend()

#%%
'''
Ploteamos voltaje y corriente de referencia (se podría hacer un inplot con el zoom)
'''
s = SignalHandler(f'10-05/e4/13.0V/reff-agua-vidrio_1e_electrodoCuatro 2024-05-10 13h 12m 39s.csv')

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
sr = SignalReff('25-04/sin_ventana/aire_1e 2024-04-25 09h 48m 54s.csv')
sz = SignalZoom('/25-04/con_ventana/aire_1e 2024-04-25 09h 46m 47s.csv', sr.T)
s = SignalHandler('/25-04/con_ventana/aire_1e 2024-04-25 09h 46m 47s.csv')

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
            señalReff = SignalReff(f'28-05/{medicion}/{os.path.basename(file)}')
            print(1/señalReff.T)
            
       
freq('30min')
freq('60min')
freq('90min')

#%%
'''
Evaluamos la potencia del tratamiento del 28/05
'''
s = Signals('28-05/30min')
print(s.P_avg)
s = Signals('28-05/60min')
print(s.P_avg)
s = Signals('28-05/90min')
print(s.P_avg)

#%%
def plot(folder, color, label=None):
    s = Signals(folder)
    plt.errorbar(unp.nominal_values(s.V_ac) / 1000, unp.nominal_values(s.P_avg), unp.std_devs(s.P_avg), c=color, label=label)
    plt.xlabel('$V$ [kV]')
    plt.ylabel('$P$ [W]')


plot('10-05/e2/13.0V', '#BD4277', 'Acrílico') # e2
plot('10-05/e2/13.5V', '#BD4277')
plot('10-05/e2/14.0V', '#BD4277')
plot('10-05/e2/14.5V', '#BD4277')

plot('10-05/e4/11.5V', '#4277BD', 'Teflón') # e4
plot('10-05/e4/12.0V', '#4277BD')
plot('10-05/e4/12.5V', '#4277BD')
plot('10-05/e4/13.0V', '#4277BD')

plot('28-05/vidrio/12.0', '#77BD42', 'Vidrio') # e5
plot('28-05/vidrio/12.5', '#77BD42')
plot('28-05/vidrio/13.0', '#77BD42')
plot('28-05/vidrio/13.5', '#77BD42')
plot('28-05/vidrio/14.0', '#77BD42')
plot('28-05/vidrio/14.5', '#77BD42')
plot('28-05/vidrio/15.0', '#77BD42')

plt.legend(loc='upper left')
plt.savefig('Potencias.pdf', dpi=300, bbox_inches='tight')

#%%
''' 
Mostramos los resultados del tratamiento de hoy
'''
WaterTreatment('04-06/tratamiento-e4')

#%%
'''
Vemos cómo se ven las corrientes porque una medición se tomó mal
'''
señales = Signals('06-06/tratamiento-e5').signals_zoom
for s in señales:
    plt.plot(s.t, s.I)
    
#%%
'''
Comparamos las mediciones con vidrio, las de teflón y las de acrílico
'''
teflon = WaterTreatment('04-06/tratamiento-e4')
teflon.color = '#4277BD'
acrilico = WaterTreatment('11-06/tratamiento-e3')
acrilico.color = '#BD4277'
vidrio = WaterTreatment('06-06/tratamiento-e5')
vidrio.color = '#77BD42'


teflon.plot_concentration('Teflón')
acrilico.plot_concentration('Acrílico')
vidrio.plot_concentration('Vidrio')

print(teflon)
print(acrilico)
print(vidrio)

plt.legend()

#%%
'''
Comparamos teflón sin vidrio, con vidrio y con vidrio y dióxido de titanio
'''
#teflon_solo = Tratamiento('04-06/tratamiento-e4')
teflon_vidr = WaterTreatment('18-06/tratamiento-e4-vidrio')
teflon_tio2 = WaterTreatment('13-06/tratamiento-e4-TiO2')
#teflon_tio2_repe = Tratamiento('25-06/tratamiento-e4-titanio')

teflon_vidr.color = '#4277BD'
teflon_vidr.plot_concentration('Sin $TiO_2$')
teflon_tio2.color = '#BD4277'
teflon_tio2.plot_concentration('Con $TiO_2$')
#teflon_tio2_repe.color = '#77BD42'
#teflon_tio2_repe.plot_concentration('Con $TiO_2$')
plt.legend()
plt.savefig('TiO2.pdf', dpi=300, bbox_inches='tight')
#plot_all([teflon_solo, teflon_vidr, teflon_tio2], ['Sin vidrio', 'Con vidrio', 'Vidrio y TiO$_2$'])

print(teflon_vidr)
print(teflon_tio2)
#%%
teflon_tio2_original = WaterTreatment('13-06/tratamiento-e4-TiO2')
teflon_tio2_original.plot_concentration(label='Teflón con recubrimiento TiO$_2$')

teflon_tio2_repetida = WaterTreatment('25-06/tratamiento-e4-titanio')
teflon_tio2_repetida.plot_concentration(label='Teflón con TiO$_2$ repetida')

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
s = SignalHandler('05-07/tratamiento-e4-e6-vidrio/zoom/e4-e6-vidrio 2024-07-05 09h 34m 13s.csv')
plt.plot(s.tV, s.V)
plt.plot(s.tI, s.I*100000)

# %%
path = c.ROOT + '/05-04/'
#sr = SeñalReff(path+'reff-tratamiento-e4 2024-06-04 17h 49m 35s.csv')
#sz = SeñalZoom(path+'tratamiento-e3 2024-06-11 17h 35m 52s.csv', sr.T)
s = SignalHandler(path+'aire_solo_1e 2024-04-05 09h 24m 18s.csv')
#Tratamiento('25-06/tratamiento-e4-titanio')

fig, ax1 = plt.subplots()
plt.plot(sr.tV * 1000, sr.V/1000-7)

# lns1 = ax1.plot(sr.tI * 1000, sr.I * 1000, color = '#4277BD', label='Corriente')
# ax1.set_xlabel('$t$ [ms]')
# ax1.set_ylabel('$I$ [mA]')
# ax1.tick_params(axis='y', labelcolor='#4277BD')

# ax2 = ax1.twinx()
# lns2 = ax2.plot(sr.tV * 1000, sr.V / 1000, color='#BD4277', label='Voltaje')
# ax2.set_ylabel('$V$ [kV]')
# ax2.tick_params(axis='y', labelcolor='#BD4277')
# plt.savefig('Filtro_1.pdf', dpi=300, bbox_inches='tight')

# lns1 = ax1.plot(s.tI * 1000, s.I * 1000, color = '#4277BD', label='Corriente')
# ax1.set_xlabel('$t$ [ms]')
# ax1.set_ylabel('$I$ [mA]')
# ax1.tick_params(axis='y', labelcolor='#4277BD')

# ax2 = ax1.twinx()
# lns2 = ax2.plot(s.tV * 1000, s.V / 1000, color='#BD4277', label='Voltaje')
# ax2.set_ylabel('$V$ [kV]')
# ax2.tick_params(axis='y', labelcolor='#BD4277')

#plt.savefig('Filtro_2.pdf', dpi=300, bbox_inches='tight')


# lns1 = ax1.plot(sz.t * 1000, sz.I * 1000, color='#77BD42', label='Corriente de streamers')
# lns2 = ax1.plot(s.tI * 1000, s.I * 1000, color = '#4277BD', label='Corriente')
# ax1.set_xlabel('$t$ [ms]')
# ax1.set_ylabel('$I$ [mA]')
# ax1.tick_params(axis='y', labelcolor='#4277BD')

# ax2 = ax1.twinx()
# lns3 = ax2.plot(s.tV * 1000, s.V / 1000, color='#BD4277', label='Voltaje')
# ax2.set_ylabel('$V$ [kV]')
# ax2.tick_params(axis='y', labelcolor='#BD4277')

# leg = lns1 + lns2 + lns3
# labs = [l.get_label() for l in leg]
# ax1.legend(leg, labs, loc='lower right')
# all_axes = fig.get_axes()
# for axis in all_axes:
#     legend = axis.get_legend()
#     if legend is not None:
#         legend.remove()
#         all_axes[-1].add_artist(legend)

# plt.savefig('Señal_Típicas.pdf', dpi=300, bbox_inches='tight')

# %%
teflones_tio2 = WaterTreatment('05-07/tratamiento-e4-e6-titanio')
teflones_tio2.plot_degradation(label='Dos teflones TiO2')
#teflones_tio2.plot_eficiencia(label='Dos teflones TiO2')

teflones_vidr = WaterTreatment('05-07/tratamiento-e4-e6-vidrio/zoom')
teflones_vidr.plot_degradation(label='Dos teflones')
#teflones_vidr.plot_eficiencia(label='Dos teflones')

teflon_vidr = WaterTreatment('18-06/tratamiento-e4-vidrio')
teflon_vidr.plot_degradation(label='Un teflón')
#teflon_vidr.plot_eficiencia(label='Un teflón')
plt.legend()

print(teflones_tio2)
print(teflones_vidr)

# %%
