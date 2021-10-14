import time
import pyecm
from sympy import factorint
from sympy.ntheory import totient, isprime
from random import randint

def generate_q(prime_number, start_prime):
    tmp = start_prime
    q = 0
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
    q = tmp
    #print("\nq = {}, длина = {}".format(q, len(str(q))))
    return q

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

def find_p():
    a = 5
    q = generate_q(100, a)
    p = 2*q + 1
    while (not isprime(p)):
        if len(list(pyecm.factors(a, False, True, 8, 1))) == 1:
            #print("a = ", a)
            q = generate_q(100, a)
            p = 2*q + 1
            a = a + 2
        else:
            a = a + 2
    if len(list(pyecm.factors(p, False, True, 8, 1))) == 1:
        print("\nq = {}, длина = {}".format(q, len(str(q))))
        print("\np = {}, длина = {}".format(p, len(str(p))))
        return p, q

start_time = time.time()	#время

p, q = find_p()

eiler = totient(p)

g = 2
for i in range(p-1):
    if binarn(g, q, p) != 1:
        break
    else:
        g += 1

print("\nПервообразный корень g = ", g)

x = randint(1, p-1)
print("\nЗакрытый ключ x = ", x)

y = binarn(g, x, p)
print("\nОткрытый ключ y = ", y)

M = int(input("\nВведите сообщение: "))
M = M % p
print("Сообщение M = ", M)

k = randint(1, p-1)
print("\nСессионный ключ k = ", k)

a = binarn(g, k, p)
b = binarn(y, k, p)
b = (b * M) % p

print("\nШифротекст: ({}, {})".format(a, b))

M1 = binarn(a, p - 1 - x, p)
M1 = (M1 * b) % p

print("\nРасшифрованное сообщение: ", M1)

print('\nЗатраченное время = ', time.time()-start_time)
