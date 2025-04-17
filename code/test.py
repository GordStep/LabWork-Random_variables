def test_func (x):
    x = "{:.3f}".format(x)
    return f"{x}".replace('.', ',')

print(test_func(0.01))