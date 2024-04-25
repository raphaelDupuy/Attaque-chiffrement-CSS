class LFSR:
    """Classe représentant un LFSR

    Attributs:
    ---------
    vecteur_init (list[{0,1}]): Vecteur d'initialisation du LFSR
    coefs_retr (list[{0,1}]): Vecteur contenant les coefficients de rétroaction du LFSR
    """

    def __init__(self, vecteur_init:list, coefs_retr:list) -> None:
        """Fonction d'initialisation de la classe LFSR"""

        if len(vecteur_init) != len(coefs_retr):
            raise IndexError("Tailles du VI et des coefficients de rétroaction incompatibles")
        
        self.coefs = coefs_retr
        self.etat = vecteur_init

    def set_etat(self, nouvel_etat):
        self.etat = nouvel_etat

    def get_etat(self, index=None) -> list|int:
        if not index == None:
            return self.etat[index]
        else:
            return self.etat
    
    def get_coefs(self, index=None) -> list|int:
        if not index == None:
            return self.coefs[index]        
        else:
            return self.coefs
    
    def get_taille(self):
        return len(self.get_etat())

    def sequence(self, taille_seq):
        """Fonction génératrice de la séquence sortie par le LFSR pour une taille donnée"""

        for _ in range(taille_seq):
            last = self.get_etat()[-1]
            yield last

            last = sum([self.get_coefs(i) * self.get_etat(i) for i in range(self.get_taille())])
            last = last % 2

            new_list = self.get_etat()[:-1]
            new_list.insert(0, last)
            self.set_etat(new_list)

class CSS:
    def __init__(self, s) -> None:
        if len(s) != 40:
            raise ValueError("Valeur fournie de mauvaise taille")
        
        s1, s2 = str("".join(str(i) for i in s[0:16])), str("".join(str(i) for i in s[16:40]))
        
        vec_17 = [(1 if i in {14, 0} else 0) for i in range(17)][::-1]
        vec_25 = [(1 if i in {12, 4, 3, 0} else 0) for i in range(25)][::-1]
        self.lfrs_17 = LFSR([int(i) for i in ("1" + s1)], vec_17)
        self.lfrs_25 = LFSR([int(i) for i in ("1" + s2)], vec_25)

    def octet(self):
        x, y = "", ""
        for i in [i for i in self.lfrs_17.sequence(8)][::-1]:
            x += str(i)
        for j in [i for i in self.lfrs_25.sequence(8)][::-1]:
            y += str(j)
        print(f"x: {x} - {int(x, 2)}, y: {y} - {int(y, 2)}")
        return int(x, 2) + int(y, 2)

    def encryptage(self, m):
        res = ""
        c = 0
        taille = len(m)
        impair = taille % 2
        print(m)
        for i in range(2, taille - impair, 2):
            message_binaire = binaire(16, m[i], m[i + 1])

            oct = self.octet()
            octet = (oct + c) % 256
            c = 1 if oct > 255 else 0

            octet_binaire = binaire(10, octet)

            res += xor(message_binaire, octet_binaire)

        if impair:
            print("impair")
            message_binaire = binaire(16, m[-1])
            
            octet = self.octet()
            octet = (oct + c) % 256
            c = 1 if oct > 255 else 0
            
            octet_binaire = binaire(10, octet)[:4]

            res += xor(message_binaire, octet_binaire)

        return hex(int(res, 2))

def xor(a,b):
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
    print(test_css.encryptage(m))
