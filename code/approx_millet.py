import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from numpy import exp, pi, sqrt, e, sin, log
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
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


data = pd.read_csv('data_millet.csv')  # предполагается, что колонки 'x' и 'y'
x = data['x'].values
y = data['y_1'].values

# Для N = N_0/2
ysum = sum(y)
y = [el / ysum for el in y]

# Аппроксимация полиномом 10-й степени
coefficients = np.polyfit(x, y, deg=10)
polynomial = np.poly1d(coefficients)

# Вывод коэффициентов полинома
print("Коэффициенты полинома 10-й степени:")
print(coefficients)

# Генерация точек для гладкой кривой
x_smooth = np.linspace(min(x), max(x), 200)
y_smooth = polynomial(x_smooth)


# Рассчёт теоретической кривой
P_k = polynomial(27.5)
sigma_k = 1 / (0.053 * sqrt(2 * pi))
aver = 27.5

print("P_k:", P_k)
print("sigma:", sigma_k)

y_theory = P_k * exp(-(x_smooth - aver) ** 2 / (2 * sigma_k ** 2))


# Вычисления для флуктуаций
print("sum:", ysum)
print("aver:", ysum / 54)
p = polynomial(7)
print("P(7):", p)

n = sqrt((1 - p) / (ysum * p))
print("n_6:", n)
n = sqrt((1 - 0.053) / (ysum * 0.053))
print("n:", n)
print(max(y))

# Создание PDF
with PdfPages('../images/graph_1.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    mp_k = max(y)
    k = mp_k / np.sqrt(np.e)

    data_y = [i / 1000 for i in range(0, 56, 5)]
    data_y.append(mp_k)
    data_y.append(k)

    # Визуализация
    plt.plot(x_smooth, y_smooth, 'k--', label='Аппроксимация (10-я степень)', linewidth=1)
    plt.scatter(x, y, label='Исходные данные')
    plt.errorbar(x, y, xerr=1/1445, yerr=0, fmt='none', label='Исходные данные')
    plt.plot(x_smooth, y_theory, color='black', label="Теоретическая кривая")

    # Вертикальные и горизонтальные линии
    for x_lines in range(0, 56, 5):
        ax.axvline(x=x_lines, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y_lines in data_y:
        ax.axhline(y=y_lines, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$k$", fontsize=14)
    ax.set_ylabel(r"$P(k), \frac{1}{\text{мм}}$", fontsize=14)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.005))

    ax.set_ylim(0, 0.055)
    ax.set_xlim(0, 55)

    y_dots = [i / 1000 for i in range(0, 56, 5)]
    y_dots.append(mp_k)
    y_dots.append(k)
    y_dots = sorted(y_dots)
    plt.yticks(ticks=y_dots, labels=y_dots)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    plt.legend(loc='upper right', fontsize='medium', frameon=True)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()

# Для N = N_0
y = data['y_2'].values

ysum = sum(y)
y = [el / ysum for el in y]

# Аппроксимация полиномом 10-й степени
coefficients = np.polyfit(x, y, deg=10)
polynomial = np.poly1d(coefficients)

# Вывод коэффициентов полинома
print("Коэффициенты полинома 10-й степени:")
print(coefficients)

# Генерация точек для гладкой кривой
x_smooth = np.linspace(min(x), max(x), 200)
y_smooth = polynomial(x_smooth)


# Рассчёт теоретической кривой
P_k = polynomial(27.5)
sigma_k = 1 / (0.053 * sqrt(2 * pi))
aver = 27.5

print("P_k:", P_k)
print("sigma:", sigma_k)

y_theory = P_k * exp(-(x_smooth - aver) ** 2 / (2 * sigma_k ** 2))


# Вычисления для флуктуаций
print("sum:", ysum)
print("aver:", ysum / 54)
p = polynomial(7)
print("P(7):", p)

n = sqrt((1 - p) / (ysum * p))
print("n_6:", n)
n = sqrt((1 - 0.053) / (ysum * 0.053))
print("n:", n)
print(max(y))

# Создание PDF
with PdfPages('../images/graph_2.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    mp_k = max(y)
    k = mp_k / np.sqrt(np.e)

    data_y = [i / 1000 for i in range(0, 56, 5)]
    data_y.append(mp_k)
    data_y.append(k)

    # Визуализация
    plt.plot(x_smooth, y_smooth, 'k--', label='Аппроксимация (10-я степень)', linewidth=1)
    plt.scatter(x, y, label='Исходные данные')
    plt.errorbar(x, y, xerr=1/1445, yerr=0, fmt='none', label='Исходные данные')
    plt.plot(x_smooth, y_theory, color='black', label="Теоретическая кривая")

    # Вертикальные и горизонтальные линии
    for x_lines in range(0, 56, 5):
        ax.axvline(x=x_lines, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y_lines in data_y:
        ax.axhline(y=y_lines, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$k$", fontsize=14)
    ax.set_ylabel(r"$P(k), \frac{1}{\text{мм}}$", fontsize=14)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.005))

    ax.set_ylim(0, 0.055)
    ax.set_xlim(0, 55)

    y_dots = [i / 1000 for i in range(0, 56, 5)]
    y_dots.append(mp_k)
    y_dots.append(k)
    y_dots = sorted(y_dots)
    plt.yticks(ticks=y_dots, labels=y_dots)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    plt.legend(loc='upper right', fontsize='medium', frameon=True)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()