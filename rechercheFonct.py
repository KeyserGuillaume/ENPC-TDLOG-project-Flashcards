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
        if langue.strip() == 'TOUTES':
            for item in langues:
                mots = floue_mot_rapide(item, mot)
                for item_mot in mots:
                    resultat.extend(recherche_one(item, item_mot, theme, tra, phrase))
        else:
            mots = floue_mot_rapide(item, mot)
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

#voir les pages wikipedia Distance De Levenshtein et Distance De Damerau Levenshtein
def DistanceDeDamerauLevenshtein(chaine1, chaine2):
    l1=len(chaine1)
    l2=len(chaine2)
    d=[[0 for j in range(l2+1)]for i in range(l1+1)]
    for i in range(l1+1):
       d[i][0]=i
    for j in range(l2+1):
       d[0][j]=j

    for i in range(l1):
        for j in range(l2):
            if (chaine1[i]==chaine2[j]):
                coutSubstitution = 0
            else:
                coutSubstitution = 1
            d[i+1][j+1]=min(d[i][j+1]+1, d[i+1][j]+1, d[i][j]+coutSubstitution)
            if (i>0 and j>0 and chaine1[i]==chaine2[j-1] and chaine1[i-1]==chaine2[j]):
                d[i+1] [j+1]=min(d[i+1][j+1], d[i-1][j-1]+coutSubstitution)
    return (d[l1][l2])
 

def floue_mot_rapide(langue, mot):
    list_mot = []
    for card in database.getAllCards(langue):
        if DistanceDeDamerauLevenshtein(card.word, mot) < 3:
            list_mot.append(card.word)
    return list_mot
               
               
            
            
            
            
            
            