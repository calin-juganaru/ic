import utils

C1 = "000100010001000000001100000000110001011100000111000010100000100100011101000001010001100100000101"
C2 = "02030F07100A061C060B1909"
key = "abcdefghijkl"

D1 = utils.strxor(utils.bin_2_str(C1), key)
print(D1)

D2 = utils.strxor(utils.hex_2_str(C2), key)
print(D2)