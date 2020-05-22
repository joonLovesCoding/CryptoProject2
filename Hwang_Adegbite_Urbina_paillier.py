import secrets
import math
    
def gcd(a,b):
    while b > 0:
        a,b = b, a % b
    return a

def lcm(a,b):
        return (a*b)//gcd(a,b)

def invMod(a,m):
    a = math.fmod(a, m); 
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1

def mul_mod(a,b,n):
    res = 0
    a = math.fmod(a,n)
  
    while (b): 
        if (b & 1): 
            res = (res + a) %n
        a = (2*a) %n
        b >>= 1
    return res

def pow_mod(x,y,p):
    res = 1
    x = math.fmod(x,p)  
  
    while (y > 0):
        if (y & 1):
            res = math.fmod(res * x,p) 
        y = y >> 1
        x = math.fmod(x*x,p) 
    return res

def prime(n) : 
    if n <= 1: 
        return False
    if n <= 3: 
        return True

    if n % 2 == 0 or n % 3 == 0: 
        return False
  
    i = 5
    while(i * i <= n) : 
        if (n % i == 0 or n % (i + 2) == 0) : 
            return False
        i = i + 6
  
    return True

def gen():
    truth = False
    while truth == False:
        p = secrets.randbelow(10)
        q = secrets.randbelow(10)
        
        while prime(p) == False or prime(q) == False or p == q:
            p = secrets.randbelow(10)
            q = secrets.randbelow(10)
        
        n = p*q
        
        xi = lcm(p-1,q-1)

        g = secrets.randbelow(n*n)
        l = (pow_mod(g,xi,n*n) - 1)//n

        while gcd(g,n*n)!= 1 or l < 1:
            g = secrets.randbelow(n*n)
            l = (pow_mod(g,xi,n*n) - 1)//n
            
        pk = [n, g]
        sk = [(p,q), xi]
        truth = test(pk,sk)
        if truth != False:
            #print(f"Paillier:\nn:{n}\ng:{g}\np:{p}\nq:{q}\nxi:{xi}")
            return pk, sk

def L(g, xi, pubKey,):
    return (pow_mod(g,xi,pubKey[0]*pubKey[0]) - 1)//pubKey[0]

def enc(m, pubKey):
    while m > pubKey[0]:
        m = int(input("Try again. m (m < n): "))

    r = secrets.randbelow(pubKey[0] - 1)
    while (gcd(r,pubKey[0]) != 1):
        r = secrets.randbelow(pubKey[0])

    c1 = pubKey[1]**m
    c2 = r**pubKey[0]
    return mul_mod(c1,c2,pubKey[0]*pubKey[0])

def dec(c, prKey, pubKey):
    L1 = L(c,prKey[1], pubKey)
    L2 = L(pubKey[1],prKey[1],pubKey)
    return mul_mod(L1, invMod(L2, pubKey[0]), pubKey[0])

def test(pk,sk):
    r = secrets.randbelow(pk[0])
    
    c1 = enc(r, pk)
    c2 = enc(r, pk)
    c3 = enc(0, pk)
    c4 = enc(0, pk)
    m = r + r
    if dec(c1 * c2 * c3 * c4, sk, pk) != m:
        return False
    else:
        return True
