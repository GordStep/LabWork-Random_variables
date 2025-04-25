import numpy as np
from scipy.interpolate import interp1d, CubicSpline
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = [475, 488, 496, 504, 510, 516, 529, 545]
ydata = [0.01, 0.03, 0.05, 0.14, 0.49, 0.82, 0.97, 1]

for i in range(0, 8):
    print('(' + str(xdata[i]) + ', ' + str(ydata[i]) + ')')
# Твои данные
x = np.array([475, 488, 496, 504, 510, 516, 529, 545])
y = np.array([0.01, 0.03, 0.05, 0.14, 0.49, 0.82, 0.97, 1]) # Пример значений

#e−39.2657+0.0739x
# Визуализация
x_new = np.linspace(x.min(), x.max(), 200)

# 1. Полиномиальная интерполяция
poly = np.polyfit(x, y, 6)  # 6 - степень полинома (кол-во точек - 1)
poly_func = np.poly1d(poly)

# 2. Кубический сплайн
cs = CubicSpline(x, y)

# 3. Линейная регрессия (для примера, хотя это может быть плохо для этих данных)
def linear_func(x, a, b):
    return a * x + b

popt, pcov = curve_fit(linear_func, x, y)
a, b = popt

y_new = np.linspace(0, 1, 200)
expi = np.exp(-39.2657 + 0.0739 * x_new)
#−0.0000x3+0.0251x2−12.7989x+2167.3808
cubiy = 1056.62924886 * y_new**3 - 1587.23184916 * y_new**2 + 605.96713305 * y_new + 469.93875185
sigma = 6.9
f_a = 0.5 * (1 + np.sign(x_new - 510) * np.sqrt(1 - np.exp( -0.63 * ((x_new - 510) / sigma)**2 )))

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'o', label='Исходные точки')
#plt.plot(x_new, expi, label='Експ')
plt.plot(x_new, poly_func(x_new), label='Полиномиальная интерполяция')
plt.plot(cubiy, y_new, label='Кубический сплайн')
plt.plot(x_new, f_a, label=f'аппрокс')


plt.xlabel('x')
plt.ylabel('y')
plt.title('Интерполяция и регрессия')
plt.legend()
plt.grid(True)
plt.show()
