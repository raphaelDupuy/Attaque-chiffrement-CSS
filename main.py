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

            test_list = self.get_etat()[:-1]
            test_list.insert(0, last)
            self.set_etat(test_list)

test_lfsr = LFSR(vecteur_init=[1,0,0,1,0,1,1,0], coefs_retr=[0,0,0,1,1,1,0,0])

if __name__ == "__main__":
    print(f"{[i for i in test_lfsr.sequence(16)]}")