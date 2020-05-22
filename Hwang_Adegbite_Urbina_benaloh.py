import math
import random
import secrets
import timeit


# https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python:_Probably_correct_answers
def is_prime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False
    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2**s*d == n-1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(8):  # number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


def modular_exponentiation(a, b, n):
    if a == 0:
        return 0
    if b == 0:
        return 1
    if b == 1:
        return a
    if b % 2 == 0:
        t = modular_exponentiation(a, b/2, n)
        return t**2 % n
    else:
        t = modular_exponentiation(a, (b-1)/2, n)
        return a*t**2 % n


def gen(r):
    """
    Choose a block size r and two large primes p and q such that:
    • r divides (p − 1).
    • r and (p − 1)/r are relatively prime.
    • r and q − 1 are relatively prime.
    • n = pq.
    """
    p = secrets.randbelow(200)
    q = secrets.randbelow(200)
    p_found = False
    while not p_found:
        if is_prime(p):
            if (p-1) % r == 0:
                if math.gcd(r, (p-1)//r) == 1:
                    break
        p = secrets.randbelow(200)
    while not is_prime(q) or math.gcd(r, q-1) != 1:
        q = secrets.randbelow(200)

    n = p*q
    y = secrets.randbelow(n)
    b = (p - 1) * (q - 1) / r
    while y == 1 or y == p or y == q or modular_exponentiation(y, b, n) == 1:
        y = secrets.randbelow(n)
    public_key = y, r, n
    private_key = p, q
    return public_key, private_key


def enc(m: int, public_key):
    (y, r, n) = public_key
    u = secrets.randbelow(n)
    while math.gcd(u, n) != 1:
        u = secrets.randbelow(n)
    return (y**m)*(u**r) % n


def dec(c: int, private_key, public_key):
    (p, q) = private_key
    (y, r, n) = public_key
    for i in range(r):
        if modular_exponentiation((y**((p-1)*(q-1)-i))*c, (p-1)*(q-1)/r, n) == 1:
            return i
