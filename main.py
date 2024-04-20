class LFSR:

    def __init__(self, vecteur_init:list, coefs_retr:list):

        self.etat_initial = vecteur_init
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

        for _ in range(taille_seq):
            last = self.get_etat()[-1]
            yield last

            last += sum([self.get_coefs(i) * self.get_etat(i) for i in range(self.get_taille())])
            last = last % 2

            test_list = self.get_etat()[:-1]
            test_list.insert(0, last)
            self.set_etat(test_list)

    def reset(self):
        self.set_etat(self.etat_initial)

test_lfsr = LFSR(vecteur_init=[1,0,0,1,0,1,1,0], coefs_retr=[0,0,0,1,1,1,0,0])


if __name__ == "__main__":
    for i in test_lfsr.sequence(8):
        print(i)