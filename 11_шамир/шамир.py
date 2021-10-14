import time
import pyecm
from math import gcd

def generate_p():
    prime_number = 82
    start_prime = 373
    tmp = start_prime
    p = 0
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
    p = tmp
    print("\np = {}, длина = {}".format(p, len(str(p))))
    return p

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

start_time = time.time()	#время

p = generate_p()

c_a = 0
i = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000029599
while i < p:
    if (gcd(i, p - 1) == 1):
        c_a = i
        break
    else:
        i += 1
print("\nc_a = {}, длина = {}".format(c_a, len(str(c_a))))

d_a = 0                       
d_a = exgcd(c_a, p - 1)
d_a = d_a % (p - 1)
print("\nd_a = {}, длина = {}".format(d_a, len(str(d_a))))

#print(c_a * d_a % (p - 1))

c_b = 0
i = 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000788921
while i < p:
    if (gcd(i, p - 1) == 1):
        c_b = i
        break
    else:
        i += 1
print("\nc_b = {}, длина = {}".format(c_b, len(str(c_b))))

d_b = 0                       
d_b = exgcd(c_b, p - 1)
d_b = d_b % (p - 1)
print("\nd_b = {}, длина = {}".format(d_b, len(str(d_b))))

#print(c_b * d_b % (p - 1))

m = int(input("\nВведите сообщение для шифрования: "))
m = m % p
print("Сообщение для шифрования: ", m)

x1 = binarn(m, c_a, p)
print("\nx1 = ", x1)

x2 = binarn(x1, c_b, p)
print("\nx2 = ", x2)

x3 = binarn(x2, d_a, p)
print("\nx3 = ", x3)

x4 = binarn(x3, d_b, p)
print("\nx4 (исходное сообщение) = ", x4)

print('\nЗатраченное время = ', time.time()-start_time)
