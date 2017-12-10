############# definition des fonctions de recherche

import flashcard, database


def recherche(langue, mot, theme, tra, phrase, floue):
    resultat = []
    langues = database.giveAllLanguages()
    if floue == False:
        if langue.strip() == 'TOUTES':
            for item in langues:
                resultat.extend(recherche_one(item, mot, theme, tra, phrase))
        else:
            resultat.extend(recherche_one(langue, mot, theme, tra, phrase))
    elif floue == True:
        mots = floue_mot(mot)
        if langue.strip() == 'TOUTES':
            for item in langues:
                for item_mot in mots:
                    resultat.extend(recherche_one(item, item_mot, theme, tra, phrase))
            else:
                for item_mot in mots:
                    resultat.extend(recherche_one(langue, item_mot, theme, tra, phrase))
    return resultat
            
        


def recherche_one(langue, mot, theme, tra, phrase):
    resultat = []
    resultat_id = []
    id_temp = []
    if mot.strip() == '' and theme.strip() == '' and tra.strip() == '' and phrase.strip() == '':
        resultat.extend(database.getAllCards(langue))
    else:
        if mot.strip():
            id_temp.append(database.getCardsWithAttribute(langue.upper(), 'MOT', mot.strip()))
        if theme.strip():
            id_temp.append(database.getCardsWithAttribute(langue.upper(), 'THEME', theme.strip()))
        if tra.strip():
            id_temp.append(database.getCardsWithAttribute(langue.upper(), 'TRADUCTION', tra.strip()))
        if phrase.strip():
            id_temp.append(database.getCardsWithAttribute(langue.upper(), 'EXEMPLE', phrase.strip()))
        flag = 1
        for item in id_temp:
            if len(item) == 0:
                flag = 0
                break
        if flag == 1:
            for item1 in id_temp[0]:
                flag1 = 1
                for k in range(1,len(id_temp)):
                    if item1 not in id_temp[k]:
                        flag1 = 0
                        break
                if flag1 == 1:
                    resultat_id.append(item1)
            for i in resultat_id:
                resultat.append(database.getCardById(langue, i))
    return resultat

def floue_mot(mot):
    list_mot = []
    return list_mot
               
                
            
            
            
            
            
            