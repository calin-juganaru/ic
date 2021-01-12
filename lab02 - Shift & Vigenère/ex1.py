from caesar import *
from format_funcs import *

def decrypt(ciphertext, common):
    plaintext = ''

    for i in range(0, 27):
        aux = caesar_dec_string(ciphertext, i)
        if aux.find(common) != -1:
            plaintext = aux
            break

    return plaintext


def main():
    ciphertexts = []
    with open("msg_ex1.txt", 'r') as f:
        for line in f:
            ciphertexts.append(line)
    print(ciphertexts)

    for c in ciphertexts:
        print(decrypt(c.strip(), 'YOU'))

    print(decrypt(ciphertexts[4].strip(), 'THE'))


if __name__ == "__main__":
    main()
