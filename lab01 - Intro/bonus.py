import utils

with open ("ciphers.ciphertexts", "r") as file:
    data = file.readlines()

the = ' the '

for i in range(0, len(data) - 1):
    for j in range(i + 1, len(data)):
        x = utils.strxor(utils.hex_2_str(data[i].strip()), utils.hex_2_str(data[j].strip()))
        print(utils.strxor(x, the))

#print(utils.strxor(data[1], data[3]))
#print(utils.strxor(data[2], data[3]))