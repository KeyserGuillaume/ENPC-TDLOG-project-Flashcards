############# definition des fonctions de recherche

import flashcard, database


def recherche(floue, condt1, condtV1, etou1, condt2, condtV2, etou2, condt3, condtV3, etou3, condt4, condtV4):
    temp = database.getCardsWithMot(condtV2, condtV1)
    return temp