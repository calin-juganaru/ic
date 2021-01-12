from utils import *
from ex1_weak_rng import *

import random
import math

def get_random_string(n): #generate random bit string
    bstr = bin(random.getrandbits(n)).lstrip('0b').zfill(n)
    return bstr

def monotest(R, N):
    S = 0
    for i in range(N):
        S += (ord(R[i]) - ord('0')) * 2 - 1
    S = abs(S) / math.sqrt(N)
    S = math.erfc(S / math.sqrt(2))
    return S

def main():
    wr = WeakRNG()
    wr.init_state()
    wr.set_rstate(1)

    N = 100
    R = ""

    for i in range(N):
        r = wr.get_prg_byte()
        if r == 0:
            r = random.randint(0, 1)
        R += chr(r + ord('0'))

    print(R)
    print(monotest(R, N))

    T = get_random_string(N)
    print(T)
    print(monotest(T, N))

if __name__ == "__main__":
    main()