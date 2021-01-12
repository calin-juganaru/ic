#!/usr/bin/env python

import random
import sys

from Crypto.Cipher import AES
from math import ceil

BLOCK_SIZE = 16
IV = b'This is easy HW!'

###############################################################################

def blockify(text, block_size=BLOCK_SIZE):
    """
    Cuts the bytestream into equal sized blocks.

    Args:
      text should be a bytestring (i.e. b'text', bytes('text') or bytearray('text'))
      block_size should be a number

    Return:
      A list that contains bytestrings of maximum block_size bytes

    Example:
      [b'ex', b'am', b'pl', b'e'] = blockify(b'example', 2)
      [b'01000001', b'01000010'] = blockify(b'0100000101000010', 8)
    """

    nr_blocks = ceil(len(text) / block_size)
    return [bytearray(text[block_size * i : block_size * (i + 1)]) for i in range(nr_blocks)]

###############################################################################

def validate_padding(padded_text):
    """
    Verifies if the bytestream ends with a suffix of X times 'X' (eg. '333' or '22')

    Args:
      padded_text should be a bytestring

    Return:
      Boolean value True if the padded is correct, otherwise returns False
    """

    value = padded_text[-1]
    index = len(padded_text) - 2
    count = 1

    while padded_text[index] == value:
        index = index - 1
        count = count + 1
        if index < 0:
            break

    return value == count

###############################################################################

def pkcs7_pad(text, block_size=BLOCK_SIZE):
    """
    Appends padding (X times 'X') at the end of a text.
    X depends on the size of the text.
    All texts should be padded, no matter their size!

    Args:
      text should be a bytestring

    Return:
      The bytestring with padding
    """

    nr_blocks = ceil(len(text) / block_size)
    X = (nr_blocks * block_size) - len(text)

    text = bytearray(text)

    if X == 0:
        for i in range(0, block_size):
            text.append(block_size)
    else:
        for i in range(0, X):
            text.append(X)

    return bytes(text)

###############################################################################

def pkcs7_depad(text):
    """
    Removes the padding of a text (only if it's valid).
    Tip: use validate_padding

    Args:
      text should be a bytestring

    Return:
      The bytestring without the padding or None if invalid
    """

    text = bytearray(text)
    if validate_padding(text):
        last = text.pop()
        while text[-1] == last:
            text.pop()
            if len(text) == 0:
                break
        return bytes(text)

    return None

###############################################################################

def aes_dec_cbc(k, c, iv):
    """
    Decrypt a ciphertext c with a key k in CBC mode using AES as follows:
    m = AES(k, c)

    Args:
      c should be a bytestring (i.e. a sequence of characters such as 'Hello...' or '\x02\x04...')
      k should be a bytestring of length exactly 16 bytes.
      iv should be a bytestring of length exactly 16 bytes.

    Return:
      The bytestring message m
    """

    aes = AES.new(k, AES.MODE_CBC, iv)
    m = aes.decrypt(c)
    depad_m = pkcs7_depad(m)

    return depad_m

###############################################################################

def check_cbcpad(c, iv):
    """
    Oracle for checking if a given ciphertext has correct CBC-padding.
    That is, it checks that the last n bytes all have the value n.

    Args:
      c is the ciphertext to be checked.
      iv is the initialization vector for the ciphertext.
      Note: the key is supposed to be known just by the oracle.

    Return 1 if the pad is correct, 0 otherwise.
    """

    key = b'za best key ever'

    if aes_dec_cbc(key, c, iv) != None:
        return 1

    return 0

###############################################################################

def byte_xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

###############################################################################

if __name__ == "__main__":
    ctext = "918073498F88237C1DC7697ED381466719A2449EE48C83EABD5B944589ED66B77AC9FBD9EF98EEEDDD62F6B1B8F05A468E269F9C314C3ACBD8CC56D7C76AADE8484A1AE8FE0248465B9018D395D3846C36A4515B2277B1796F22B7F5B1FBE23EC1C342B9FD08F1A16F242A9AB1CD2DE51C32AC4F94FA1106562AE91A98B4480FDBFAA208E36678D7B5943C80DD0D78C755CC2C4D7408F14E4A32A3C4B61180084EAF0F8ECD5E08B3B9C5D6E952FF26E8A0499E1301D381C2B4C452FBEF5A85018F158949CC800E151AECCED07BC6C72EE084E00F38C64D989942423D959D953EA50FBA949B4F57D7A89EFFFE640620D626D6F531E0C48FAFC3CEF6C3BC4A98963579BACC3BD94AED62BF5318AB9453C7BAA5AC912183F374643DC7A5DFE3DBFCD9C6B61FD5FDF7FF91E421E9E6D9F633"
    ciphertext = bytes.fromhex(ctext)
    blocks = blockify(ciphertext, BLOCK_SIZE)
    msg = ""

    for block in blocks:
        r = bytearray(b'0' * 16)

        for i in range(0, 16):
            X = bytearray(b'0' * (15 - i))
            for k in range(0, i + 1):
                X.append(i + 1)

            char = -1

            for j in range(1, 256):
                r[15 - i] = j

                aux = byte_xor(IV, r)
                aux = byte_xor(aux, X)

                if check_cbcpad(block, aux):
                    if char == -1:
                        char = j
                    else:
                        IV_test = bytearray(IV)
                        IV_test[-2] = (IV_test[-2] + 123) % 256
                        aux2 = byte_xor(IV_test, r)
                        aux2 = byte_xor(aux2, X)
                        if check_cbcpad(block, aux2):
                            char = j

            r[15 - i] = char

        IV = block
        msg += r.decode()

    print(msg)

###############################################################################