def diviseurs(n):
    resultat = []
    for d in range(1, n + 1):
        if n % d == 0:
            resultat.append(d)
    return resultat

# print(diviseurs(28))
# print(diviseurs(97))

def pgcd_naif(a, b):
    meilleur = 1
    for d in range(1, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            meilleur = d
    return meilleur

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# print(pgcd_naif(1071, 462), pgcd(1071, 462))

import time

def est_premier_naif(n):
    """Teste la primalité en essayant tous les diviseurs jusqu'à n - 1."""
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True

# print(est_premier_naif(97), est_premier_naif(91))

def est_premier(n):
    """Teste la primalité en s'arrêtant à la racine carrée de n."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 2
    return True

# print(est_premier(97), est_premier(91), est_premier(2), est_premier(1))

def duree(fonction, argument):
    """Renvoie le temps d'exécution de fonction(argument), en secondes."""
    debut = time.perf_counter()
    fonction(argument)
    return time.perf_counter() - debut

# n = 1_000_003  # un nombre premier
# print(f"naif        : {duree(est_premier_naif, n):.4f} s")
# print(f"jusqu'a rac : {duree(est_premier, n):.6f} s")

# for n in (10007, 100003, 1000003):
#     t_naif = duree(est_premier_naif, n)
#     t_rac = duree(est_premier, n)
#     print(f"{n:>9} : naif {t_naif:.5f} s | racine {t_rac:.6f} s")


def crible(limite):
    """Renvoie la liste des nombres premiers de 2 à limite inclus."""
    est_premier_tab = [True] * (limite + 1)
    est_premier_tab[0] = False
    if limite >= 1:
        est_premier_tab[1] = False
    d = 2
    while d * d <= limite:
        if est_premier_tab[d]:
            for multiple in range(d * d, limite + 1, d):
                est_premier_tab[multiple] = False
        d = d + 1
    resultat = []
    for n in range(limite + 1):
        if est_premier_tab[n]:
            resultat.append(n)
    return resultat

# premiers = crible(100)
# print(premiers)
# print(len(premiers), "premiers jusqu'a 100")


debut = time.perf_counter()
p = crible(100000)
t_cribble = time.perf_counter()-debut

d=time.perf_counter()
c = sum(1 for n in range(100001)if est_premier(n))
t_1_par_1 = time.perf_counter()-debut

# print(len(p),c)
# print("cribble",t_cribble,"un par un ",t_1_par_1)


def facteurs(n):
    res = []
    d=2
    while d*d<=n:
        while n%d==0:
            res.append(d)
            n=n//d
        d=d+1
    if n>1:
        res.append(n)
    return res

# print(facteurs(360))

p = 1
for x in (facteurs(360)):
    p=p*x
# print(p)



def fibonacci_recursif(n):
    """F(n) en suivant la définition, par récurrence."""
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)

# print([fibonacci_recursif(n) for n in range(15)])

# for i in (20,25,30):
#     print("F",i,duree(fibonacci_recursif,i))

appel={}

def fibonacci_compte(n):
    appel[n]=appel.get(n,0)+1
    if n<2:
        return n
    return fibonacci_compte(n-1)+fibonacci_compte(n-2)

print("f30 =",fibonacci_compte(30))
print("appel f1",appel[1])
print("appel total",sum(appel.values()))

def fibo(n):
    prec=0
    suiv=1
    for _ in range(n):
        ancien=prec
        prec=suiv
        suiv=ancien+suiv
    return prec

# print(all(fibo(n)==fibonacci_recursif(n) for n in range(26)))
# print("f30",duree(fibo,30))
# print(len(str(fibo(10000))),"chiffres")

def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v

g, u, v = euclide_etendu(1071, 462)
print(g, u, v, 1071 * u + 462 * v == g)


def puissance_mod_naive(a, e, n):
    """a^e mod n, par e multiplications successives."""
    resultat = 1
    for _ in range(e):
        resultat = resultat * a % n
    return resultat

def puissance_mod(a, e, n):
    """a^e mod n, par élévations au carré successives."""
    resultat = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            resultat = resultat * a % n
        a = a * a % n
        e = e // 2
    return resultat

a, e, n = 7, 10 ** 7, 1_000_003
print(puissance_mod(a, e, n), pow(a, e, n))

debut = time.perf_counter()
puissance_mod_naive(a, e, n)
t_naive = time.perf_counter() - debut
debut = time.perf_counter()
puissance_mod(a, e, n)
t_rapide = time.perf_counter() - debut
print("naive",t_naive,"rapide",t_rapide)