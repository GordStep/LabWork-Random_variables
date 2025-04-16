import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages

# Устанавливаем шрифт Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['legend.fontsize'] = 12

# Данные
data = {
    "R": [41108.5, 49403.3, 106391, 243721.2],
    "J": [0, 3.8, 10.1, 18.7],
    "dR": [9473.9, 11223, 15456.9, 22241.4],
    "dJ": [0.1, 0.1, 0.1, 0.1]
}

def rounding(number: float, roundoff: int) -> str:
    return f"{number:.{roundoff}f}"

# Функция для форматирования чисел
def sci_notation_formatter(x, pos):
    coeff, exp = f"{x:.1e}".split('e')
    coeff = coeff.replace('.', ',')
    exp = int(exp)
    return f"${rounding(x,2)}$".replace('.', ',')

# Функция для форматирования чисел
def sci_notation_formatter_y(x, pos):
    coeff, exp = f"{x:.1e}".split('e')
    coeff = coeff.replace('.', ',')
    exp = int(exp)
    return f"${rounding(x / 10**5, 1)}$".replace('.', ',')

# Создание PDF
with PdfPages('1.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(14, 9))  # Увеличили ширину

    # Основные элементы графика
    for x, y, dx, dy in zip(data["R"], data["J"], data["dR"], data["dJ"]):
        rect = Rectangle(
            (x - dx, y - dy), 2*dx, 2*dy,
            linewidth=0.5, edgecolor='gray', facecolor='lightgray', alpha=0.5
        )
        ax.add_patch(rect)
    
    ax.plot(data["R"], data["J"], 'o', color='black', markersize=2)

    # Теоретическая кривая
    R_theory = np.linspace(30000, 260000, 500)
    J_theory = 1 / 0.0988 * np.log(R_theory / 38103)
    ax.plot(R_theory, J_theory, 'k--', linewidth=1)

    # Вертикальные и горизонтальные линии
    for x, dx in zip(data["R"], data["dR"]):
        ax.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.axvline(x=x+dx, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.axvline(x=x-dx, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    for y, dy in zip(data["J"], data["dJ"]):
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.axhline(y=y+dy, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.axhline(y=y-dy, color='gray', linestyle='--', linewidth=0.5, alpha=0.3)

    # Настройка основной оси X (снизу)
    ax.set_xlabel(r"$J,\, 10^5 \times кг \cdot м^2$", fontsize=14)
    ax.set_ylabel(r"$R,\, см$", fontsize=14)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter_y))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(sci_notation_formatter))

    # Устанавливаем шаг для осей
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10000))  # Увеличили шаг
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.25))

    # Дополнительная ось X (сверху)
    R_values = data["R"]
    dR_values = data["dR"]
    xticks_top = []
    xticklabels_top = []
    for R, dR in zip(R_values, dR_values):
        xticks_top.extend([R - dR, R, R + dR])
        xticklabels_top.extend([
            f"{(R - dR):.1f}".replace('.', ','),
            f"{R:.1f}".replace('.', ','),
            f"{(R + dR):.1f}".replace('.', ',')
        ])

    ax_top = ax.secondary_xaxis('top')
    ax_top.set_xticks(xticks_top)
    labels = ax_top.set_xticklabels(xticklabels_top, rotation=60, fontsize=10)
    
    # Настраиваем выравнивание индивидуально
    for i, label in enumerate(labels):
        if i == 4:  # Центральные значения (R), каждое второе из трёх
            label.set_ha('center')  # Выравнивание слева
        else:  # Значения погрешностей (R - dR и R + dR)
            label.set_ha('left')  # Выравнивание справа


    # Дополнительная ось Y (справа)
    ax_right = ax.secondary_yaxis('right')
    ax_right.set_yticks(data["J"])
    ax_right.set_yticklabels(
        [f"{y:.1f}".replace('.', ',') for y in data["J"]],
        rotation=0, ha='left', fontsize=12  # Угол 0, шрифт 12
    )
    ax_right.tick_params(axis='y', pad=10)  # Отступ для меток

    # Сетка и пределы
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(30000, 260000)
    ax.set_ylim(-1, 20)

    plt.tight_layout(pad=3.0)  # Увеличенный отступ
    pdf.savefig(fig, bbox_inches='tight', dpi=300)

    plt.show()
    plt.close()

