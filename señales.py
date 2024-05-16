import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy import integrate
import constantes as c


class Señal:
    def __init__(self, data):
        self.tV, self.V, self.tI, self.I = data


class SeñalReff(Señal):
    def __init__(self, data):
        super().__init__(data)
        self.T = self.periodo()

    def periodo(self, test=False):
        self.picos, _ = find_peaks(self.V, distance=0.9*1/c.f * 1/np.diff(self.tV)[0])
        return self.tV[self.picos[1]] - self.tV[self.picos[0]]


class SeñalZoom(Señal):
    def __init__(self, data_zoom, data_reff):
        super().__init__(data_zoom)
        self.SeñalReff = SeñalReff(data_reff)
        self.tf, self.If, self.Vf = self.filtro()
        self.P_avg, self.I_avg = self.potencia(self.SeñalReff.T)

    def filtro(self):
        dt = 50
        i, f = np.where(self.I > 0.005)[0][0] - dt, np.where(self.I > 0.005)[0][-1] + dt
        t_filtro, y = np.linspace([self.tI[i], np.mean(self.I[i-dt:i])], [self.tI[f], np.mean(self.I[f:f+dt])], f-i).T
        I_filtro = self.I[i:f] - y
        V_filtro = self.V[i:f]
        return t_filtro, I_filtro, V_filtro
    
    def potencia(self, T):
        I_avg = np.mean(self.If)
        P_avg = integrate.simpson(self.If * self.Vf, x=self.tf) / T
        return P_avg, I_avg


class Test:
    def periodo(self, señalReff):
        plt.plot(señalReff.tV, señalReff.V)
        plt.axvline(señalReff.tV[señalReff.picos[0]])
        plt.axvline(señalReff.tV[señalReff.picos[1]])

    def filtro(self, señalZoom):
        plt.plot(señalZoom.tI*1000, señalZoom.I*1000, c='red', label='Original')
        plt.plot(señalZoom.tf*1000, señalZoom.If*1000, c='blue', label='Filtrada')
        plt.xlabel('T [s]', fontsize=20)
        plt.ylabel('I [mA]', fontsize=20)
        plt.legend()
