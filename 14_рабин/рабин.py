import time
import pyecm
from sympy import factorint
from sympy.ntheory import totient

def generate_p_q():
    
    prime_number = 82       
    start_prime = 359          
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
    return p, q

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

def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0, y0

start_time = time.time()	#время

p, q = generate_p_q()

n = p * q
print("\nn = ", n)

m = int(input("\nВведите сообщение: "))
m = m % n
print("Сообщение: ", m)

c = (m**2) % n
print("\nЗашифрованное сообщение: ", c)

m1 = binarn(c, (p+1)//4, p)
m2 = binarn(c, (q+1)//4, q)
print("\nm1 = {}, m2 = {}".format(m1, m2))

y1, y2 = xgcd(p, q)
print("\ny1 = {}, y2 = {}".format(y1, y2))

r1 = (y1*p*m2 + y2*q*m1) % n
r2 = (n - r1)
r3 = (y1*p*m2 - y2*q*m1) % n
r4 = (n - r3)
print("\nr1 =", r1)
print("\nr2 =", r2)
print("\nr3 =", r3)
print("\nr4 =", r4)

if r1 == m:
    print("\nРасшифрованное сообщение r1: ", r1)
else:
    if r2 == m:
        print("\nРасшифрованное сообщение r2: ", r2)
    else:
        if r3 == m:
            print("\nРасшифрованное сообщение r3: ", r3)
        else:
            print("\nРасшифрованное сообщение r4: ", r4)
                       
print('\nЗатраченное время = ', time.time()-start_time)
