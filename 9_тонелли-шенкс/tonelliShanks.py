from sympy.ntheory import legendre_symbol
import time
import sys

def generate_p():

    prime_number = 83       
    start_prime = 353
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

def find_two(num):   #поиск степ 2ки, к-рые содерж в числе
    if num % 2 == 1:
        return 0, num

    power = 0

    while num % 2 != 1:
        
        num //= 2
        power += 1
    print("S = {}, Q = {}".format(power, num))

    return power, num 

def sqrt_mod(n, p):         #вычисл кв корня по мод (алг Тонелли-Шэнкса)

    S, Q = find_two(p - 1)

    if S >= 2:
        
        #ищем произвольн квадратичн невычет
        z = 1
        while legendre_symbol(z,p) != -1:
            z += 1
        print("z = ", z)

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

def p_5_mod_8(n, p):

    if pow(n, (p-1)//4, p) == 1:
            R = pow(n, (p + 3)//8, p)
            
    elif pow(n, (p-1)//4, p) == -1:
        R = pow(n, (p + 3)//8, p)*pow(2, (p - 1)//4, p)

    else:
        print("Корней нет")
        sys.exit()

    return R % p, p - R

def p_41_mod_48(n, p):

    if pow(n, (p-1)//4, p) == 1:
        if pow(n, (p-1)//8, p) == 1:
            R = pow(n, (p + 7)//16, p)
        elif pow(n, (p-1)//8, p) == -1%p:
            R = pow(n, (p + 7)//16, p)*pow(3, (p - 1)//4, p)
        else:
            print("Корней нет")
            sys.exit()
            
    elif pow(n, (p-1)//4, p) == -1%p:
        if (pow(n, (p-1)//8, p)*pow(3, (p - 1)//4, p))%p == 1:
            R = pow(n, (p + 7)//16, p)*pow(3, (p - 1)//8, p)
        elif (pow(n, (p-1)//8, p)*pow(3, (p - 1)//4, p))%p == -1%p:
            R = pow(n, (p + 7)//16, p)*pow(3, (3*p - 3)//8, p)
        else:
            print("Корней нет")
            sys.exit()

    else:
        print("Корней нет")
        sys.exit()

    return R % p, (p - R)%p

start_time = time.time()

p = generate_p()
#p = 89
#print("p = ", p)

if p <= 3:
    print("p должен быть > 3")
    sys.exit()
    
isKvadratic = False
while isKvadratic != True:
    m = int(input("\nВведите число, из которого необходимо извлечь корень: "))
    m = m % p
    if legendre_symbol(m, p) == 1:
        isKvadratic = True
    else:
        print("Не выполнено условие разрешимости сравнения\nЧисло должно быть квадратичным вычетом по модулю p")

print("\nЧисло: ", m)

if p % 4 == 3:
    print("\np % 4 == 3")
    R = pow(m, (p+1)//4, p)
    y1 = R % p
    y2 = p - R
    
elif p % 8 == 5:
    print("\np % 8 == 5")
    y1, y2 = p_5_mod_8(m, p)

elif p % 48 == 41:
    print("\np % 48 == 41")
    y1, y2 = p_41_mod_48(m, p)
    
else:
    print("\nИспользуем общий случай")
    y1, y2 = sqrt_mod(m, p)

print("\nКорни:\n(1) {}\n\n(2) {}".format(y1, y2))

#проверка

print("\nПроверка:\n(1) {}\n\n(2) {}".format(y1**2 % p, y2**2 % p))

print('\nЗатраченное время =', time.time()-start_time)
