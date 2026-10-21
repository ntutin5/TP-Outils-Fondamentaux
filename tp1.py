import math


def presque_egaux(a, b, tolerance=1e-9):
    return abs(a - b) <= tolerance


def nb_de_chiffre(n):
    n = abs(n)
    nombre = 1
    while n >= 10:
        n = n // 10
        nombre = nombre + 1
    return nombre


def heron(a, tolerance=1e-12):
    if a < 0:
        return "valeur negatif"
    if a == 0:
        return 0.0

    x = float(a)
    while True:
        nouveau_x = (x + a / x) / 2
        if abs(nouveau_x - x) <= tolerance * abs(nouveau_x):
            return nouveau_x
        x = nouveau_x


print(heron(2))
print(math.sqrt(2))
print(presque_egaux(heron(2), math.sqrt(2)))