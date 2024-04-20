import itertools
from main import LFSR


def test_lfsr17():
    # Utilise itertools pour générer toutes les combinaisons possibles pour une taille 17
    combinaisons = list(itertools.product([0, 1], repeat=17))

    for combinaison in combinaisons:
        # Si combinaison vaut 0 (= not any), on passe à la prochaine (on ne veut pas montrer que le LFSR fonctionne ou pas avec un vecteur nul, -> 2 (puissance 17) -1 combinaisons possibles)
        if not any(combinaison):
            continue
        
        # On crée un LFSR avec la combinaison actuelle (les coefficients de rétroaction sont inutilisés pour ce test)
        lfsr = LFSR(list(combinaison), [0]*17)
    
        # Pour que la combinaison soit comparable, on la transforme en liste
        combinaison = list(combinaison)

        #Vérification que les tests sont corrects (en ajoutant volontairement une erreur)
        # -> combinaison.append(1)

        # On vérifie que la séquence générée par le LFSR est égale à la combinaison précedemment générée
        assert lfsr.get_etat() == combinaison, f"Echec à la combinaison : {combinaison}"

