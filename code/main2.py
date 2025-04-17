import matplotlib.pyplot as plt
import numpy as np
from numpy import exp, pi, sqrt, e
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

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
    return f"${rounding(x,0)}$".replace('.', ',')

# Функция для форматирования чисел
def sci_notation_formatter_y(x, pos = 3):
    coeff, exp = f"{x:.1e}".split('e')
    coeff = coeff.replace('.', ',')
    exp = int(exp)
    x = "{:.2f}".format(x)
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

print(ydata,"len: ", len(ydata))
print(xdata,"len: ", len(xdata))


aver = 510
n = 100
P_max = ydata[xdata.index(510)]
print(P_max)

#sigma = 1 / (P_max * sqrt(2 * pi))
p = 1 / ( (max(xdata) - min(ydata)) / 500 )
sigma = sqrt(n * p * ( 1 - p ))
print(sigma)

sigma *= (max(xdata) - min(ydata)) / 500

sigma = P_max / sqrt(e)
print("sigma: ", sigma)



def W(x: float) -> float:
    r1 = 1 / (sqrt(2 * pi) * sigma)
    r2 = exp(-(x - aver)**2 / (2 * sigma**2))
    return r1 * r2


sum_p = 0
th_data = []
for x in range(int(min(xdata)), int(max(xdata)) + 1):
    sum_p += W(x)
    th_data.append(W(x))

print("Sum: ", sum_p)
total_probability = sum(th_data)
normalized_probabilities = [p / total_probability for p in th_data]



# Создание PDF
with PdfPages('../images/graph_3.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    data_y = [i / 100 for i in range(0, 16)]
    data_y.append(P_max)

    # Вертикальные и горизонтальные линии
    for x in range(510 - 50, 510 + 51, 5):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y in data_y:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    ax.set_xlabel(r"$R, Ом$", fontsize=14)
    ax.set_ylabel(r"$P(R), \frac{1}{Ом}$", fontsize=14)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))

    #mp_k = float(sci_notation_formatter_y(mp_k).replace(',', '.'))
    #k = float(sci_notation_formatter_y(k).replace(',', '.'))
    y = [i / 100 for i in range(0, 15)]
    y.append(P_max)
    y = sorted(y)

    #y = [sci_notation_formatter_y(i) for i in y]

    ax.set_ylim(0, 0.14)
    ax.set_xlim(510 - 51, 510 + 51)



    plt.yticks(ticks=y, labels=y)

    plt.scatter(xdata, ydata)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    R_theory = np.linspace(510 - 50, 510 + 50, 500)
    P_theory = r1 = 1 / (sqrt(2 * pi) * sigma) * exp(-(R_theory - aver)**2 / (2 * sigma**2))

    plt.plot(R_theory, P_theory, 'k--', linewidth=1)
    plt.plot( [x for x in range(int(min(xdata)), int(max(xdata)) + 1)], normalized_probabilities, 'k--', linewidth=1)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()


