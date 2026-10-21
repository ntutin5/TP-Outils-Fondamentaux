# ==== exo 1 ====
A = [[1, 2, 2],
    [1, 2, 1],
    [0, 1, 2]]

print(A[0])
print(A[0][2])
print(len(A), len(A[0]))

def transposee(A):
    lignes = len(A)
    colonnes = len(A[0])
    resultat = []
    for j in range(colonnes):
        ligne = []
        for i in range(lignes):
            ligne.append(A[i][j])
        resultat.append(ligne)
    return resultat

# ==== exo 2 ====

def produit(A, B):
    """Produit matriciel A x B, en Python pur."""
    n, p = len(A), len(A[0])
    if len(B) != p:
        raise ValueError("dimensions incompatibles")
    q = len(B[0])
    C = [[0] * q for _ in range(n)]
    for i in range(n):
        for j in range(q):
            somme = 0
            for k in range(p):
                somme = somme + A[i][k] * B[k][j]
            C[i][j] = somme
    return C

identite = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
A = [[1, 2, 2], [1, 2, 1], [0, 1, 2]]
print(produit(A, identite) == A)
print(produit([[2, 3], [4, 5]], [[0, 1], [1, 0]]))


import random
import time

random.seed(24)

def matrice_aleatoire(n):
    matrice = []
    for i in range(n):
        ligne = []
        for j in range(n):
            ligne.append(random.random())
        matrice.append(ligne)
    return matrice

for n in (40, 80, 120):
    A = matrice_aleatoire(n)
    B = matrice_aleatoire(n)
    debut = time.perf_counter()
    produit(A, B)
    print(f"n = {n:>3} : {time.perf_counter() - debut:.4f} s")

# ==== exo 3 ====

try:
    import numpy as np
except ImportError:
    np = None

if np is not None:
    A_numpy = np.array([[1.0, 2.0, 2.0],
                        [1.0, 2.0, 1.0],
                        [0.0, 1.0, 2.0]])
    b_numpy = np.array([3.0, 4.0, 3.0])

n = 120
A = matrice_aleatoire(n)
B = matrice_aleatoire(n)

debut = time.perf_counter()
produit(A, B)
t_python = time.perf_counter() - debut

if np is not None:
    An, Bn = np.array(A), np.array(B)
    debut = time.perf_counter()
    An @ Bn
    t_numpy = time.perf_counter() - debut

print(f"python pur {t_python:.4f} s")
if np is not None:
    print(f"numpy      {t_numpy:.6f} s")
    print("rapport :", round(t_python / max(t_numpy, 1e-9)))


# ==== exo 4 ====

def resoudre(A, b, tolerance=1e-14):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]

    for k in range(n):
        meilleure = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[meilleure][k]):
                meilleure = i
        if abs(M[meilleure][k]) <= tolerance:
            raise ValueError("systeme singulier ou mal pose")
        M[k], M[meilleure] = M[meilleure], M[k]

        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] = M[i][j] - facteur * M[k][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        somme = M[i][n]
        for j in range(i + 1, n):
            somme = somme - M[i][j] * x[j]
        x[i] = somme / M[i][i]
    return x

A = [[1, 2, 2], [1, 2, 1], [0, 1, 2]]
b = [3, 4, 3]
x = resoudre(A, b)
print([round(v, 10) for v in x])

verif = []
for i in range(3):
    somme = 0
    for j in range(3):
        somme = somme + A[i][j] * x[j]
    verif.append(somme)
print([round(v, 10) for v in verif])


random.seed(11)
n = 50
A = matrice_aleatoire(n)
b = [random.random() for _ in range(n)]

mienne = resoudre(A, b)
if np is not None:
    celle_de_numpy = np.linalg.solve(np.array(A), np.array(b))
    ecart = 0
    for i in range(n):
        difference = abs(mienne[i] - celle_de_numpy[i])
        if difference > ecart:
            ecart = difference
    print("ecart maximal :", ecart)
    print(ecart < 1e-9)


# ==== exo 5 =====

def hilbert(n):
    matrice = []
    for i in range(n):
        ligne = []
        for j in range(n):
            ligne.append(1.0 / (i + j + 1))
        matrice.append(ligne)
    return matrice

n = 12
H = hilbert(n)
if np is not None:
    H_numpy = np.array(H)
    x_vrai = np.ones(n)
    b_numpy = H_numpy @ x_vrai

    x_solve = np.linalg.solve(H_numpy, b_numpy)
    x_inverse = np.linalg.inv(H_numpy) @ b_numpy

    print("erreur avec solve   :", float(np.max(np.abs(x_solve - x_vrai))))
    print("erreur avec inv @ b :", float(np.max(np.abs(x_inverse - x_vrai))))
    print("conditionnement     : {:.3e}".format(float(np.linalg.cond(H_numpy))))

# ==== exo 6 ====

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

if np is not None:
    def rotation(angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([[c, -s], [s, c]])

    maison = np.array([[0, 0], [2, 0], [2, 1.5], [1, 2.5], [0, 1.5], [0, 0]]).T

    if plt is not None:
        plt.figure(figsize=(5, 5))
        plt.plot(maison[0], maison[1], label="depart")
        for angle in (np.pi / 8, np.pi / 4, 3 * np.pi / 8):
            image = rotation(angle) @ maison
            plt.plot(image[0], image[1], label=f"rotation {int(np.degrees(angle))} degres")
        plt.axis("equal")
        plt.legend()
        plt.title("Une matrice fait tourner une figure")
        plt.show()

    gauche = rotation(np.pi / 4) @ rotation(np.pi / 8)
    droite = rotation(3 * np.pi / 8)
    print(np.allclose(gauche, droite))
    print(np.round(droite, 10))

# ==== exo 7 ====

def determinant(A):
    
    n = len(A)
    M = [list(ligne) for ligne in A]
    det = 1.0
    for k in range(n):
        meilleure = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[meilleure][k]) < 1e-14:
            return 0.0
        if meilleure != k:
            M[k], M[meilleure] = M[meilleure], M[k]
            det = -det
        det = det * M[k][k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] = M[i][j] - facteur * M[k][j]
    return det

A = [[1, 2, 2], [1, 2, 1], [0, 1, 2]]
if np is not None:
    print(determinant(A), float(np.linalg.det(np.array(A, dtype=float))))
print(determinant([[1, 2], [2, 4]]))

# ==== exo 8 ===
from fractions import Fraction

def hilbert_exacte(n):
    return [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]

n = 12
H_exacte = hilbert_exacte(n)
b_exact = [sum(ligne) for ligne in H_exacte]

try:
    resoudre(H_exacte, b_exact)
except ValueError as erreur:
    print("premier essai :", erreur)

x_exact = resoudre(H_exacte, b_exact, tolerance=0)
print(x_exact)
print(all(v == 1 for v in x_exact))

# ==== exo 9 ===== 

def translation(tx, ty):
    return np.array([[1.0, 0.0, tx],
                     [0.0, 1.0, ty],
                     [0.0, 0.0, 1.0]])

def rotation_h(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0.0],
                     [s, c, 0.0],
                     [0.0, 0.0, 1.0]])

if np is not None:
    point = np.array([1.0, 0.0, 1.0])
    T = translation(3, 1)
    R = rotation_h(np.pi / 2)
    print(np.round(R @ T @ point, 10))
    print(np.round(T @ R @ point, 10))