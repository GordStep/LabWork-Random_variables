import math
from numpy import exp, pi, sqrt

k = 54  # Количество уровней (54 ячейки)
p = 1 / 54

aver = 26.5
n = aver / p
print("n: ", n)
Dx = aver * (1 - p)
print("Dx: ", Dx, sqrt(Dx))

#Dx = sum( (k - aver)**2 for k in range(0, 54) ) / 54
#print("Dx: ", Dx)
sigma = sqrt(Dx) 
#sigma = 7.6

print("aver: ", aver)
print("Dx: ", Dx)
print("sigma: ", sigma)

print("P(k_sr): ", 1 / (sqrt(2 * pi) * 7.6))
print("sigma: ", 1 / (0.053 * sqrt(2 * pi)))

def W(x: float) -> float:
    r1 = 1 / (sqrt(2 * pi) * sigma)
    r2 = exp(-(x - aver)**2 / (2 * sigma**2))
    return r1 * r2

# Вычисляем вероятности для каждой ячейки (1 до 54)
probabilities = [W(i - 0.5) for i in range(1, 55)] # Центр ячейки


# Нормируем вероятности, чтобы сумма была равна 1
total_probability = sum(probabilities)
#normalized_probabilities = [p / total_probability for p in probabilities]

# Выводим результаты (можно сравнить с экспериментальными данными)
#for i, prob in enumerate(normalized_probabilities):
    #    print(f"Ячейка {i + 1}: {prob:.4f}")

def W_s(x: float) -> float:
    r1 = 0.053
    r2 = exp(-(x - aver)**2 / (2 * sigma**2))
    return r1 * r2

def W_d(k):
    return 1 / (sqrt(2 * pi) * sigma) * exp(-(k - aver)**2 / (2 * sigma**2))

file_name = "theory_data"
data = [W(x) for x in range(1, 55)]
data = probabilities
#x = 0
#while (x < 54):
    #data.append(W_d(x))
#    x += 1
    
#data = probabilities
print("sum data: ", sum(data))

with open(f"{file_name}.txt", 'w') as file:
    print(*data, file = file)

    file.close()
