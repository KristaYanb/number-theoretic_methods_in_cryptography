import gmpy2 
import pyecm
from random import randint
import time
from math import pi

def is_square_free(n):
	prime_list = list(pyecm.factors(n,False,True, 8, 1))
	for i in range(len(prime_list)-1):
		if prime_list[i] == prime_list[i+1]:
			return False
	return True

N = 10**50
M = 1000

summ = 0

start_time = time.time()

for i in range(M):
	a = randint(1, N)
	print(a)
	if is_square_free(a):
		summ += 1
	else:
		summ += 0

print('Затраченное время = ', time.time()-start_time)
print('Вероятность = ', summ/M)
print('Теоретическая оценка = ', 6/pi**2)
