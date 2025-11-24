import math


def e_exp_e_pi():
    return math.exp(math.exp(math.pi))


def harmonic_sum_10000():
    return sum(1.0 / n for n in range(1, 10001))


def primes_under(limit):
    if limit < 2:
        return []

    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    p = 2
    while p * p <= limit:
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
        p += 1

    return [n for n in range(2, limit) if sieve[n]]


def count_primes_under_10000():
    return len(primes_under(10000))


def order_GL3_Z7():
    q = 7
    n = 3
    return (q**n - 1) * (q**n - q) * (q**n - q**2)


def alternating_sum_1_to_1e6() :
    s = 0.0
    sign = -1.0 
    for n in range(1, 10**6 + 1):
        s += sign / n
        sign = -sign
    return s


def _sin_over_x(x):
    if x == 0.0:
        return 1.0  
    return math.sin(x) / x


def integral_sin_x_over_x_0_100(n_steps: int = 100000) :
    if n_steps % 2 == 1:
        n_steps += 1

    a, b = 0.0, 100.0
    h = (b - a) / n_steps
    s = _sin_over_x(a) + _sin_over_x(b)

    for i in range(1, n_steps):
        x = a + i * h
        coef = 4 if i % 2 == 1 else 2
        s += coef * _sin_over_x(x)

    return s * h / 3.0


def prime_product_under_10000():
    prod = 1.0
    for p in primes_under(10000):
        prod *= 1.0 / (1.0 - 1.0 / p)  
    return prod


def binom_10_5():
    return math.comb(10, 5)


def log_factorial_100():
    return math.lgamma(101.0)


def euler_phi(n) :
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def phi_63():
    return euler_phi(63)


print("e^{e^{pi}} =", e_exp_e_pi())
print("sum_{n=1}^{10000} 1/n =", harmonic_sum_10000())
print("|{p premier : p < 10000}| =", count_primes_under_10000())
print("|GL_3(Z/7Z)| =", order_GL3_Z7())
print("sum_{n=1}^{10^6} (-1)^n / n =", alternating_sum_1_to_1e6())
print("∫_0^{100} sin(x)/x dx ≈", integral_sin_x_over_x_0_100())
print("∏_{p<10000} (1 - 1/p)^(-1) ≈", prime_product_under_10000())
print("C(10, 5) =", binom_10_5())
print("ln(100!) =", log_factorial_100())
print("phi(63) =", phi_63())
