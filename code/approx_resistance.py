import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from numpy import exp, pi, sqrt, e, sin, log
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from numpy.ma.extras import average
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline



# Устанавливаем шрифт CMU Serif
plt.rcParams['font.family'] = 'CMU Serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 12

def rounding(number: float, roundoff: int) -> str:
    return f"{number:.{roundoff}f}"

# Функция для форматирования чисел
def sci_notation_formatter(x, pos):
    coeff, exp = f"{x:.1e}".split('e')
    coeff = coeff.replace('.', ',')
    exp = int(exp)
    return f"{rounding(x,0)}".replace('.', ',')

# Функция для форматирования чисел
def sci_notation_formatter_y(x, pos = 3):
    coeff, exp = f"{x:.1e}".split('e')
    coeff = coeff.replace('.', ',')
    exp = int(exp)
    x = "{:.3f}".format(x)
    return f"{x}".replace('.', ',')

data = pd.read_csv('data_resistance.csv')  # предполагается, что колонки 'x' и 'y'
x = data['x'].values
y = data['y'].values
# Допустим, у вас есть массив из 50 точек: x_data и y_data
# Для примера сгенерируем случайные данные



def sigmoid(x, a, k, x0, c):
    return  a / (1 + np.exp(-k * (x - x0))) + c

# Начальные параметры: a=1, k=0.1, x0=510, c=0
# Амплитуда (a): 1.01, Крутизна (k): 0.12, Точка перегиба (x0): 510.33, Смещение (c): -0.01
popt, _ = curve_fit(sigmoid, x, y, p0=[1, 0.6, 510, -3])
a, k, x0, c = popt
print("k:", k)

x_smooth = np.linspace(510 - 50, 510+50, 300)
y_sigmoid = sigmoid(x_smooth,1, 0.23, 511, 0)


with PdfPages('../images/graph_3.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$R, Ом$", fontsize=14)
    ax.set_ylabel(r"$P(R), \frac{1}{Ом}$", fontsize=14)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг

    ax.set_ylim(0, 1.05)
    ax.set_xlim(510 - 51, 510 + 51)

    plt.scatter(x, y, label='Данные')
    plt.errorbar(x, y, xerr=1, yerr=0, fmt='none')
    plt.plot(x_smooth, y_sigmoid, color='red', label='Сигмоида')

    y_dots = [i / 100 for i in range(0, 110, 5)]
    y_dots = sorted(y_dots)
    plt.yticks(ticks=y_dots, labels=y_dots)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    plt.legend(("Сигмойда", 'Интегральная функция распределения'), loc='upper left', fontsize='medium', frameon=True)

    data_y = [i / 100 for i in range(0, 101, 5)]
    data_y.append(0.11)

    # Вертикальные и горизонтальные линии
    for x in range(510 - 50, 510 + 51, 5):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y in data_y:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()

data = pd.read_csv('data_resistance_count.csv')  # предполагается, что колонки 'x' и 'y'
x = data['r'].values
y = data['count'].values

y = [i / 100 for i in y]

R_theory = np.linspace(510 - 50, 510 + 50, 300)
#P_theory = [sigmoid(R_theory[i],1, 0.296, 511, 0) for i in range(0, 200)]
P_theory = [(y_sigmoid[i] - y_sigmoid[i - 1]) / (R_theory[i] - R_theory[i - 1]) for i in range(0, 300)]

Pmax = max(P_theory)
print("P_max:", Pmax)
for i in range(0, 300):
    if P_theory[i] == Pmax:
        print("R_m:", R_theory[i])

with PdfPages('../images/graph_4.pdf') as pdf:

    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$R, Ом$", fontsize=14)
    ax.set_ylabel(r"$W(R), \frac{1}{Ом}$", fontsize=14)
    # Точки теоретических данных
    #plt.scatter(x,y, color="gray")

    # Дифференцированная кривая
    plt.plot(R_theory, P_theory, label=r"$\text{Плотность вероятностей } W(R)$")

    # Теоретическая кривая
    sigma = 6.37
    W_theory =  1 / (sqrt(2 * pi) * sigma) * exp(-(R_theory - 511.2) ** 2 / (2 * sigma ** 2))
    plt.plot(R_theory, W_theory, linestyle='--', label=r"$\text{Нормальное распределение } W^{'}_T(R)$")

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг

    ax.set_ylim(0, 0.06)
    ax.set_xlim(510 - 49, 510 + 49)

    plt.legend(loc='upper right', fontsize='medium', frameon=True)

    y_dots = [i / 1000 for i in range(0, 71, 5)]
    y_dots.append(max(W_theory))
    y_dots.append(max(P_theory))
    y_dots.append(max(W_theory) / sqrt(e))
    plt.yticks(ticks=y_dots, labels=y_dots)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    data_y = [i / 1000 for i in range(0, 150, 5)]
    data_y.append(round(0.057 / sqrt(e), 3))
    data_y.append(max(P_theory))
    data_y.append(max(W_theory))
    data_y.append(max(W_theory) / sqrt(e))

    # Вертикальные и горизонтальные линии
    for x in range(510 - 50, 510 + 51, 5):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y in data_y:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()