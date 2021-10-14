from random import randint
from math import log 
import time

N = 10**100         #отрезок
M = 10000           #повторы

count = 0           #кол-во подходящих условию чисел
i = 0
start_time = time.time()

while i < M:
    b = randint(1, N)
    if (N % b) < b/2:       #сравниваем остаток от деления
            count += 1
    i += 1

print('Затраченное время = ', time.time()-start_time)

probability = count/M

print('Вероятность = ', probability)
teor = 2-2*log(2)
print('Теоретическая оценка = ', teor)
