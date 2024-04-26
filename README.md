# Attaque-chiffrement-CSS
Programme d'attaque contre le chiffrement à flot CSS et réponses à certaines questions théoriques dans le cadre d'un devoir maison pour l'UE Cryptographie (LSIN603)


# Tests

1. ### LSFR
    Une fonction de test test_lfsr(taille) permet de tester un LSFR d'une taille donnée. Son déroulement est entièrement commenté et expliqué.\
    Ce test est basé sur une classe LSFR. On a besoin d'un vecteur d'initialisation et des coéfficients de rétroaction pour initialiser un objet.
2. ### CSS
    Une fonction de test test_CSS(m) permet de tester un chiffrement et un déchiffrement d'un texte avec CSS. Le message doit être entré en argument de la fonction. Son déroulement est lui aussi entièrement commenté et expliqué.\
    Ce test est basé sur une classe CSS, un objet etant initialisé avec une liste de 40 éléments représentants la clé, séparé ensuite en deux pour les deux LSFR de taille 16 et 24.
3. ### Attaque contre CSS
