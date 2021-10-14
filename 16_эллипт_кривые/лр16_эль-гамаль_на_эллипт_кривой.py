import time
import sys
from random import randint
from sympy.ntheory import legendre_symbol

#параметры эллиптической кривой: p, a, b, q (ГОСТ 34.10-12)
param_curve = (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7,
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC4,
        0xE8C2505DEDFC86DDC1BD0B2B6667F1DA34B82574761CB0E879BD081CFD0B6265EE3CB090F30D27614CB4574010DA90DD862EF9D4EBEE4761503190785A71C760,
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF27E69532F48D89116FF22B8D4E0560609B4B38ABFAD2B85DCACDB1411F10B275)

def find_two(num):   #поиск степ 2ки, к-рые содерж в числе
    if num % 2 == 1:
        return 0, num

    power = 0

    while num % 2 != 1:
        
        num //= 2
        power += 1

    return power, num 

def sqrt_mod(n, p):         #вычисл кв корня по мод (алг Тонелли-Шэнкса)
    if p <= 3:
        raise Exception("p must be > 3") 

    S, Q = find_two(p - 1)

    if S == 0:
        raise Exception("p should be odd prime")

    if S == 1 and p % 4 == 3:
        R = pow(n, (p+1)//4, p)

        return R % p, p - R

    if S >= 2:
        
        #ищем произвольн квадратичн невычет
        z = 1
        while legendre_symbol(z,p) != -1:
            z += 1

        c = pow(z, Q, p)
        R = pow(n, (Q+1)//2, p)
        t = pow(n, Q, p)
        M = S

        while True:
            if t == 1:
                return R, p - R
            
            if t == 0:
                return 0

            for i in range(1,M):
                t_new = pow(t, 2**i, p)
                if t_new == 1:
                    b = pow(c, 2**(M-i-1), p)
                    R = R*b % p
                    t = (t*((b**2) % p)) % p
                    c = b**2 % p
                    M = i
                    break

def rand_point(a, b, p): #ген случ т. на эллипт кривой 

    x_cor = randint(1, p)
    f = x_cor**3 + a*x_cor + b

    while legendre_symbol(f, p) != 1:
        x_cor = randint(1, p)
        f = x_cor**3 + a*x_cor + b

    y1, y2 = sqrt_mod(f, p)

    G = []
    G.append(0)
    G.append(0)
    G[0] = x_cor
    G[1] = y1
    return G

def add(point_one_x, point_one_y, point_two_x, point_two_y, p): #слож 2х т. эллипт кривой

    L1 = lambda x1, x2, y1, y2, N: ((y2-y1)*invert(x2-x1, N)) % N
    L2 = lambda x1, y1, N: (3*x1**2 + a)*invert(2*y1, N) % N

    #случ, если одна из точек big_O, т.е нейтр эл-т по слож
    if (point_one_x == "O" and point_one_y == "O"):
        return point_two_x, point_two_y
    if (point_two_x == "O" and point_two_y == "O"):
        return point_one_x, point_one_y
        
    #случ, если т. наход на одной верт прямой 
    if (point_one_x == point_two_x and point_one_y != point_two_y):
        return Point("O","O")
    elif (point_one_y == point_two_y and point_one_y == 0):
        return Point("O","O")

    #все др случ считаем
    else:
        lmbd = 0
        if point_one_x!= point_two_x:
            lmbd = L1(point_one_x, point_two_x, point_one_y, point_two_y, p)

        elif point_one_x == point_two_x and point_one_y == point_two_y:
            lmbd = L2(point_one_x, point_one_y, p)

        X = (lmbd**2 - point_one_x - point_two_x) % p
        Y = (lmbd*(point_one_x - X) - point_one_y) % p
            
        return X, Y

def mul(point_one_x, point_one_y, n):
            
    if n < 0:
        point_one_y = - point_one_y    #если множитель n<0 => склад обр т.

    point_two_x = point_one_x
    point_two_y = point_one_y
    for i in range(-n):
        point_one_x, point_one_y = add(point_one_x, point_one_y, point_two_x, point_two_y, n) #склад n раз сами с собой

    return point_one_x, point_one_y

def exgcd(a, b):

    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return (x, y)

def invert(x, n):   #поиск обр числа y по мод n, что x*y == 1 (mod n)
    return exgcd(x, n)[0] % n
    
start_time = time.time()

#шифрование

#поле и кривая
p = param_curve[0]
a = param_curve[1]
b = param_curve[2]
q = param_curve[3]
print("\np = ", p)
print("\na = ", a)
print("\nb = ", b)
print("\nq = ", q)

M = int(input("\nВведите сообщение для шифрования: "))
M = M % p
print("Сообщение для шифрования: ", M)

G = rand_point(a, b, p)     #берем случ т. с этой кривой
print("\nВыбранная точка основания G = ", G)

#генерир ключи для А и В - закр и откр ключи из случ т. на кривой
c_b = randint(1, q-1)       #секр ключ
d_b = []
d_b.append(0)
d_b.append(0)
d_b[0], d_b[1] = mul(G[0], G[1], c_b)  #откр ключ

k = randint(1, q-1)         #случ число k
print("\nk = ", k)

R = []
R.append(0)
R.append(0)
R[0], R[1] = mul(G[0], G[1],k)      #R = [k]*G - умн случ т. на K - 1-я ч. шифротекста
print("\nR = ", R)

P = []
P.append(0)
P.append(0)
P[0], P[1] = mul(d_b[0], d_b[1],k)  #P = [k]*B_open = [k]*[A_key]*G - умн откр ключ адресата В на k
print("\nP = ", P)

e = M*P[0] % p                      #e = m*x mod p - 2-я ч. шифротекста
print("\nШифротекст e = ", e)

#дешифрование

Q = []
Q.append(0)
Q.append(0)
Q[0], Q[1] = mul(R[0], R[1], c_b)   #Q = [c_b]*R - вычисл т. Q
decode = e*invert(Q[0], p) % p      #m' = e*x^(-1) mod p

print("\nДекодированное сообщение: ", decode)

print('\nЗатраченное время =', time.time()-start_time)
