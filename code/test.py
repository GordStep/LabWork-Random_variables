import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from numpy import exp, pi, sqrt, e, sin
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

from main2 import P_theory

# Устанавливаем шрифт Times New Roman
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

with open("data.txt") as file:
    content = file.read()
    data = []

    for number_str in content.split():
        el = float(number_str)
        data.append(el)

    file.close()

ydata = []
xdata = []

for el in data:
    if xdata.count(el) == 0:
        xdata.append(el)
        ydata.append(data.count(el))

ydata = [i / 100 for i in ydata]
print("Data: ")
print(ydata,"len: ", len(ydata))
print(xdata,"len: ", len(xdata))

dsum = 0
v_y = []
for i in range(1, len(ydata) + 1):
    dsum += ydata[i - 1]
    v_y.append(dsum)
print(len(v_y), len(xdata))


# Создание PDF
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
    #ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

    #mp_k = float(sci_notation_formatter_y(mp_k).replace(',', '.'))
    #k = float(sci_notation_formatter_y(k).replace(',', '.'))
    y = [i / 100 for i in range(0, 101, 5)]
    y.append(0.11)
    y = sorted(y)

    #y = [sci_notation_formatter_y(i) for i in y]

    ax.set_ylim(0, 1.05)
    ax.set_xlim(510 - 51, 510 + 51)

    R_theory = np.linspace(510 - 50, 510 + 50, 500)
    #P_theory = 0.718673 * sin(0.0643134 * R_theory - 1.51821) + 0.532803
    #P_theory = 0.97689 / (1 + exp(-(0.273963 * R_theory-139.77149)))
    P_theory = 0.990454 / (1 + exp(-(0.307085 * R_theory - 156.73791))) + 0.01
    plt.plot(R_theory, P_theory, 'k--', linewidth=1)

    P_theory = [ (ydata[i] - ydata[i - 1]) / (xdata[i] - xdata[i - 1]) for i in range(1, len(ydata))]
    print("y: ", len(P_theory), "x: ", len(xdata))

    plt.yticks(ticks=y, labels=y)

    plt.scatter(xdata, v_y)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    #plt.plot([xdata[i] for i in range(0, len(xdata) - 1)], P_theory, 'k--', linewidth=1)

    plt.plot(xdata, v_y)
    plt.legend((r"$\frac{0,990454}{1 + \exp{-(0.307085 * x - 156.73791)}}$", 'Интегральная функция распределения'), loc='upper left', fontsize='medium', frameon=True)

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

with PdfPages('../images/graph_4.pdf') as pdf:

    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$R, Ом$", fontsize=14)
    ax.set_ylabel(r"$W(R), \frac{1}{Ом}$", fontsize=14)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг
    #ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))

    # mp_k = float(sci_notation_formatter_y(mp_k).replace(',', '.'))
    # k = float(sci_notation_formatter_y(k).replace(',', '.'))
    y = [i / 100 for i in range(0, 13)]
    y.append(0.11)
    y.append(0.11/ sqrt(e))
    y = sorted(y)

    # y = [sci_notation_formatter_y(i) for i in y]

    ax.set_ylim(0, 0.12)
    ax.set_xlim(510 - 51, 510 + 51)

    for i in range(1, len(ydata)):
        print("y: ", v_y[i], "-", v_y[i -1],  "x: ", xdata[i], "-", xdata[i - 1], "ydata: ", ydata[i], end=" ")
        print("delta: ", (v_y[i] - v_y[i - 1]) / (xdata[i] - xdata[i - 1]))

    P_theory = [(v_y[i] - v_y[i - 1]) / (xdata[i] - xdata[i - 1]) for i in range(1, len(ydata))]
    print("y: ", len(P_theory), "x: ", len(xdata))
    print(P_theory)
    plt.yticks(ticks=y, labels=y)

    plt.scatter(xdata, ydata, color='gray')
    #plt.scatter(xdata, ydata)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    #plt.scatter([xdata[i] for i in range(1, len(xdata))], P_theory)
    plt.plot([xdata[i] for i in range(1, len(xdata))], P_theory)

    R = 510
    m_ind = xdata.index(R)
    W_R = ydata[m_ind]
    print(W_R)
    y_R = W_R / sqrt(e)

    #sigma = 1 / (sqrt(2 * pi) * 0.11)

    y_1 = lambda x: 0.01125 * x - 5.638749999999999
    y_2 = lambda x: -0.01 * x + 5.21

    x_1 = lambda y : (y + 5.638749999999999) / 0.01125
    x_2 = lambda y : (y - 5.21) / (- 0.01)

    print("y_R", y_R)
    print("x_1: ", x_1(y_R), "x_2: ", x_2(y_R), x_2(y_R) - x_1(y_R))

    sigma = (x_2(y_R) - x_1(y_R)) / 2

    print("s / r: ", sigma / R)
    print("sigma: ", sigma)

    print(y_2(520))

    #R_theory = np.linspace(510 - 50, 510 + 50, 500)
    #P_theory = 1 / (sqrt(2 * pi) * sigma) * exp(-(R_theory - R) ** 2 / (2 * sigma ** 2))

    #plt.plot(R_theory, P_theory, 'k--', linewidth = 2)



    plt.plot([x_1(0), 510, x_2(0)], [0, 0.11, 0], color='gray')

    plt.legend(('Экспериментальные данные', 'Плотность вероятностей', 'Вспомогательные прямые', ''), loc='upper right', fontsize='medium', frameon=True)


    data_y = [i / 100 for i in range(0, 15)]
    data_y.append(0.11)
    data_y.append(0.11 / sqrt(e))

    # Вертикальные и горизонтальные линии
    for x in range(510 - 50, 510 + 51, 5):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y in data_y:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()

[print(sci_notation_formatter_y(el), end=" ") for el in v_y]
print()
[print(sci_notation_formatter_y(el), end=" ") for el in xdata]

with PdfPages('../images/graph_5.pdf') as pdf:

    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$R, Ом$", fontsize=14)
    ax.set_ylabel(r"$W(R), \frac{1}{Ом}$", fontsize=14)



    ax.set_ylim(0, 0.12)
    ax.set_xlim(510 - 51, 510 + 51)

    #plt.yticks(ticks=y, labels=y)



    # plt.scatter([xdata[i] for i in range(1, len(xdata))], P_theory)
    #plt.plot([xdata[i] for i in range(1, len(xdata))], P_theory)

    #plt.scatter(xdata, ydata)
    P_theory = [(v_y[i] - v_y[i - 1]) / (xdata[i] - xdata[i - 1]) for i in range(1, len(ydata))]

    plt.plot([xdata[i] for i in range(1, len(xdata))], P_theory)


    R_theory = np.linspace(510 - 50, 510 + 50, 500)
    P_theory = 1 / (sqrt(2 * pi) * sigma) * exp(-(R_theory - R) ** 2 / (2 * sigma ** 2))

    plt.plot(R_theory, P_theory, 'k--', linewidth=1)

    plt.legend(
        ('Эксперементальная плотность вероятностей', 'Нормельное распределение'),
        loc='upper right', fontsize='medium', frameon=True)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))

    data_y = [i / 100 for i in range(0, 13)]
    data_y.append(0.11)
    data_y.append(0.11 / sqrt(e))

    # Вертикальные и горизонтальные линии
    for x in range(510 - 50, 510 + 51, 5):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y in data_y:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # подписываем ось Y
    y = [i / 100 for i in range(0, 13)]
    y.append(0.11)
    y.append(0.11 / sqrt(e))
    y = sorted(y)

    plt.yticks(ticks=y, labels=y)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()



