from numpy import sqrt

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
#print(ydata)
#print(len(xdata), len(ydata))

aver_ver = sum( ydata ) / len ( ydata )

Dx = sum( (ydata[i] - aver_ver )**2 for i in range( 1, len(ydata) - 1 ) ) / len( ydata )
sigma = sqrt(Dx)

print("aver: ", aver_ver)
print("Dx: ", Dx)
print("Sigma: ", sigma)


