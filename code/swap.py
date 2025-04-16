content = ""

file_name = "data_n_2"

with open(f"{file_name}.txt", 'r') as file:
    content = file.readline()
    file.close()

with open(f"{file_name}.txt", 'w') as file:
    content = content.replace(',', '.')
    file.write(content)

    print(content.count('.'))

    file.close()
