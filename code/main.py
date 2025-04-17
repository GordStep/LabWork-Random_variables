import matplotlib.pyplot as plt
import numpy as np
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
    x = "{:.4f}".format(x)
    return f"{x}".replace('.', ',')





with open("data_n_2.txt") as file:
    content = file.read()
    data = []

    for number_str in content.split():
        el = float(number_str)
        data.append(el)

    file.close()

with open("theory_data.txt") as file:
    content = file.read()
    thdata = []

    for number_str in content.split():
        el = float(number_str)
        thdata.append(el)

    file.close()


print(thdata, len(thdata))
print(data, len(data))

sum_count = sum(data)
print(sum_count)

ydata = [el / sum_count for el in data]
xdata = [x for x in range(1, 55)]

print("sum ver: ", sum(ydata))
print(ydata)
print(len(xdata), len(ydata))

# Создание PDF
with PdfPages('../images/graph_1.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    mp_k:float = max(ydata)
    k = mp_k / np.sqrt(np.e)

    data_y = [i for i in range(0, 56, 5)]
    data_y.append(mp_k * 1000)
    data_y.append(k * 1000)

    # Вертикальные и горизонтальные линии
    for x in range(0, 56, 5):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y in data_y:
        ax.axhline(y=y / 1000, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Настройка основной оси X
    ax.set_xlabel("Номер ячейки", fontsize=14)
    # Настройка основной оси Y
    ax.set_ylabel("Вероятность попадания", fontsize=14)

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # Увеличили шаг
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.005))

    #mp_k = float(sci_notation_formatter_y(mp_k).replace(',', '.'))
    #k = float(sci_notation_formatter_y(k).replace(',', '.'))
    y = [i / 1000 for i in range(0, 56, 5)]
    y.append(mp_k)
    y.append(k)
    y = sorted(y)

    #y = [sci_notation_formatter_y(i) for i in y]

    ax.set_ylim(0, 0.055)
    ax.set_xlim(0, 55)



    plt.yticks(ticks=y, labels=y)

    plt.scatter(xdata, ydata)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))

    plt.plot(xdata, thdata, 'k--', linewidth=1)

    plt.tight_layout(pad=0.2)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)
    plt.show()


