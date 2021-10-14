from sympy.ntheory import isprime
from math import gcd
import time
import sys
import pyecm

def generate_p_q():
    
    prime_number = 82
    start_prime = 367
    tmp = start_prime
    pq = []
    for i in range(2):
        
        while len(str(tmp)) < prime_number:
            N = 4 * tmp + 2
            U = 0
            candidate = 0
            while True:
                candidate = (N + U) * tmp + 1
                if pow(2, int(candidate - 1), int(candidate)) == 1 and pow(2, int(N + U), int(candidate)) != 1:
                    tmp = candidate
                    break
                else:
                    U = U - 2
        pq.append(tmp)
        start_prime = start_prime + 2
        while len(list(pyecm.factors(start_prime, False, True, 8, 1))) != 1:
            start_prime = start_prime + 2
        tmp = start_prime
    p = pq[0]
    q = pq[1]
    print("\np = {}, длина = {}".format(p, len(str(p))))
    print("\nq = {}, длина = {}".format(q, len(str(q))))
    return p,q

def binarn(x, y, N):
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = binarn(x, y // 2, N)
    p = (p * p)% N
    if y % 2:
        p = (p * x)% N
    return p

def exgcd(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x
    
start_time = time.time()

p, q = generate_p_q()
        
N = p * q
print("\nN = ", N)

f = (p - 1)*(q - 1)
print("\nФ-ция Эйлера f =", f)

e = 0
i = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
while i < f:
    if isprime(i) and (gcd(i,p-1) == 1) and (gcd(i,q-1) == 1):
        e = i
        break
    else:
        i += 1
print("\nОткрытый ключ e =", e)

d = 0                       
d = exgcd(e, f)
d = d % f
print("\nЗакрытый ключ d =", d)

y = int(input("\nВведите сообщение для шифрования: "))
y = y % N
print("\nСообщение для шифрования: ", y)

x = binarn(y, e, N)
print("\nЗашифрованное сообщение x =", x)
print("\nРасшифрованное сообщение y1 =", binarn(x, d, N))

print('\nЗатраченное время =', time.time()-start_time)
