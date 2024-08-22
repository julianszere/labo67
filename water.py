import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import uncertainties.unumpy as unp
from uncertainties import ufloat
import os
import glob
import constants as c
from signals import Signals


class WaterTreatment(Signals):
    def __init__(self, folder, V=200):
        Signals.__init__(self, folder)
        self.V = V
        self.t, self.A = self.get_data(folder)
        self.C = self.get_concentrations()
        self.DE = self.get_degradations()
        self.Y = self.get_efficiencies()
        self.color = "#{:06x}".format(np.random.randint(0, 0xFFFFFF))

    def get_data(self, folder):
        file_name = glob.glob(os.path.join(c.ROOT, folder, '*.txt'))[0]
        t, A = np.loadtxt(Path(file_name).expanduser(), skiprows=1).T
        return unp.uarray(t, np.ones(len(t)) * c.T_ERR), unp.uarray(A, np.ones(len(A)) * c.A_ERR)

    def get_concentrations(self):
        F = ufloat(c.F, c.F_ERR)
        return self.A * F
    
    def get_degradations(self):
        return (self.A[0] - self.A) / self.A[0] * 100
    
    def get_efficiencies(self):
        M_0 = ufloat(c.M_0, c.M_0_ERR)
        V_0 = ufloat(c.V_0, c.V_0_ERR)
        return 6 * M_0 / V_0 * self.DE[1:] * self.V / (10**4 * self.P_avg * self.t[1:])
    
    def plot_concentration(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.C), color=self.color, label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.C), unp.std_devs(self.C), unp.std_devs(self.t), color=self.color)
        plt.xlabel('$t$ [min]')
        plt.ylabel('$C$ [mg/L]')
    
    def plot_degradation(self, label=None):
        plt.plot(unp.nominal_values(self.t), unp.nominal_values(self.DE), color=self.color, label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t), unp.nominal_values(self.DE), unp.std_devs(self.DE), unp.std_devs(self.t), color=self.color)
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('Porcentaje removido (%)', fontsize=20)

    def plot_efficiency(self, label=None):
        plt.plot(unp.nominal_values(self.t[1:]), unp.nominal_values(self.Y), color=self.color, label=label, marker='o')
        plt.errorbar(unp.nominal_values(self.t[1:]), unp.nominal_values(self.Y), unp.std_devs(self.Y), unp.std_devs(self.t[1:]), color=self.color)
        plt.xlabel('Tiempo [min]', fontsize=20)
        plt.ylabel('$Y$ [g/kWh]', fontsize=20)
    
    def __repr__(self):
        SignalesRepr = Signals.__repr__(self)
        return f'''
                    {SignalesRepr}
                    DE = {self.DE[-1]:.2f} %
                    Y = {self.Y[-1]:.2f} g/kWh
                '''
