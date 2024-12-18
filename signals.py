import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy import integrate
from scipy.signal import find_peaks
import glob
import os
import uncertainties.unumpy as unp
import constants as c
from matplotlib import pyplot as plt

class SignalHandler:
    def __init__(self, file_name):
        self.tV, self.V, self.tI, self.I = self.get_signal(file_name)

    def get_signal(self, file_name):
        df = pd.read_csv(f'{c.ROOT}/{file_name}', index_col=0)
        t_volt, volt = [np.asarray(df[f'Tiempo CH{c.CH_VOLT}']), 
                        np.asarray(df[f'Voltaje CH{c.CH_VOLT}'])]
        t_istr, istr = [np.asarray(df[f'Tiempo CH{c.CH_ISTR}']), 
                1/c.R * np.asarray(df[f'Voltaje CH{c.CH_ISTR}'])]
        return t_volt, volt, t_istr, istr


class SignalReff(SignalHandler):
    def __init__(self, file):
        super().__init__(file)
        self.V_ac, self.V_ac_err, self.V_cc, self.V_cc_err, self.T, self.T_err = self.fit_sin()

    def fit_sin(self):
        def sin(x, A, T, p, B): return A*np.sin(2*np.pi/T*x + p) + B
        initialGuess = [7500, 1/8000, 0, 10000]
        popt, pcov = curve_fit(sin, self.tV, self.V, p0=initialGuess)
        perr = np.sqrt(np.diag(pcov))
        A, T, p, B = popt
        A_err, T_err, p_err, B_err = perr
        return 2*A, 2*A_err, B, B_err, T, T_err
    

class SignalZoom(SignalHandler):
    def __init__(self, file_zoom, T):
        super().__init__(file_zoom)
        self.t, self.I, self.V = self.filter(file_zoom)
        self.P_avg = self.get_power(T)
        self.I_avg = self.get_current()
        
    def filter(self, file_zoom):
        dt = 100
        threshold = 0.2
        dIdt = np.abs(np.gradient(self.I, self.tI)[dt:-dt])
        indices = find_peaks(dIdt/np.max(dIdt), height=threshold)[0] + dt
        i, f = indices[0], indices[-1]
        try:
            if len(indices) < 2:
                print(indices)
                raise ValueError("Not enough peaks found.") 
            t_filter, y = np.linspace([self.tI[i], np.mean(self.I[i-dt:i])], [self.tI[f], np.mean(self.I[f:f+dt])], f-i).T
            I_filter = self.I[i:f] - y
            V_filter = self.V[i:f]
            if np.any(np.isnan(I_filter)):
                print(i)
                print(f)
                print(self.I[i:f])
                print(y)
                raise ValueError("NAN.")
            return t_filter, I_filter, V_filter
        except Exception as e:
            print(f'El cálculo de la potencia en {file_zoom} falló con error {e}')
            plt.plot(self.tI[dt:-dt], np.abs(dIdt / np.max(dIdt)), label='Derivada')
            plt.plot(self.tI, self.I / np.max(self.I), label='Corriente')
            plt.axhline(0.25, label='Threshold')
            plt.legend()
    
    def get_power(self, T):
        return integrate.simpson(self.I * self.V, x=self.t) / T
    
    def get_current(self):
        return np.mean(self.I)
    

class Signals:
    def __init__(self, folder):
        self.folder = folder
        files = glob.glob(os.path.join(c.ROOT, self.folder, '*.csv'))
        self.signals_reff = self.get_reff_signals(files)
        self.T_avg =  self.get_avg_period()
        self.signals_zoom = self.get_zoom_signals(files)
        self.P_avg = self.get_avg_power()
        self.V_ac, self.V_cc = self.get_avg_voltage()
        self.I_avg = self.get_avg_current()

    def get_reff_signals(self, files):
        return [SignalReff(f'{self.folder}/{os.path.basename(file)}') for file in files if 'reff' in os.path.basename(file)]
        
    def get_zoom_signals(self, files):
        return [SignalZoom(f'{self.folder}/{os.path.basename(file)}', self.T_avg) for file in files if 'reff' not in os.path.basename(file)]
    
    def get_avg_period(self):
        return np.mean([s.T for s in self.signals_reff], axis=0)
    
    def get_avg_power(self):
        P_avg = np.mean([s.P_avg for s in self.signals_zoom], axis=0)
        P_std = np.std([s.P_avg for s in self.signals_zoom], axis=0)
        return unp.uarray(P_avg, P_std)

    def get_avg_voltage(self):
        V_ac = np.mean([s.V_ac for s in self.signals_reff], axis=0)
        V_ac_std = np.mean([s.V_ac_err for s in self.signals_reff], axis=0)
        V_cc = np.mean([s.V_cc for s in self.signals_reff], axis=0)
        V_cc_std = np.mean([s.V_cc_err for s in self.signals_reff], axis=0)
        return unp.uarray(V_ac, V_ac_std), unp.uarray(V_cc, V_cc_std)
    
    def get_avg_current(self):
        I_avg = np.mean([s.I_avg for s in self.signals_zoom], axis=0)
        I_std = np.std([s.I_avg for s in self.signals_zoom], axis=0) # Dudas, ¿asi se calculaba el error del promedio de un promedio? Además, estamos con std de numpy que está sesgado
        return unp.uarray(I_avg, I_std)
    
    def __repr__(self):
        return f'''
                    {self.folder}
                    I = {self.I_avg * 1000} mA
                    V_cc = {self.V_cc / 1000} kV
                    V_ac = {self.V_ac / 1000} kV
                    P = {self.P_avg} W'''
