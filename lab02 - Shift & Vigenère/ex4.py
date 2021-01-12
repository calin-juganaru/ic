from format_funcs import *

def main():

    # Plaintexts
    s1 = 'floare'
    s2 = 'albina'

    G = ''  # To find

    # http://www.lammertbies.nl/comm/info/crc-calculation.html

    x1 = str_2_hex(s1)
    x2 = str_2_hex(s2)

    crc1 = '8E31'  # CRC-16 of x1
    crc2 = '54BA'

    print("x1: " + x1)
    print("crc1: " + crc1 + '\n')

    print("x2: " + x2)
    print("crc2: " + crc2 + "\n")

    # Compute delta (xor) of x1 and x2:
    xd = hexxor(x1, x2)
    crcd = hexxor(crc1, crc2)

    print("xd: " + xd)
    print("crcd: " + crcd + "\n")

    final = hexxor(xd, str_2_hex(s1))

    print("Final: " + hex_2_str(final) + "\n")

if __name__ == "__main__":
    main()
