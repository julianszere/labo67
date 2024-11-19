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
    def __init__(self, folder, V=200):
        Signals.__init__(self, folder)
        self.file_name = glob.glob(os.path.join(c.ROOT, folder, '*.txt'))[0]
        self.V_0, self.C_0 = self.get_parameters()
        self.t, self.A = self.get_data()
        self.C = self.get_concentrations()
        self.DE = self.get_degradations()
        self.Y = self.get_efficiencies()

    def get_parameters(self):
        ppm_match = re.search(r'(\d+)(?=ppm)', self.file_name)
        ml_match = re.search(r'(\d+)(?=ml)', self.file_name)
        V_0 = ppm_match.group(1) if ppm_match else 200
        C_0 = ml_match.group(1) if ml_match else 10
        return unp.uarray(V_0, c.V_0_ERR), unp.uarray(C_0, c.C_0_ERR)
        
    def get_data(self):
        t, A = np.loadtxt(Path(self.file_name).expanduser(), skiprows=1, usecols=(0,1)).T
        avg = 3 if self.C_0 == 1 else 1
        return unp.uarray(t, np.ones(len(t)) * c.T_ERR), unp.uarray(A, np.ones(len(A)) * c.A_ERR / avg)
        
    def get_concentrations(self):
        F = ufloat(c.F, c.F_ERR)
        return self.A * F
    
    def get_degradations(self):
        return (self.A[0] - self.A) / self.A[0] * 100
    
    def get_efficiencies(self):
        return 6 * self.C_0 * self.DE[1:] * self.V_0 / (10**4 * self.P_avg * self.t[1:])
    
    def plot_concentration(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.C), label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.C), unp.std_devs(self.C), unp.std_devs(self.t))
        plt.xlabel('$t$ [min]')
        plt.ylabel('$C$ [mg/L]')
    
    def plot_degradation(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.DE), label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.DE), unp.std_devs(self.DE), unp.std_devs(self.t))
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('$DE$ (%)', fontsize=20)

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
