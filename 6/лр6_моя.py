import time
import pyecm
from sympy import factorint

start_time = time.time()

prime_number = 500
                                
start_prime = 2011         #305-е простое число (с википедии)
tmp = start_prime

for i in range(1000):
    print(i)
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
    print(tmp)
    print(len(str(tmp)))
    #print(factorint(tmp))
    #print(len(factorint(tmp)))
    start_prime = start_prime + 2
    while len(list(pyecm.factors(start_prime, False, True, 8, 1))) != 1:
        start_prime = start_prime + 2
    tmp = start_prime

print("Время выполнения: ", time.time() - start_time)
