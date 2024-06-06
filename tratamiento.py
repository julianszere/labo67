import numpy as np
from pathlib import Path
import os
import constantes as c
from señales import SeñalProm

class Concentracion:
    def __init__(self, file):
        self.t, self.A = self.txt(file)
        self.C = self.concentracion()

    def txt(self, file):
        return np.loadtxt(Path(file).expanduser(), skiprows=1).T
    
    def concentracion(self):
        return self.A * c.F

class Tratamiento:
    def __init__(self, folder):
        self.concent, self.señales = self.data(folder)
        self.DE, self.Y = self.eficiencia(self.concent.A[0], self.concent.A[-1], self.concent.t[-1], self.señales.P_avg)

    def data(self, folder):
        folder_path = f'{c.ROOT}/{folder}'
        for file in os.listdir(folder_path):
            if file.endswith('.txt') and 'tratamiento' in file:
                concent = Concentracion(os.path.join(folder_path, file))
        señales = SeñalProm(f'{folder}/potencia')
        return concent, señales
    
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
    
    def __str__(self):
        return f'''
                    P = {self.señales.P_avg} ± {self.señales.P_std}
                    I = {self.señales.I_avg} ± {self.señales.I_std}
                    V = {self.señales.V_vpp} ± {self.señales.V_std}
                    DE = {self.DE}
                    Y = {self.Y}
                '''
