import matplotlib.pyplot as plt


def periodo(señalReff):
    t = señalReff.tV*1000
    V = señalReff.V*1000
    plt.plot(t, V)
    plt.axvline(t[señalReff.picos[0]])
    plt.axvline(t[señalReff.picos[1]])
    plt.xlabel('T [ms]', fontsize=20)
    plt.ylabel('V [kV]', fontsize=20)

def filtro(señalZoom):
    plt.plot(señalZoom.tI*1000, señalZoom.I*1000, c='red', label='Original')
    plt.plot(señalZoom.tf*1000, señalZoom.If*1000, c='blue', label='Filtrada')
    plt.xlabel('T [ms]', fontsize=20)
    plt.ylabel('I [mA]', fontsize=20)
    plt.legend()
