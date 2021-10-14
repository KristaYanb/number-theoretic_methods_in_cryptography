from random import randint
from math import pi 
import time

N = 10**100         #отрезок
M = 10000           #повторы

count = 0                           #кол-во случаев взаимной простоты
i = 0
start_time = time.time()
while i < M:
    a = randint(1, N)
    b = randint(1, N)
    while (a!=0 and b!=0):      #алгоритм Евклида
        if a > b:
            a = a % b
        else:
            b = b % a
    if (a + b) == 1:            #если НОД = 1
                count += 1
    i += 1
    
print('Затраченное время = ', time.time()-start_time)

probability = count/M

print('Вероятность = ', probability)
teor = 6/pi**2
print('Теоретическая оценка = ', teor)
