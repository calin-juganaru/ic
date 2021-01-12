from utils import *
from operator import itemgetter
import bisect
from Crypto.Cipher import DES

def get_index(a, x):
    """Locate the leftmost value exactly equal to x in list a"""
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

def des_enc(k, m):
    """
    Encrypt a message m with a key k using DES as follows:
    c = DES(k, m)

    Args:
        m should be a bytestring (i.e. a sequence of characters such as 'Hello' or '\x02\x04')
        k should be a bytestring of length exactly 8 bytes.

    Note that for DES the key is given as 8 bytes, where the last bit of
    each byte is just a parity bit, giving the actual key of 56 bits, as expected for DES.
    The parity bits are ignored.

    Return:
        The bytestring ciphertext c
    """
    d = DES.new(k, DES.MODE_ECB)
    c = d.encrypt(m)
    return c

def des_dec(k, c):
    """
    Decrypt a message c with a key k using DES as follows:
    m = DES(k, c)

    Args:
        c should be a bytestring (i.e. a sequence of characters such as 'Hello' or '\x02\x04')
        k should be a bytestring of length exactly 8 bytes.

    Note that for DES the key is given as 8 bytes, where the last bit of
    each byte is just a parity bit, giving the actual key of 56 bits, as expected for DES.
    The parity bits are ignored.

    Return:
        The bytestring plaintext m
    """
    d = DES.new(k, DES.MODE_ECB)
    m = d.decrypt(c)
    return m

###################################################################################################

def des2_enc(k1, k2, c):
    return des_enc(k1, des_enc(k2, c))

def des2_dec(k1, k2, c):
    return des_dec(k2, des_dec(k1, c))

###################################################################################################

def meet_in_the_middle(k1, m1, c1, k2, m2, c2):
    keys = []

    for i in range(0, 127):
        for j in range(0, 127):
            key = chr(i) + chr(j) + k2[2:]
            enc = des_enc(string_to_bytes(key), string_to_bytes(m1))
            keys.append((key, enc))

    keys = sorted(keys, key=itemgetter(1))
    tenc = [value for _,value in keys]

    for i in range(0, 127):
        for j in range(0, 127):
            key1 = chr(i) + chr(j) + k1[2:]
            m = des_dec(string_to_bytes(key1), bytes.fromhex(c1))

            index = get_index(tenc, m)
            if index != -1:
                key2 = keys[index][0]
                enc2 = des2_enc(string_to_bytes(key1), string_to_bytes(key2), string_to_bytes(m2))

                if enc2 == bytes.fromhex(c2):
                    print("(k1, k2) = ({}, {})".format(key1, key2))

###################################################################################################

def main():
    # Exercitiu pentru test des2_enc
    key1 = 'Smerenie'
    key2 = 'Dragoste'
    m1_given = 'Fericiti cei saraci cu duhul, ca'
    c1 = 'cda98e4b247612e5b088a803b4277710f106beccf3d020ffcc577ddd889e2f32'
    c2 = '54826ea0937a2c34d47f4595f3844445520c0995331e5d492f55abcf9d8dfadf'

    # TODO: implement des2_enc and des2_dec
    #m1 = des2_dec(key1, key2, c1)
    m1 = bytes_to_string(des2_dec(string_to_bytes(key1), string_to_bytes(key2), bytes.fromhex(c1)))
    m2 = bytes_to_string(des2_dec(string_to_bytes(key1), string_to_bytes(key2), bytes.fromhex(c2)))

    print('ciphertext: ' + c1)
    print('plaintext: {}\n'.format(m1))
    #print('plaintext in hexa: ' + bin_2_hex(m1))

    print('ciphertext: ' + c2)
    print('plaintext: {}\n'.format(m2))

    # TODO: run meet-in-the-middle attack for the following plaintext/ciphertext
    m1 = 'Pocainta'
    c1 = '9f98dbd6fe5f785d'
    m2 = 'Iertarea'
    c2 = '6e266642ef3069c2'

    # Note: you only need to search for the first 2 bytes of the each key:
    k1 = '??oIkvH5'
    k2 = '??GK4EoU'

    meet_in_the_middle(k1, m1, c1, k2, m2, c2)

if __name__ == "__main__":
    main()