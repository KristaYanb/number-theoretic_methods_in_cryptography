from sympy.ntheory import isprime, jacobi_symbol, legendre_symbol
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
                if (candidate % 4 == 3) and pow(2, int(candidate - 1), int(candidate)) == 1 and pow(2, int(N + U), int(candidate)) != 1:
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

def find_s(N):
    s = 2
    while (jacobi_symbol(s, N) != (-1)):
        s += 1
    return s

start_time = time.time()

#подготовка ключей

p, q = generate_p_q()
#p = 7
#q = 11

N = p * q
print("\nОткрытый ключ N = ", N)

s = find_s(N)
print("\nОткрытый ключ s = ", s)

k = (((p-1)*(q-1)//4)+1)//2
k = int(k)
print("\nЗакрытый ключ k = ", k)

#шифрование

M = int(input("Введите сообщение для шифрования: "))
M = M % N
print("Сообщение для шифрования: ", M)

jac_Mn = jacobi_symbol(M,N)
if jac_Mn == 1:
    c1 = 0
else:
    c1 = 1
print("\nc1 = ", c1)

M_shtrih = ((s**c1)*M)%N
print("\nM_shtrih = ", M_shtrih)
c2 = M_shtrih%2
print("\nc2 = ", c2)

c = (M_shtrih**2)%N
print("\nc = ", c)

#дешифрование

M_2_shtrih = binarn(c,k,N)
print("\nM_2_shtrih = ", M_2_shtrih)

if c2 == 1 and M_2_shtrih % 2 == 0:
    M_2_shtrih = -M_2_shtrih % N
if c2 == 0 and M_2_shtrih % 2 == 1:
    M_2_shtrih = -M_2_shtrih % N
    
M_decoded = (pow(s,-c1,N)*M_2_shtrih)%N

print("\nM_decoded = ", M_decoded)
#print("\nM_decoded_2 = ", M_decoded_2)

print('\nЗатраченное время =', time.time()-start_time)
