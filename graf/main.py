import matplotlib.pyplot as plt


with open("data.txt") as file:
    data = [int(line) for line in file.readlines()]

print(data)

sort_data = {el : data.count(el) for el in set(sorted(data))}
set_data = set(data)

sort_data = sorted(sort_data.items(), key=lambda x: x[0])
sort_data = dict(sort_data)
print(sort_data)

xdata = list(sort_data.keys())
ydata = list(sort_data.values())

plt.scatter(xdata, ydata)
plt.ylabel('count')
plt.xlabel('cell')
plt.show()
