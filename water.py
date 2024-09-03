import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import uncertainties.unumpy as unp
from uncertainties import ufloat
import os
import glob
import constants as c
from signals import Signals


class Treatment(Signals):
    def __init__(self, folder):
        Signals.__init__(self, folder)
        self.t, self.A, self.V = self.get_data(folder)
        self.C = self.get_concentrations()
        self.DE = self.get_degradations()
        self.Y = self.get_efficiencies()

    def get_data(self, folder):
        file_name = glob.glob(os.path.join(c.ROOT, folder, '*.txt'))[0]
        data = np.loadtxt(Path(file_name).expanduser(), skiprows=1).T
        t = data[0]
        A = data[1]
        if data.shape[0] == 3:
            V = data[2]
        else:
            V = 200
        return unp.uarray(t, np.ones(len(t)) * c.T_ERR), unp.uarray(A, np.ones(len(A)) * c.A_ERR), unp.uarray(V,  c.V_0_ERR*1000)

    def get_concentrations(self):
        F = ufloat(c.F, c.F_ERR)
        return self.A * F
    
    def get_degradations(self):
        return (self.A[0] - self.A) / self.A[0] * 100
    
    def get_efficiencies(self):
        M_0 = ufloat(c.M_0, c.M_0_ERR)
        V_0 = ufloat(c.V_0, c.V_0_ERR)
        return 6 * M_0 / V_0 * self.DE[1:] * self.V / (10**4 * self.P_avg * self.t[1:])
    
    def __repr__(self):
        SignalesRepr = Signals.__repr__(self)
        return f'''
                    {SignalesRepr}
                    DE = {self.DE[-1]:.2f} %
                    Y = {self.Y[-1]:.2f} g/kWh
                '''
    
class Plot:
    def __init__(self, treatment, label=None, color=None):
        self.treatment = treatment
        self.label = label
        self.color = color or "#{:06x}".format(np.random.randint(0, 0xFFFFFF))

    def plot(self, x, y): 
        plt.plot(unp.nominal_values(x), unp.nominal_values(y), color=self.color, label=self.label, marker='o')
        plt.errorbar(unp.nominal_values(x), unp.nominal_values(y), unp.std_devs(y), unp.std_devs(x), color=self.color)

    def concentration(self):
        self.plot(self.treatment.t, self.treatment.C)
        plt.xlabel('$t$ [min]')
        plt.ylabel('$C$ [mg/L]')
    
    def degradation(self):
        self.plot(self.treatment.t, self.treatment.DE)
        plt.xlabel('$t$ [min]')
        plt.ylabel('$DE$ [%]')

    def efficiency(self):
        self.plot(self.treatment.t[1:], self.treatment.Y)
        plt.xlabel('$t$ [min]')
        plt.ylabel('$Y$ [g/kWh]')

    def plot_all(self, axs):
        axs[2].set_xlabel('$t$ [min]')

        axs[0].plot(unp.nominal_values(self.treatment.t), unp.nominal_values(self.treatment.C), color=self.color, label=self.label, marker='o')
        axs[0].errorbar(unp.nominal_values(self.treatment.t), unp.nominal_values(self.treatment.C), unp.std_devs(self.treatment.C), unp.std_devs(self.treatment.t), color=self.color)
        axs[0].set_ylabel('$C$ [mg/L]')   

        axs[1].plot(unp.nominal_values(self.treatment.t), unp.nominal_values(self.treatment.DE), color=self.color, label=self.label, marker='o')
        axs[1].errorbar(unp.nominal_values(self.treatment.t), unp.nominal_values(self.treatment.DE), unp.std_devs(self.treatment.DE), unp.std_devs(self.treatment.t), color=self.color)
        axs[1].set_ylabel('$DE$ [%]')   

        axs[2].plot(unp.nominal_values(self.treatment.t[1:]), unp.nominal_values(self.treatment.Y), color=self.color, label=self.label, marker='o')
        #axs[2].errorbar(unp.nominal_values(self.treatment.t[1:]), unp.nominal_values(self.treatment.Y), unp.std_devs(self.treatment.Y), unp.std_devs(self.treatment.t[1:]), color=self.color)
        axs[2].set_ylabel('$Y$ [g/kWh]')    
