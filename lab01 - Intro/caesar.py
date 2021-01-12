import utils

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def caesar_enc(letter, key):
    if letter < 'A' or letter > 'Z':
        print("Invalid letter")
        return
    else:
        return alphabet[(ord(letter) - ord('A') + key) % len(alphabet)]


def caesar_enc_string(plaintext, key):
    ciphertext = ''
    key = hash(key)
    for letter in plaintext:
        ciphertext = ciphertext + caesar_enc(letter, key)
    return ciphertext


def caesar_dec_string(plaintext, key):
    ciphertext = ''
    key = hash(key)
    for letter in plaintext:
        ciphertext = ciphertext + alphabet[(ord(letter) + ord('A') - key) % len(alphabet)]
    return ciphertext


def main():
    m = 'HELLOWORLD'
    key = 'TRALALA'
    c = caesar_enc_string(m, key)
    print(c)
    print(caesar_dec_string(c, key))

if __name__ == "__main__":
    main()