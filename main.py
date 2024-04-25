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

            last += sum([self.get_coefs(i) * self.get_etat(i) for i in range(self.get_taille())])
            last = last % 2

            new_list = self.get_etat()[:-1]
            new_list.insert(0, last)
            self.set_etat(new_list)

class CSS:
    def __init__(self, s) -> None:
        if len(s) != 40:
            raise ValueError("Valeur fournie de mauvaise taille")
        
        s1, s2 = str("".join(str(i) for i in s[0:16])), str("".join(str(i) for i in s[16:40]))
        
        vec_17 = [(1 if i in {14, 0} else 0) for i in range(17)]
        vec_25 = [(1 if i in {12, 4, 3, 0} else 0) for i in range(25)]
        self.lfrs_17 = LFSR([int(i) for i in ("1" + s1)], vec_17)
        self.lfrs_25 = LFSR([int(i) for i in ("1" + s2)], vec_25)

    def octet(self):
        x, y = int(''.join(map(str, [i for i in self.lfrs_17.sequence(8)])), 2), int(''.join(map(str, [i for i in self.lfrs_25.sequence(8)])), 2)
        return x + y
    
    def encryptage(self, m):
        res = ""
        c = 0
        taille = len(m[2:])
        impair = taille % 2
        for i in range(2, taille + 1, 2):
            print(f"res: {res}")
            print(f"bits: {m[i]}, {m[i+1]}")
            message_binaire = str(bin(int(m[i], 16)))[2:] + str(bin(int(m[i + 1], 16)))[2:]

            oct = self.octet()
            octet = (oct + c) % 256
            c = 1 if oct > 255 else 0

            # On fait en sorte que notre keystream tienne sur 8bits
            octet_binaire = ""
            for _ in range(8 - len(bin(octet)[2:])):
                    
                    octet_binaire += "0"
            octet_binaire += str(bin(octet)[2:])
            res += xor(message_binaire, octet_binaire)

        if impair:
            print("impair")
            message_binaire = str(bin(int(m[-1], 16)))[2:]
            
            octet = self.octet()
            octet = (oct + c) % 256
            c = 1 if oct > 255 else 0
            
            # On fait en sorte que notre keystream tienne sur 4bits
            octet_binaire = ""
            for _ in range(4 - len(bin(octet)[6:])):
                    octet_binaire += "0"
            octet_binaire += str(bin(octet)[6:])

            message_binaire = str(bin(int(m[-1], 16)))[2:]
            res += xor(message_binaire, octet_binaire)

        return hex(int(res, 2))

def xor(a,b):
    if len(a) != len(b):
        raise IndexError("Tailles différentes")
    
    
    res = ""
    for i in range(len(a)):
        res += str((int(a[i]) + int(b[i])) % 2)

    return res


if __name__ == "__main__":
    m = "0xfffffffffff"
    test_css = CSS([0 for _ in range(40)])
    print(test_css.encryptage(m))

