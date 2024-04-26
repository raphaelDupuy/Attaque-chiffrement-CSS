from random import randint

class LFSR:
    """Classe représentant un LFSR

    Attributs:
    ---------
    vecteur_init (list[{0,1}]): Vecteur d'initialisation du LFSR
    coefs_retr (list[{0,1}]): Vecteur contenant les coefficients de rétroaction du LFSR
    """

    def __init__(self, vecteur_init:list, coefs_retr:list) -> None:
        """Méthode d'initialisation de la classe LFSR"""

        if len(vecteur_init) != len(coefs_retr):
            raise IndexError("Tailles du VI et des coefficients de rétroaction incompatibles")
        
        self.sauvegarde = vecteur_init
        self.coefs = coefs_retr
        self.etat = vecteur_init

    def set_etat(self, nouvel_etat):
        """Remplace l'état actuel du LFSR par un nouvel état"""
        self.etat = nouvel_etat

    def get_etat(self, index=None) -> list|int:
        """Retourne l'état entier du LFSR ou seulement le bit à l'index indiqué"""
        if not index == None:
            return self.etat[index]
        else:
            return self.etat
    
    def get_coefs(self, index=None) -> list|int:
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
            last = sum([self.get_coefs(i) * self.get_etat(i) for i in range(self.get_taille())])
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
        s1, s2 = str("".join(str(i) for i in s[0:16])), str("".join(str(i) for i in s[16:40]))
        
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
        print(f"x: {x} - {int(x, 2)}, y: {y} - {int(y, 2)}")
        return int(x, 2) + int(y, 2)

    def encryptage(self, m):
        """Encrypte le message m grâce au Content Scrambling System"""
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
    """Renvoie l'addition de a et b modulo 2"""
    if len(a) != len(b):
        raise IndexError("Tailles différentes")

    res = ""
    for i in range(len(a)):
        res += str((int(a[i]) + int(b[i])) % 2)

    return res

def binaire(*args) -> str:
    """Transforme des chiffres en hexa ou en base 10 en binaire sur 4 bits et les concatènent"""
    res = ""
    for elem in args[1:]:
        tmp = str(bin(int(str(elem), args[0])))[2:]
        for _ in range((4 if args[0] == 16 else 8 if args[0] == 10 else len(tmp)) - len(tmp)):
            tmp = "0" + tmp
        res += tmp

    return res

if __name__ == "__main__":

    m = "0xfffffffffff"
    test_css = CSS([0 for _ in range(40)])
    c = test_css.encryptage(m)
    test_css.reset()
    m1 = test_css.encryptage(c)
    print(f"{m} -> {c} -> {m1}")

    initialisation = [randint(0, 1) for _ in range(40)]
    print(f"{len(initialisation)}, {initialisation}")
