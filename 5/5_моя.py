import time 
from sympy.ntheory import totient

N = 2019
a = 2019
z = 10**2019

start_time = time.time()	#время

eiler = totient(z)              #ф-ция Эйлера
new_a = a

for i in range(N-1):
	r = new_a % eiler
	new_a = pow(a,r,z) 	#a^r (mod z)
	print(i) 	        #номер итерации
print(new_a)
print('Затраченное время = ', time.time()-start_time)
