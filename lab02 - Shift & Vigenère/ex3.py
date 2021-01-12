from caesar import *

freqs = {'A': 0.07048643054277828,
         'C': 0.01577161913523459,
         'B': 0.012074517019319227,
         'E': 0.13185372585096597,
         'D': 0.043393514259429625,
         'G': 0.01952621895124195,
         'F': 0.023867295308187673,
         'I': 0.06153403863845446,
         'H': 0.08655128794848206,
         'K': 0.007566697332106716,
         'J': 0.0017594296228150873,
         'M': 0.029657313707451703,
         'L': 0.04609015639374425,
         'O': 0.07679967801287949,
         'N': 0.060217341306347746,
         'Q': 0.0006382244710211592,
         'P': 0.014357175712971482,
         'S': 0.05892939282428703,
         'R': 0.05765294388224471,
         'U': 0.02749540018399264,
         'T': 0.09984475620975161,
         'W': 0.01892824287028519,
         'V': 0.011148804047838086,
         'Y': 0.023045078196872126,
         'X': 0.0005289788408463661,
         'Z': 0.00028173873045078196
         }

# computes the chi-distribution based on a dictionary of frequecies
# relative to the freqs frequencies dictionary


def compute_distribution(f):
    x2 = 0
    for l in freqs:
        x2 = x2 + (f[l] - freqs[l]) ** 2 / freqs[l]
    return x2

# splits a text in keylen cosets


def split_in_cosets(text, keylen):
    cosets = []
    for i in range(keylen):
        coset = []
        for j in range(i, len(text), keylen):
            coset.append(text[j])
        cosets.append(coset)
    return cosets

# merges the cosets to obtain the original text


def merge_cosets(cosets, coset_size):
    text = ''
    for j in range(coset_size):
        for i in range(len(cosets)):
            text = text + cosets[i][j]
    return text

# computes the frequency table for a coset shefited to left with a given shift


def get_freq_dict(coset, shift):
    d = {}

    # TODO 1 compute the frequency of the letters in the coset shifted to left
    # by the shift parameter
    for char in coset:
        aux = caesar_dec(char, shift)
        if aux in d:
            d[aux] = d[aux] + 1
        else:
            d[aux] = 0

    return d

# returns the shift computed for a coset


def find_correct_shift(coset):
    shift = 0

    # TODO 2 compute the shift which leads to the lowest chi-distribution
    minim = 0x3f3f3f3f

    for i in range(1, 27):
        frequency = get_freq_dict(coset, i)
        distribution = compute_distribution(frequency)

        if distribution < minim:
            minim = distribution
            shift = i

    return shift


def main():
    with open('msg_ex3.txt', 'r') as myfile:
        text = myfile.read().strip()

    dec_text = ''

    # TODO 3 decrypt the text

    for coset in split_in_cosets(text, 7):
        dec = caesar_dec_string(coset, find_correct_shift(coset))
        dec_text = dec_text + dec

    print(dec_text)


if __name__ == "__main__":
    main()
