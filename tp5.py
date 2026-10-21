# === exo 1 =====

def lettre_vers_nombre(c):
    return ord(c) - ord("A")

def nombre_vers_lettre(n):
    return chr(n % 26 + ord("A"))

print(lettre_vers_nombre("C"), nombre_vers_lettre(2))
print([nombre_vers_lettre(lettre_vers_nombre(c)) == c for c in "ABCXYZ"])

import unicodedata

def nettoyer(texte):
    sans_accent = unicodedata.normalize("NFD", texte)
    sans_accent = "".join(c for c in sans_accent if unicodedata.category(c) != "Mn")
    return "".join(c for c in sans_accent.upper() if "A" <= c <= "Z")

print(nettoyer("Été, à Paris !"))

# ==== exo 2 ====

def chiffrer(texte, a, b):
    resultat = []
    for c in nettoyer(texte):
        x = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre((a * x + b) % 26))
    return "".join(resultat)

message = "ATTAQUEALAUBE"
print(chiffrer(message, 7, 11))
print(chiffrer(message, 1, 3))   

# ==== exo 3 ====

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

valides = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print(valides)
print(len(valides), "valeurs possibles pour a")

def inverse_modulaire(a, n):
    a = a % n
    for candidat in range(1, n):
        if (a * candidat) % n == 1:
            return candidat
    raise ValueError(f"{a} n'est pas inversible modulo {n}")

print(inverse_modulaire(7, 26))
print((7 * 15) % 26)

try:
    inverse_modulaire(4, 26)
except ValueError as erreur:
    print("erreur attendue :", erreur)

# ==== exo 4 ====

def dechiffrer(texte, a, b):
    a_inverse = inverse_modulaire(a, 26)
    resultat = []
    for c in nettoyer(texte):
        y = lettre_vers_nombre(c)
        resultat.append(nombre_vers_lettre(a_inverse * (y - b) % 26))
    return "".join(resultat)

message = nettoyer("Attaque a l aube")
secret = chiffrer(message, 7, 11)
print(secret)
print(dechiffrer(secret, 7, 11))
print(dechiffrer(secret, 7, 11) == message)

try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print("cle refusee :", erreur)


# ==== exo 5 ====

def toutes_les_clefs(secret):
    resultats = []
    for a in valides:
        for b in range(26):
            resultats.append((a, b, dechiffrer(secret, a, b)))
    return resultats

essais = toutes_les_clefs(secret)
print(len(essais), "clefs essayees")
bons = [e for e in essais if e[2] == message]
print("la bonne clef :", bons[0][0], bons[0][1])


# ==== exo 6 ====
from collections import Counter

texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles."
)
secret_long = chiffrer(texte_long, 9, 4)

comptes = Counter(secret_long)
lettre_frequente = comptes.most_common(1)[0][0]
print("lettre la plus frequente du chiffre :", lettre_frequente)

cible = lettre_vers_nombre(lettre_frequente)
candidats = []
for a in valides:
    b = (cible - 4 * a) % 26
    candidats.append((a, b, dechiffrer(secret_long, a, b)))

print(len(candidats), "candidats au lieu de 312")
for a, b, texte in candidats:
    if texte.startswith("LECHIFFREMENT"):
        print("trouve :", a, b)
        print(texte[:60])

# ==== exo 7 ====

import random

def indice_coincidence(texte):
    N = len(texte)
    comptes = Counter(texte)
    return sum(n * (n - 1) for n in comptes.values()) / (N * (N - 1))

random.seed(1)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
hasard = "".join(random.choice(alphabet) for _ in range(len(texte_long)))

print(f"clair    : {indice_coincidence(texte_long):.4f}")
print(f"affine   : {indice_coincidence(secret_long):.4f}")
print(f"hasard   : {indice_coincidence(hasard):.4f}")

# ==== exo 8 ====
def vigenere(texte, cle):
    resultat = []
    for i, c in enumerate(nettoyer(texte)):
        decalage = lettre_vers_nombre(cle[i % len(cle)])
        resultat.append(nombre_vers_lettre(lettre_vers_nombre(c) + decalage))
    return "".join(resultat)

secret_vigenere = vigenere(texte_long, "LUNE")
print(secret_vigenere[:40])
print(f"IC vigenere : {indice_coincidence(secret_vigenere):.4f}")

for L in range(1, 8):
    colonnes = [secret_vigenere[i::L] for i in range(L)]
    moyenne = sum(indice_coincidence(col) for col in colonnes) / L
    print(f"L = {L} : indice moyen {moyenne:.4f}")