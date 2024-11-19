import os
from pathlib import Path as pth
from osciloscopio_tek import osciloscopio_tek as tek
from matplotlib import pyplot as plt
import time
from glob import glob
import pandas as pd
from signals import SignalHandler, SignalReff, SignalZoom, Signals
import constants as c




#%%-----------------------------Inicializar osciloscopio------------------------------------------ 

# Este string determina el intrumento que van a usar.
# Lo tienen que cambiar de acuerdo a lo que tengan conectado (installar NI VISA y 
#TEK VISA).
resource_name = 'USB0::0x0699::0x03B4::C021419::INSTR'


#inicializamos la comunicacion
def init():
    osci = tek(resource_name)
    osci.adquirir()
    print('Datos del osciloscopio:', osci.identificar())
    
    modo, prom, est, fren = osci.modo_adq()
    print('Modo:', modo, ', Promediado:', prom, ', Estado:', est, ', Frenar:', fren)
    
    # Modo de transmision: Binario
    osci.set_binario()
    return osci
#%% ---------------------------- Funciones -------------------------------------------------------
espera = 0 # Tiempo de espera entre mediciones en segundos.
folder = '14-11/pH_e4-150ml-1ppm'
path = f'{c.ROOT}/{folder}/'

def medir_all(osci):
    '''
    Mide todos los canales activos y devuelve un Dataframe de Pandas con los parametros y datos de cada uno. 
    '''
    estado_canales = osci.estado_ch()
    canales_activos = [int(canal+1) for canal in range(len(estado_canales)) if estado_canales[canal] =='1'] 
    osci.pausar()
    tabla = pd.DataFrame()
    for ch in canales_activos:
        print('midiendo canal {}'.format(ch))
        medir = osci.definir_medir(int(ch))
        tiempo, voltaje = medir()
        time.sleep(.1)
        params = osci.params_medir()
        time.sleep(.1)
        data = pd.DataFrame({'Tiempo CH{}'.format(int(ch)): tiempo, 'Voltaje CH{}'.format(int(ch)): voltaje})
        tabla_ch = pd.concat([params, data], axis=1)
        tabla = pd.concat([tabla, tabla_ch], axis=1)
    print('Todos los canales adquiridos correctamente')
    osci.adquirir()
    return tabla

def medir_guardar(osci, nombre=''):
    dataZoom = medir_all(osci)
    filename = path+nombre+' {}.csv'.format(time.strftime(
            "%Y-%m-%d %Hh %Mm %Ss", time.localtime()))
    dataZoom.to_csv(filename)
    time.sleep(espera)
    return filename

#%% --------------------------- Mediciones -----------------------------------
osci = init()
cant_med = 1000


#file_reff = medir_guardar(osci, 'reff-')
signal_reff = SignalReff(file_reff.replace(c.ROOT, ''))
print(f'''
          V_cc = {signal_reff.V_cc / 1000} kV
          V_ac = {signal_reff.V_ac / 1000} kV''')
input('Presione cuando haya hecho zoom')
for k in range(cant_med):
    print('Medicion ' + str(int(k+1)))
    file_zoom = medir_guardar(osci)
    
    signal_zoom = SignalZoom(file_zoom.replace(c.ROOT, ''), signal_reff.T)
    signal = Signals(folder)
    print(f'''
               I = {signal_zoom.I_avg * 1000} mA
               P = {signal_zoom.P_avg} W
               I_avg = {signal.I_avg * 1000} mA
               P_avg = {signal.P_avg} W''')

print('Fin de las mediciones. Cerrando comunicacion con el osciloscopio...')
osci.cerrar()
print('Comunicacion con el osciloscpio terminada.')    

#%%
folder = '05-11/tratamiento_e4e6-1ppm-150ml'
print(Signals(f'{folder}'))