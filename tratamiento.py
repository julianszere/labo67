import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy import integrate
from pathlib import Path
import os
import glob
import constantes as c
import uncertainties.unumpy as unp
from uncertainties import ufloat

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
        self.Vpp, self.Vpp_err, self.T, self.T_err = self.fit_sin()

    def fit_sin(self):
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
        self.t, self.I, self.V = self.filtro()
        self.P_avg = self.potencia(T)
        self.I_avg = self.corriente()

    def filtro(self):
        dt = 50
        # 0.005 np.max(self.I)/2
        #indices =  np.where(self.I > 0.005)[0]
        indices =  np.where(self.I/np.max(self.I) > 0.4)[0]
        i, f = indices[0] - dt, indices[-1] + dt
        t_filtro, y = np.linspace([self.tI[i], np.mean(self.I[i-dt:i])], [self.tI[f], np.mean(self.I[f:f+dt])], f-i).T
        I_filtro = self.I[i:f] - y
        V_filtro = self.V[i:f]
        return t_filtro, I_filtro, V_filtro
    
    def potencia(self, T):
        return integrate.simpson(self.I * self.V, x=self.t) / T
    
    def corriente(self):
        return np.mean(self.I)



class SeñalProm:
    def __init__(self, folder):
        self.señalesReff, self.señalesZoom = self.data(folder)
        self.P_avg = self.potencia()
        self.V_vpp = self.voltaje()
        self.I_avg = self.corriente()

    def data(self, folder):
        files = glob.glob(os.path.join(c.ROOT, folder, '*.csv'))
        señalesReff = [SeñalReff(file) for file in files if 'reff' in os.path.basename(file)]
        señalesZoom = [SeñalZoom(file, señalesReff[0].T) for file in files if 'reff' not in os.path.basename(file)]
        return señalesReff, señalesZoom
    
    def potencia(self):
        P_avg = np.mean([señal.P_avg for señal in self.señalesZoom], axis=0)
        P_std = np.std([señal.P_avg for señal in self.señalesZoom], axis=0)
        return unp.uarray(P_avg, P_std)

    def voltaje(self):
        V_vpp = np.mean([señal.Vpp for señal in self.señalesReff], axis=0)
        V_std = np.mean([señal.Vpp_err for señal in self.señalesReff], axis=0)
        return unp.uarray(V_vpp, V_std)
    
    def corriente(self):
        I_avg = np.mean([señal.I_avg for señal in self.señalesZoom], axis=0)
        I_std = np.std([señal.I_avg for señal in self.señalesZoom], axis=0) # Dudas, ¿asi se calculaba el error del promedio de un promedio? Además, estamos con std de numpy que está sesgado
        return unp.uarray(I_avg, I_std)
    
    def __repr__(self):
        return f'''
                    I = {self.I_avg * 1000} mA
                    V = {self.V_vpp / 1000} kV
                    P = {self.P_avg} W'''


class Concentracion:
    def __init__(self, file):
        self.t, self.A = self.txt(file)
        self.C = self.concentracion()
        self.DE = self.degradaciones()
        self.color = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))

    def txt(self, file):
        t, A = np.loadtxt(Path(file).expanduser(), skiprows=1).T
        return unp.uarray(t, np.ones(len(t)) * c.T_ERR), unp.uarray(A, np.ones(len(A)) * c.A_ERR)

    def concentracion(self):
        F = ufloat(c.F, c.F_ERR)
        return self.A * F
    
    def degradaciones(self):
        return (self.A[0] - self.A) / self.A[0] * 100
    
    def plot_concentracion(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.C), color=self.color, label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.C), unp.std_devs(self.C), unp.std_devs(self.t), color=self.color)
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('Concentración [mg/L]', fontsize=20)
    
    def plot_degradacion(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.DE), color=self.color, label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.DE), unp.std_devs(self.DE), unp.std_devs(self.t), color=self.color)
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('Porcentaje removido (%)', fontsize=20)
    
    def __repr__(self):
        return f'''DE = {self.DE[-1]:.2f} %'''

'''
    absor_ini: A_0, absorbancia inicial
    absor_fin: A_t, absorbancia final
    T: t, tiempo de tratamiento [min]
    pot: P, potencia [W]
    concent_ini: C_0, concentración inicial [mg/L]
    vol: V, volumen de la solución [ml]
'''
class Tratamiento(SeñalProm, Concentracion):
    def __init__(self, folder, V_0=200):
        SeñalProm.__init__(self, folder)
        Concentracion.__init__(self, glob.glob(os.path.join(c.ROOT, folder, '*.txt'))[0])
        self.V_0 = V_0
        self.Y = self.eficiencia()
        print(self.__repr__())
    
    def eficiencia(self):
        M_0 = ufloat(c.M_0, c.M_0_ERR)
        V_0 = ufloat(c.V_0, c.V_0_ERR)
        return 6 * M_0 / V_0 * self.DE[1:] * self.V_0 / (10**4 * self.P_avg * self.t[1:])
    
    def plot_eficiencia(self, label):
        plt.plot(unp.nominal_values(self.t[1:]), unp.nominal_values(self.Y), color=self.color, label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t[1:]), unp.nominal_values(self.Y), unp.std_devs(self.Y), unp.std_devs(self.t[1:]), color=self.color)
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('$Y$ [g/kWh]', fontsize=20)
        
    def __repr__(self):
        señalesRepr = SeñalProm.__repr__(self)
        concentRepr = Concentracion.__repr__(self)
        return f'''
                    {señalesRepr}
                    {concentRepr}
                    Y = {self.Y[-1]:.2f} g/kWh
                '''
