import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import uncertainties.unumpy as unp
from uncertainties import ufloat
import os
import glob
import constants as c
from signals import Signals
import re


class WaterTreatment(Signals):
    def __init__(self, folder, half_series=False, data_column=1, absorbance_error=c.A_ERR):
        self.file_name = self.get_file(folder)
        self.V_0, self.C_0 = self.get_parameters()
        self.t, self.A = self.get_data(half_series, data_column, absorbance_error)
        self.C = self.get_concentrations()
        self.DE = self.get_degradations()
        self.Y = self.get_efficiencies()

    def get_file(self, folder):
        file_list = glob.glob(os.path.join(c.ROOT, folder, '*.txt'))
        if file_list:
            Signals.__init__(self, folder)
            return file_list[0]
        else: 
            self.P_avg = 1
            return os.path.join(c.ROOT, f'{folder}.txt')

    def get_parameters(self):
        ppm_match = re.search(r'(\d+)(?=ppm)', self.file_name)
        ml_match = re.search(r'(\d+)(?=ml)', self.file_name)
        V_0 = ml_match.group(1) if ml_match else 200
        C_0 = ppm_match.group(1) if ppm_match else 10
        return ufloat(V_0, c.V_0_ERR), ufloat(C_0, c.C_0_ERR)
        
    def get_data(self, half_series, data_column, absorbance_error):
        t, A = np.loadtxt(Path(self.file_name).expanduser(), skiprows=1, usecols=(0,data_column)).T
        if half_series:
            A = A[np.logical_and(t % 2 == 0, t <= 60)]
            t = t[np.logical_and(t % 2 == 0, t <= 60)]
        avg = 3 if self.C_0.nominal_value == 1 else 1
        return unp.uarray(t, np.ones(len(t)) * c.T_ERR), unp.uarray(A, np.ones(len(A)) * absorbance_error / avg)
        
    def get_concentrations(self):
        F = ufloat(c.F, c.F_ERR)
        return self.A * F
    
    def get_degradations(self):
        return (1 - (self.A) / self.A[0]) * 100
    
    def get_efficiencies(self):
        return 6 * self.C_0 * self.DE[1:] * self.V_0 / (10**4 * self.P_avg * self.t[1:])
    
    def plot_absorbance(self, label=None, color=None):
        plt.errorbar(
            unp.nominal_values(self.t), 
            unp.nominal_values(self.A), 
            yerr=unp.std_devs(self.A), 
            xerr=unp.std_devs(self.t),
            fmt='d',                 
            elinewidth=1,  
            capsize=2,   
            capthick=1,      
            linestyle='None',   
            label=label,
            color=color
        )
        plt.xlabel('$t$ [min]')
        plt.ylabel('$A$')
    
    def plot_concentration(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.C), label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.C), unp.std_devs(self.C), unp.std_devs(self.t))
        plt.xlabel('$t$ [min]')
        plt.ylabel('$C$ [mg/L]')
    
    def plot_degradation(self, label=None):
        plt.errorbar(
            unp.nominal_values(self.t), 
            unp.nominal_values(self.DE), 
            yerr=unp.std_devs(self.DE), 
            xerr=unp.std_devs(self.t),
            fmt='d',                 
            elinewidth=1,  
            capsize=2,   
            capthick=1,      
            linestyle='None',   
            label=label  
        )
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('$DE$ [%]', fontsize=20)
        plt.tight_layout()
        if label:
            plt.legend()

    def plot_efficiency(self, label=None):
        plt.plot(unp.nominal_values(self.t[1:]), unp.nominal_values(self.Y), label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t[1:]), unp.nominal_values(self.Y), unp.std_devs(self.Y), unp.std_devs(self.t[1:]))
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('$Y$ [g/kWh]', fontsize=20)
    
    def __repr__(self):
        SignalesRepr = Signals.__repr__(self)
        return f'''
                    {SignalesRepr}
                    DE = {self.DE[-1]:.2f} %
                    Y = {self.Y[-1]:.2f} g/kWh
                '''
