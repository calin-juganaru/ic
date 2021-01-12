import random
import math

# =============================================================================

def int2bin(val):
    """
    Convert a 4-bit value to binary and return it as a list.
    """
    l = [0] * (4)

    l[0] = val & 0x1
    l[1] = (val & 0x2) >> 1
    l[2] = (val & 0x4) >> 2
    l[3] = (val & 0x8) >> 3

    return l

# =============================================================================

def generate(Q = 97, s = 19, N = 20):

    A = [random.randint(0, Q - 1) for i in range(N)]
    B = A

    for i in range(N):
        B[i] *= s
        B[i] += random.randint(1, 4)
        B[i] %= Q

    return A, B

# =============================================================================

def encrypt_bit(A, B, plain_bit, Q = 97):
    """
    Encrypt one bit using Learning with Errors (LWE).

        TODO 3: Compute "v"
            v = sum of the samples from vector B + floor(q/2) * plain_bit
            Don't forget modulo.

        TODO 4: Return cipher pair u, v
    """
    indices = random.sample(range(len(A)), 5)
    u = sum([A[i] for i in indices]) % Q
    v = (sum([B[i] for i in indices]) + (math.floor(Q / 2) * plain_bit)) % Q
    return (u, v)

# =============================================================================

def encrypt(A, B, number, q=97):
    """
    Encrypt a 4-bit number

    :param A: Public Key.
    :param B: Public Key.
    :param number: Number in interval [0, 15] that you want to encrypt.
    :param q: Modulus

    :return list with the cipher pairs (ui, vi).
    """
    # Convert number to binary; you will obtain a list with 4 bits
    bit_list = int2bin(number)

    # Using the function that you made before, encrypt each bit.
    u0, v0 = encrypt_bit(A, B, bit_list[0], q)
    u1, v1 = encrypt_bit(A, B, bit_list[1], q)
    u2, v2 = encrypt_bit(A, B, bit_list[2], q)
    u3, v3 = encrypt_bit(A, B, bit_list[3], q)

    return [(u0, v0), (u1, v1), (u2, v2), (u3, v3)]

# =============================================================================

def decrypt_bit(cipher_pair, s = 19, Q = 97):
    """
    Decrypt a bit using Learning with errors.
    """
    u = cipher_pair[0]
    v = cipher_pair[1]
    dec = (v - s * u) % Q
    return (u, v)

# =============================================================================

def decrypt(cipher, s=19, q=97):
    """
    Decrypt a 4-bit number from the cipher text pairs (ui, vi).

    :param cipher: Cipher text. List with 4 cipher pairs (u, v) corresponding to each encrypted bit
    :param s: Secret key
    :param q: Modulus

    :return plain: List with the 4 decrypted bits.
    """
    u1, v1 = cipher[0][0], cipher[0][1]
    u2, v2 = cipher[1][0], cipher[1][1]
    u3, v3 = cipher[2][0], cipher[2][1]
    u4, v4 = cipher[3][0], cipher[3][1]

    bit0 = decrypt_bit([u1, v1], s, q)
    bit1 = decrypt_bit([u2, v2], s, q)
    bit2 = decrypt_bit([u3, v3], s, q)
    bit3 = decrypt_bit([u4, v4], s, q)

    return [bit3, bit2, bit1, bit0]

# =============================================================================

def xor_then_decrypt_bit(cipher_pair1, cipher_pair2, s = 19, Q = 97):
    """
    Xor Cipher pairs and then decrypt a bit using Learning with errors.
    :return list with the cipher pairs (ui, vi).
    """

    u_1 = cipher_pair1[0]
    v_1 = cipher_pair1[1]

    u_2 = cipher_pair2[0]
    v_2 = cipher_pair2[1]

    dec = ((v_1 - s * u_1) + (v_2 - s * u_2)) % Q

    if dec > math.floor(Q / 2):
        return 1
    return 0

# =============================================================================

def xor_then_decrypt(cipher1, cipher2, s=19, q=97):
    """
    Bit wise xor the two cipher pairs and the decrypt 4-bit number result.

    :param cipher1: Cipher 1.
    :param cipher2: Cipher 2.
    :param s: Secret key
    :param q: Modulus

    :return plain: List with the 4 decrypted bits.
    """
    u1_1, v1_1 = cipher1[0][0], cipher1[0][1]
    u2_1, v2_1 = cipher1[1][0], cipher1[1][1]
    u3_1, v3_1 = cipher1[2][0], cipher1[2][1]
    u4_1, v4_1 = cipher1[3][0], cipher1[3][1]

    u1_2, v1_2 = cipher2[0][0], cipher2[0][1]
    u2_2, v2_2 = cipher2[1][0], cipher2[1][1]
    u3_2, v3_2 = cipher2[2][0], cipher2[2][1]
    u4_2, v4_2 = cipher2[3][0], cipher2[3][1]

    bit0 = xor_then_decrypt_bit([u1_1, v1_1], [u1_2, v1_2], s, q)
    bit1 = xor_then_decrypt_bit([u2_1, v2_1], [u2_2, v2_2], s, q)
    bit2 = xor_then_decrypt_bit([u3_1, v3_1], [u3_2, v3_2], s, q)
    bit3 = xor_then_decrypt_bit([u4_1, v4_1], [u4_2, v4_2], s, q)

    return [bit3, bit2, bit1, bit0]

# =============================================================================

if __name__ == "__main__":
    # Initialise Parameters
    q = 97
    s = 19
    nr_values = 20
    print("Initial parameters are:\n modulus={}\n secret_key={}\n nr_of_values={}\n".format(q, s, nr_values))

    # Integer in [0, 15] that you want to encrypt
    number_to_encrypt = 10
    print("You want to encrypt number " + str(number_to_encrypt))

    # Generate Step
    A, B = generate(q, s, nr_values)
    print("\nPublic Keys obtained:")
    print("A=", end="")
    print(A)
    print("B=", end="")
    print(B)

    # Encrypt Step
    cipher = encrypt(A, B, number_to_encrypt, q)
    print("\nCipher is ", end="")
    print(cipher)

    # Decrypt Step
    plain = decrypt(cipher, s, q)
    print("\nPlain value in binary is ", end="")
    print(plain)

    secretnumber1 = [(91, 56), (25, 52), (8, 3), (54, 7)]
    secretnumber2 = [(85, 2), (85, 5), (48, 50), (45, 3)]
    secretnumber3 = [(53, 89), (96, 95), (93, 91), (93, 41)]
    secretnumber4 = [(91, 57), (88, 49), (67, 83), (94, 63)]
    secretnumber5 = [(32, 71), (22, 47), (67, 36), (51, 50)]

    x = decrypt(secretnumber1, 17)
    print(x[0])
    print(x[1])
    print("")

    decrypt(secretnumber2, 17)
    decrypt(secretnumber3, 17)
    decrypt(secretnumber4, 17)
    decrypt(secretnumber5, 17)

    #result = xor_then_decrypt([1, 0, 0, 1], [1, 0, 1, 1])
    #print(result)

# =============================================================================