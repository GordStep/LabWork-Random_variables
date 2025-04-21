from numpy import sqrt


with open("data.txt") as file:
    content = file.read()
    data = []

    for number_str in content.split():
        el = float(number_str)
        data.append(el)

    file.close()

aver_r = sum(data) / len(data)
print("Среднее: ", aver_r)

sum_dx = 0
for r in data:
    sum_dx += (r - aver_r)**2
    print((r-aver_r)**2)
Dx = sum_dx / len(data)

print("Dx", Dx)

sigma = sqrt(Dx)
print("Сигма:", sigma)
