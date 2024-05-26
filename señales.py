import numpy as np
import pandas as pd
from scipy.signal import find_peaks
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
        self.T = self.periodo()

    def periodo(self):
        freq = 8000
        self.picos, _ = find_peaks(self.V, distance=0.9 * 1/freq * 1/np.diff(self.tV)[0])
        return self.tV[self.picos[1]] - self.tV[self.picos[0]]


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
        self.V_max, self.V_std = self.voltaje()

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
        V_max = np.mean([np.max(señal.V) for señal in self.señalesZoom], axis=0)
        V_std = np.std([np.max(señal.V) for señal in self.señalesZoom], axis=0)
        return V_max, V_std
    