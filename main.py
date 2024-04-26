from random import randint
import itertools

class LFSR:
    """Classe représentant un LFSR

    Attributs:
    ---------
    vecteur_init (list[{0,1}]): Vecteur d'initialisation du LFSR
    coefs_retr (list[{0,1}]): Vecteur contenant les coefficients de rétroaction du LFSR
    """

    def __init__(self, vecteur_init: list, coefs_retr: list) -> None:
        """Méthode d'initialisation de la classe LFSR"""

        if len(vecteur_init) != len(coefs_retr):
            raise IndexError(
                "Tailles du VI et des coefficients de rétroaction incompatibles")

        self.sauvegarde = vecteur_init
        self.coefs = coefs_retr
        self.etat = vecteur_init

    def set_etat(self, nouvel_etat):
        """Remplace l'état actuel du LFSR par un nouvel état"""
        self.etat = nouvel_etat

    def get_etat(self, index=None) -> list | int:
        """Retourne l'état entier du LFSR ou seulement le bit à l'index indiqué"""
        if not index == None:
            return self.etat[index]
        else:
            return self.etat

    def get_coefs(self, index=None) -> list | int:
        """Retourne les coeficientss de rétroaction entiers du lfsr ou seulement le bit à l'index indiqué"""
        if not index == None:
            return self.coefs[index]
        else:
            return self.coefs

    def get_taille(self):
        """Retourne la taille du LFSR"""
        return len(self.get_etat())

    def reset(self):
        """Redémarre le LFSR avec son vecteur d'initialisation"""
        self.etat = self.sauvegarde

    def sequence(self, taille_seq):
        """Fonction génératrice de la séquence sortie par le LFSR pour une taille donnée"""

        for _ in range(taille_seq):

            # On renvoie le bit de poids faible
            last = self.get_etat()[-1]
            yield last

            # On fait la somme des produits des états[i] et des coefs[i] du LFSR le tout modulo 2
            last = sum([self.get_coefs(i) * self.get_etat(i)
                       for i in range(self.get_taille())])
            last = last % 2

            # On décale l'état précédent vers la droite et on ajoute le nouveau bit de poids fort
            new_list = self.get_etat()[:-1]
            new_list.insert(0, last)
            self.set_etat(new_list)


class CSS:
    """Classe représentant l'encryptage CSS

    Attributs:
    ---------
    s (list[{0, 1}]): Liste de 0 et 1 de 40 élements
    """

    def __init__(self, s) -> None:
        """Méthode d'initialisation de la classe CSS"""

        if len(s) != 40:
            raise ValueError("Valeur fournie de mauvaise taille")

        # On sépare s en deux morceaux s1 et s2 de tailles 16 et 24
        s1, s2 = str("".join(str(i) for i in s[0:16])), str(
            "".join(str(i) for i in s[16:40]))

        # On initialise les vecteurs des LFSR
        vec_17 = [(1 if i in {14, 0} else 0) for i in range(17)][::-1]
        vec_25 = [(1 if i in {12, 4, 3, 0} else 0) for i in range(25)][::-1]

        # On initialise les LFSR avec 1|s1 et 1|s2 et leurs vecteurs d'initialisation respectifs
        self.lfrs_17 = LFSR([int(i) for i in ("1" + s1)], vec_17)
        self.lfrs_25 = LFSR([int(i) for i in ("1" + s2)], vec_25)

    def reset(self):
        """Redémarre les deux LFSR du CSS avec leurs vecteurs initiaux"""
        self.lfrs_17.reset()
        self.lfrs_25.reset()

    def octet(self):
        """Retourne un octet qui correspond à l'addition d'un octets des deux LFSR"""
        x, y = "", ""
        for i in [i for i in self.lfrs_17.sequence(8)][::-1]:
            x += str(i)
        for j in [i for i in self.lfrs_25.sequence(8)][::-1]:
            y += str(j)
        return int(x, 2) + int(y, 2)

    def encryptage(self, m):
        """Encrypte le message m grâce au Content Scrambling System
        
        Ex:
        --
            css_test = CSS([0 for _ in range(40)])
            message = "0xffffffffff"
            chiffre = css_test.encryptage(message)
            resultat_attendu = "0xffffb66c39"
            print(f"{(True if (resultat_attendu == chiffre) else False)}")
            css_test.reset()
            clair = css_test.encryptage(chiffre)
            print(f"{(True if message == clair else False)}")
        """
        res = ""
        c = 0
        taille = len(m)
        impair = taille % 2

        # Pour tous les nibbles (4bits) deux à deux
        for i in range(2, taille - impair, 2):

            # On concatène les nibbles en un octet binaire
            message_binaire = binaire(16, m[i], m[i + 1])

            # On récupère un octet de clé du CSS
            oct = self.octet()
            octet = (oct + c) % 256

            # On calcule la retenue
            c = 1 if oct > 255 else 0

            # On transforme l'octet obtenu en binaire
            octet_binaire = binaire(10, octet)

            # On XOR l'octet de message et l'octet de clé et on ajoute le résultat au chiffré
            res += xor(message_binaire, octet_binaire)

        # Si la taille du message à encrypter est impaire
        if impair:

            # On récupère le dernier nibble seul
            message_binaire = binaire(16, m[-1])

            # On récupère l'octet de clé
            octet = self.octet()
            octet = (oct + c) % 256
            c = 1 if oct > 255 else 0

            # On ne garde que les 4 premiers bits de l'octet de clé
            octet_binaire = binaire(10, octet)[:4]

            # On XOR les 4 bits de message et les 4 bits de clé et on ajoute le résultat au chiffré
            res += xor(message_binaire, octet_binaire)

        return hex(int(res, 2))

