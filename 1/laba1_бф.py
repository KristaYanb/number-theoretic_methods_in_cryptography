from random import randint
from math import log, pi 
import time

N = 10**100         #отрезок
M = 10000           #повторы

itter = 0                           #кол-во делений (сумма по всем числам)
i = 0
j = 0
start_time = time.time()

a1 = 0
b1 = 0
#aM = 0
#bM = 0

while i < M:
    a = randint(1, N)
    b = randint(1, N)
    a1 += a/M
    b1 += b/M
    step = 0                    #число делений по каждому числу
    while (a!=0 and b!=0):      #алгоритм Евклида
        if a > b:
            a = a % b
        else:
            b = b % a
        step += 1
    itter += step
    i += 1
    
print("Среднее число a: ", a1)
print("Среднее число b: ", b1)

"""k = 1
k1 = 0
while j <= N:
    k1 += k/N
    k += 1
    j += 1
print("Мат ож: ", k)"""

print('Затраченное время = ', time.time()-start_time)

avg_count = itter/M                 #среднее число делений

print('Среднее число делений = ', avg_count)
teor = 12*log(2)*log(N)/pi**2
print('Теоретическая оценка = ', teor)
