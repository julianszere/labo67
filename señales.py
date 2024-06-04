import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy import integrate
from pathlib import Path
import os
import constantes as c


class Señal:
    def __init__(self, file):
        self.tV, self.V, self.tI, self.I = self.csv(file)

    def csv(self, file):
        df = pd.read_csv(Path(file).expanduser(), index_col=0)
        t_volt, volt = [np.asarray(df[f'Tiempo CH{c.CH_VOLT}']), 
                        np.asarray(df[f'Voltaje CH{c.CH_VOLT}'])]
        t_istr, istr = [np.asarray(df[f'Tiempo CH{c.CH_ISTR}']), 
                1/c.R * np.asarray(df[f'Voltaje CH{c.CH_ISTR}'])]
        return t_volt, volt, t_istr, istr


class SeñalReff(Señal):
    def __init__(self, file):
        super().__init__(file)
        self.Vpp, self.Vpp_err, self.T, self.T_err = self.fit()

    def fit(self):
        def sin(x, A, T, p, B): return A*np.sin(2*np.pi/T*x + p) + B
        initialGuess = [7500, 1/8000, 0, 10000]
        popt, pcov = curve_fit(sin, self.tV, self.V, p0=initialGuess)
        perr = np.sqrt(np.diag(pcov))
        A, T, p, B = popt
        A_err, T_err, p_err, B_err = perr
        return 2*A, 2*A_err, T, T_err
        

class SeñalZoom(Señal):
    def __init__(self, file_zoom, T):
        super().__init__(file_zoom)
        self.tf, self.If, self.Vf = self.filtro()
        self.P_avg = self.potencia(T)
        self.I_avg = self.corriente()

    def filtro(self):
        dt = 50
        indices =  np.where(self.I > 0.005)[0]
        i, f = indices[0] - dt, indices[-1] + dt
        t_filtro, y = np.linspace([self.tI[i], np.mean(self.I[i-dt:i])], [self.tI[f], np.mean(self.I[f:f+dt])], f-i).T
        I_filtro = self.I[i:f] - y
        V_filtro = self.V[i:f]
        return t_filtro, I_filtro, V_filtro
    
    def potencia(self, T):
        return integrate.simpson(self.If * self.Vf, x=self.tf) / T
    
    def corriente(self):
        return np.mean(self.If)


class SeñalProm:
    def __init__(self, folder):
        self.señalesReff, self.señalesZoom = self.señales(folder)
        self.P_avg, self.P_std = self.potencia()
        self.V_vpp, self.V_std = self.voltaje()
        self.I_avg, self.I_std = self.corriente()

    def señales(self, folder):
        señalesReff = []
        señalesZoom = []
        folder_path = f'{c.ROOT}/{folder}'
        for file in os.listdir(folder_path):
            if file.endswith('.csv') and 'reff' in file:
                señalReff = SeñalReff(os.path.join(folder_path, file))
                señalesReff.append(señalReff)
        for file in os.listdir(folder_path):
            if file.endswith('.csv') and 'reff' not in file:
                señalZoom = SeñalZoom(os.path.join(folder_path, file), señalesReff[0].T)
                señalesZoom.append(señalZoom)
        return señalesReff, señalesZoom
    
    def potencia(self):
        P_avg = np.mean([señal.P_avg for señal in self.señalesZoom], axis=0)
        P_std = np.std([señal.P_avg for señal in self.señalesZoom], axis=0)
        return P_avg, P_std

    def voltaje(self):
        V_vpp = np.mean([señal.Vpp for señal in self.señalesReff], axis=0)
        V_std = np.mean([señal.Vpp_err for señal in self.señalesReff], axis=0)
        return V_vpp, V_std
    
    def corriente(self):
        I_avg = np.mean([señal.I_avg for señal in self.señalesZoom], axis=0)
        I_std = np.std([señal.I_avg for señal in self.señalesZoom], axis=0) # Dudas, ¿asi se calculaba el error del promedio de un promedio? Además, estamos con std de numpy que está sesgado
        return I_avg, I_std

'''
absor_ini: A_0, absorbancia inicial
absor_fin: A_t, absorbancia final
T: t, tiempo de tratamiento [min]
pot: P, potencia [W]
concent_ini: C_0, concentración inicial [mg/L]
vol: V, volumen de la solución [ml]
'''
def eficiencia(absor_ini, absor_fin, T, pot, concent_ini=10, vol=200):
    DE = (absor_ini - absor_fin) / absor_ini * 100
    Y = 6 * concent_ini * DE * vol / (10**4 * pot * T)
    return DE, Y
    
#s = SeñalReff(f'{c.ROOT}/28-05/30min/reff-agua-e3e4 2024-05-28 16h 15m 39s.csv')