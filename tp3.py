def evaluer_naif(P, x):
    total = 0
    for i in range(len(P)):
        total = total + P[i] * x ** i
    return total

# print(evaluer_naif([2, 3, 0, 5], 2))
# print(evaluer_naif([2, 3, 0, 5], 0))

# ======== EXO 2 ==============

def evaluer(P, x):
    total = 0
    for coefficient in reversed(P):
        total = total * x + coefficient
    return total

P = [2, 3, 0, 5]
# for x in (-5, 0, 1, 3, 12):
#     print(x, evaluer_naif(P, x), evaluer(P, x))

import time

for degre in (1000, 5000, 20000):
    P = [1] * (degre + 1)

    debut = time.perf_counter()
    a = evaluer_naif(P, 1.0001)
    t_naif = time.perf_counter() - debut

    debut = time.perf_counter()
    b = evaluer(P, 1.0001)
    t_horner = time.perf_counter() - debut

    # print(f"degre {degre:>6} : naif {t_naif:.5f} s | horner {t_horner:.5f} s "
    #       f"| rapport {t_naif / t_horner:.1f} | ecart des valeurs {abs(a - b):.2e}")

for degre in (200, 400, 800):
    P = [1] * (degre + 1)

    debut = time.perf_counter()
    a = evaluer_naif(P, 3)
    t_naif = time.perf_counter() - debut

    debut = time.perf_counter()
    b = evaluer(P, 3)
    t_horner = time.perf_counter() - debut

    # print(f"degre {degre:>4} : rapport {t_naif / t_horner:.1f} | resultats egaux : {a == b}")


# ========= EXo 3 ===========
def deriver(P):
    resultat = []
    for i in range(1, len(P)):
        resultat.append(i * P[i])
    return resultat

# print(deriver([2, 3, 0, 5]))
# print(deriver([7]))

# ============ exo 4 ===========

def dichotomie(f, a, b, tolerance=1e-12):
    fa, fb = f(a), f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) doivent etre de signes opposes")
    while b - a > tolerance:
        milieu = (a + b) / 2
        if f(a) * f(milieu) <= 0:
            b = milieu
        else:
            a = milieu
    return (a + b) / 2

def carre_moins_deux(x):
    return x * x - 2

racine = dichotomie(carre_moins_deux, 0, 2)
# print(racine)
# print(abs(racine - 2 ** 0.5) < 1e-9)

def newton(P, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(P)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("tangente horizontale, Newton ne peut pas continuer")
        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError("pas de convergence en {} tours".format(tours_max))

# print(racine, "en", newton([-5, -2, 0, 1], 2), "tours")
# print(abs(evaluer([-5, -2, 0, 1], newton([-5, -2, 0, 1], 2))) < 1e-10)

def newton_trace(P, depart, tours):
    derivee = deriver(P)
    x = float(depart)
    trajet = [x]
    for _ in range(tours):
        pente = evaluer(derivee, x)
        if pente == 0:
            break
        x = x - evaluer(P, x) / pente
        trajet.append(x)
    return trajet


# print(newton_trace([2, -2, 0, 1] , 0, 8))

# try:
#     print(newton(R, 0))
# except RuntimeError as erreur:
#     print("echec :", erreur)


for i in (2, 1, 0):
    racine, tours = newton([-5, -2, 0, 1], i)
    # print(f"depart {i:>2} : {tours:>2} tours, racine {racine:.9f}")

# =========== exo 5 ==============

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

if plt is not None:
    Q = [-5, -2, 0, 1]
    xs = []
    ys = []
    for i in range(-300, 301):
        x = i / 100
        xs.append(x)
        ys.append(evaluer(Q, x))

    plt.figure()
    plt.plot(xs, ys, label="x^3 - 2x - 5")
    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)
    plt.ylim(-20, 20)
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.legend()
    plt.title("Un polynome et son unique racine reelle")


# === exo 6 =========
def somme(P, Q):
    longueur = max(len(P), len(Q))
    P = P + [0] * (longueur - len(P))
    Q = Q + [0] * (longueur - len(Q))
    resultat = []
    for i in range(longueur):
        resultat.append(P[i] + Q[i])
    return resultat

def produit_poly(P, Q):
    if not P or not Q:
        return []
    R = [0] * (len(P) + len(Q) - 1)
    for i in range(len(P)):
        for j in range(len(Q)):
            R[i + j] = R[i + j] + P[i] * Q[j]
    return R

# print(somme([1, 2], [0, 0, 3]))
# print(produit_poly([1, 1], [1, 1]))
# print(produit_poly([-1, 1], [1, 1]))

binome = [1]
for _ in range(10):
    binome = produit_poly(binome, [1, 1])
# print(binome)
# print(sum(binome), 2 ** 10)

# ==== exo 7 ======
import math

def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h

def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

exacte = math.cos(1.0)
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
    e_avant = abs(derivee_avant(math.sin, 1.0, h) - exacte)
    e_centree = abs(derivee_centree(math.sin, 1.0, h) - exacte)
    # print(f"h = {h:.0e} : avant {e_avant:.1e} | centree {e_centree:.1e}")


# ==== exo 8 ====

def rectangles(f, a, b, n):
    h = (b - a) / n
    total = 0
    for i in range(n):
        total = total + f(a + i * h)
    return h * total

def trapezes(f, a, b, n):
    h = (b - a) / n
    interieur = 0
    for i in range(1, n):
        interieur = interieur + f(a + i * h)
    return h * ((f(a) + f(b)) / 2 + interieur)

def simpson(f, a, b, n):
    if n % 2 == 1:
        n = n + 1
    h = (b - a) / n
    impairs = 0
    for i in range(1, n, 2):
        impairs = impairs + f(a + i * h)
    pairs = 0
    for i in range(2, n, 2):
        pairs = pairs + f(a + i * h)
    return h / 3 * (f(a) + f(b) + 4 * impairs + 2 * pairs)

def carre(x):
    return x * x

for n in (10, 100, 1000):
    e_rect = abs(rectangles(carre, 0, 1, n) - 1 / 3)
    e_trap = abs(trapezes(carre, 0, 1, n) - 1 / 3)
    e_simp = abs(simpson(carre, 0, 1, n) - 1 / 3)
    # print(f"n = {n:>4} : rectangles {e_rect:.1e} | trapezes {e_trap:.1e} | simpson {e_simp:.1e}")


def arctangente_derivee(x):
    return 4 / (1 + x * x)

approx_trap = trapezes(arctangente_derivee, 0, 1, 1000)
approx_simp = simpson(arctangente_derivee, 0, 1, 1000)
# print(approx_trap, abs(approx_trap - math.pi))
# print(approx_simp, abs(approx_simp - math.pi))