def xor(a,b):
    """Renvoie le xor bit par bit de a et b en binaire
    
    Ex:
    --
    a = 1101, b = 0110
    res = 1 xor 0 | 1 xor 1 | 0 xor 1 | 1 xor 0
        =    1         0         1         1
        la fonction renvoie 1011
    """
    if len(a) != len(b):
        raise IndexError("Tailles différentes")

    res = ""
    for i in range(len(a)):
        res += str((int(a[i]) + int(b[i])) % 2)

    return res


def binaire(*args) -> str:
    """Transforme des chiffres en hexa ou en base 10 en binaire sur 8 bits et les concatènent
    
    Ex:
    --
    *args = (10, 155, 49)
        10 correspond à la base
        en binaire 12 = 10011011 et 49 = 110001 la fonction renvoie: 1001101100110001
    """
    res = ""
    for elem in args[1:]:
        tmp = str(bin(int(str(elem), args[0])))[2:]
        for _ in range((4 if args[0] == 16 else 8 if args[0] == 10 else len(tmp)) - len(tmp)):
            tmp = "0" + tmp
        res += tmp

    return res

def attaque(css: CSS):
    # On récupère les 6 premiers octets du CSS
    css.reset()
    z = [css.octet() for _ in range(6)]
    css.reset()

    # On teste pour toutes les combinaisons de taille 16
    combinaisons = list(itertools.product([0, 1], repeat=16))
    for combi in combinaisons:
        css.reset()
        s1 = [1]
        for i in combi:
            s1.append(i)

        # On crée un LFSR de test avec la combinaison actuelle
        lfsr17_test = LFSR(s1, [(1 if i in {14, 0} else 0) for i in range(17)][::-1])

        y = [0, 0, 0]
        c = 0
        # On récupère 24 bits de sortie du lfsr 17 pour les xor avec les Z
        for i in range(3):
            sequence_test17 = [str(j) for j in lfsr17_test.sequence(8)][::-1]
            seq17_b10 = int("".join(sequence_test17), 2)
            y[i] = (seq17_b10 + z[i] + c) % 256
            c = 1 if (int("".join(sequence_test17), 2) + z[i] + c) > 255 else 0

        # pour chaque Y ainsi obtenu, on test un nouveau css et on compare les resultats
        for index in range(3):
            y[index] = binaire(10, y[index])
        s2 = []

        for i in y:
            for j in i:
                s2.append(int(j))

        s_test = []

        for bit in s1[1:]:
            s_test.append(int(bit))

        for bit in s2:
            s_test.append(int(bit))

        css_test_seq = CSS(s_test)

        c = 0
        comparaison = []
        for _ in range(6):
            octet = css_test_seq.octet()
            oct = (octet + c) % 256
            c = 1 if (octet + c) > 255 else 0
            comparaison.append(oct)
        print(comparaison)

        count = 0
        for i in range(6):
            if z[i] == comparaison[i]:
                count += 1

        if count == 6:
            return "Trouvé"

def test_lfsr(taille):
    # Utilise itertools pour générer toutes les combinaisons possibles pour une taille donnée
    combinaisons = list(itertools.product([0, 1], repeat=taille))

    for combinaison in combinaisons:
        # Si combinaison vaut 0 (= not any), on passe à la prochaine (on ne veut pas montrer que le LFSR fonctionne ou pas avec un vecteur nul, -> 2 (puissance 17) -1 combinaisons possibles)
        if not any(combinaison):
            continue

        # On crée un LFSR avec la combinaison actuelle (les coefficients de rétroaction sont inutilisés pour ce test)
        lfsr = LFSR(list(combinaison), [0]*taille)

        # Pour que la combinaison soit comparable, on la transforme en liste
        combinaison = list(combinaison)

        # Vérification que les tests sont corrects (en ajoutant volontairement une erreur)
        # -> combinaison.append(1)

        # On vérifie que la séquence générée par le LFSR est égale à la combinaison précedemment générée
        assert lfsr.get_etat(
        ) == combinaison, f"Echec à la combinaison : {combinaison}"

    print("\nLFSR : Tous les tests ont été passés avec succès\n")


def test_CSS(m):
    # On crée un objet CSS
    css = CSS([0 for _ in range(40)])

    # On chiffre le message
    c = css.encryptage(m)

    # On réinitialise le CSS
    css.reset()

    # On déchiffre le message
    m1 = css.encryptage(c)

    # On vérifie que le message déchiffré est égal au message initial
    assert m == m1, f"Echec à la comparaison : {m} != {m1}"

    print(f"\nRésultat du CSS validé: {m} -> {c} -> {m1}\n")



if __name__ == "__main__":

    # On teste un LFSR de taille 17
    test_lfsr(22)

    # On teste le chiffremennt CSS
    m = "0xffffffffff"
    test_CSS(m)
    
    # Pas touché à ca
    initialisation = [randint(0, 1) for _ in range(40)]
    print(f"{len(initialisation)}, {initialisation}")
