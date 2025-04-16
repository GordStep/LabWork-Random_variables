import matplotlib.pyplot as plt



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

plt.scatter(xdata, ydata)

print(ydata[27] * 100, ydata[28] * 100)

ydata = thdata
xdata.clear()
x = 0
for i in range(0, len(thdata)):
    x += 1    
    xdata.append(x)
print(len(xdata), len(ydata))



plt.plot(xdata, ydata, 'k--', linewidth=1)
plt.ylabel('probability')
plt.xlabel('cell')
plt.show()
