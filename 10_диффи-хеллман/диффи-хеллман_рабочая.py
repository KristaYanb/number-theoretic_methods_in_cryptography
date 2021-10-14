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
    a = 3
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

a = randint(1, 703503704377529130553306840697074855410577792808958060862168606495439)
print("a = ", a)
b = randint(1, 8380329074897079174859830551541464287981119146440204133333743645049581)
print("b = ", b)

p, q = find_p()

eiler = totient(p)

g = 2
for i in range(p-1):
    if binarn(g, q, p) != 1:
        break
    else:
        g += 1

print("g = ", g)

r_a = a % eiler
A = binarn(g, r_a, p)

print("\nОткрытый ключ A = {}, длина = {}".format(A, len(str(A))))

r_b = b % eiler
B = binarn(g, r_b, p)
print("\nОткрытый ключ B = {}, длина = {}".format(B, len(str(B))))

K = binarn(B, r_a, p)
print("\nЗакрытый ключ K = {}, длина = {}".format(K, len(str(K))))

K2 = binarn(A, r_b, p)
print("\nПроверка: закрытый ключ K = {}, длина = {}".format(K, len(str(K))))

message = input("\nВведите сообщение для шифрования: ")
encrypted_message = ''
for char in message:
    encrypted_message += chr((ord(char) + K) % 256)
print("\nЗашифрованное сообщение: ", encrypted_message)

decrypted_message = ''
for char in encrypted_message:
    decrypted_message += chr((ord(char) - K) % 256)
print("\nРасшифрованное сообщение: ", decrypted_message)
    
print('\nЗатраченное время = ', time.time()-start_time)
