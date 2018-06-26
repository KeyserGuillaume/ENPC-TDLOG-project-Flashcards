######### stockage en base de donnees. Our database is called FlashCards.db
 #Table existante : LANGUAGES

from random import randint
from model import flashcard, soundAPI, imageAPI
from model.connDB import connDB
from numpy import argmax

def getALLtables():
    conn=connDB()
    cursor=conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    result = [row[0] for row in cursor]
    conn.close()
    return result
#return a list of tables' names

## appelee dans rechercheFonct.py
def getAllCards(language):
    result = []
    conn=connDB()
    cursor=conn.execute("SELECT * FROM {}".format(language.upper()))
    for row in cursor:                        
        result.append(flashcard.FlashCards(*row ))
    conn.close()
    return result


# ne peut pas modifier le mot et la langue
def modifyCard(tableName, Id, trad, ex, theme, diff, level, image, sound, nature):
    conn=connDB()
    cursor=conn.execute("UPDATE '{}' SET TRADUCTION = ?, EXEMPLE = ?, THEME = ? ,DIFFICULTE = ? , MAITRISE = ? , ILLUSTRATIONPATH = ? , SOUNDPATH = ? , NATURE = ? WHERE ID = ? ".format(tableName.upper()), 
    (trad, ex, theme, diff, level, image, sound, nature, Id))
    conn.commit()
    conn.close()

def getNextId(tableName):
    conn=connDB()
    a=[x for x in conn.execute("SELECT max(ID) FROM {}".format(tableName.upper()))][0][0]
    if (a):
        result=1+a
    else:
        result=1
    conn.close()
    return result

def giveAllLanguages():
    conn=connDB()
    cursor=conn.execute("SELECT name from LANGUAGES")
    result=[row[0] for row in cursor]
    conn.close()
    return result

def existsLanguage(language):
    conn=connDB()
    cursor = conn.execute("select count(*) from LANGUAGES where name = '{}'".format(language.upper()))
    result = cursor.fetchone()[0]
    if result:
        return True
    else:
        return False

def countLanguage(language):
    conn=connDB()
    cursor = conn.execute("select count(*) from '{}'".format(language.upper()))
    result = cursor.fetchone()[0]
    conn.close()
    return result

def addLanguage(language):
    conn=connDB()
    conn.execute("INSERT INTO LANGUAGES (NAME) \
        VALUES ('{}')".format(language.upper()))
    conn.execute('''CREATE TABLE {}
          (ID INT PRIMARY KEY     NOT NULL,
           MOT TEXT NOT NULL,
           TRADUCTION TEXT NOT NULL,
           EXEMPLE TEXT,
           THEME TEXT,
           DIFFICULTE INT,
           MAITRISE INT,
           ILLUSTRATIONPATH TEXT,
           SOUNDPATH TEXT,
           NATURE TEXT,
           LANGUE TEXT      NOT NULL);'''.format(language.upper()))
    conn.commit()
    conn.close()

def removeLanguage(language):
    conn=connDB()
    allCards=getAllCards(language)
    for card in allCards:
        soundAPI.deleteAudio(card.pronounciation)
    conn.execute("DELETE from LANGUAGES where name = '{}';".format(language.upper()))
    conn.execute('drop table if exists {}'.format(language.upper()))
    conn.commit()
    conn.close()

def addCard(mot, trad, ex, theme, diff, level, image, sound, nature, langue):
    conn=connDB()
    nextId=getNextId(langue)
    conn.execute("INSERT INTO {} (ID, MOT, TRADUCTION, EXEMPLE, THEME, DIFFICULTE, MAITRISE, ILLUSTRATIONPATH, SOUNDPATH, NATURE, LANGUE) \
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ".format(langue.upper()), 
    (nextId, mot, trad, ex, theme, diff, level, image, sound, nature, langue.upper()))
    conn.commit()
    conn.close()

def register(flashcard):
    addCard(flashcard.word, flashcard.trad, flashcard.exemple, flashcard.thema, flashcard.howhard, flashcard.level, flashcard.image, flashcard.pronounciation, flashcard.nature, flashcard.tablename)


def getCardById(language, name):
    conn=connDB()
    cursor = conn.execute("SELECT * from {} where id = {}".format(language.upper(), name))
    for row in cursor:
        return flashcard.FlashCards(*row )
    conn.close()
    
def updateCards(cardList):
    newCardList=[]
    for i in range(len(cardList)):
        newCard=getCardById(cardList[i].tablename, cardList[i].name)
        if newCard!=None:
            newCardList.append(newCard)
    return newCardList

## donne les cartes avec givenleveldown <= maitrise <= givenlevelup
def getCardsToLearn(language, givenleveldown, givenlevelup):
    result = []
    conn = connDB()
    cursor = conn.execute("SELECT * from {} where MAITRISE <= {} and MAITRISE >= {}".format(language.upper(), givenlevelup, givenleveldown))
    for row in cursor:
        result.append(flashcard.FlashCards(*row))
    conn.close()
    return result

def removeCard(language, name):
    conn=connDB()
    myCard=getCardById(language, name)
    soundAPI.deleteAudio(myCard.pronounciation)
    imageAPI.deleteImage(myCard.image)
    conn.execute("DELETE from {} where id = {};".format(language.upper(), name))
    conn.commit()
    conn.close()

def giveNewCardName(language):
    return getNextId(language)

def getRandomCard(language):
    cardList=getAllCards(language)
    n=len(cardList)
    a=randint(1,n-1)
    return cardList[a]
    
def removeLastCard(language):
    removeCard(language, getNextId(language)-1)

##appelee dans rechercheFonct.py
#returns ids of all cards according to some attribute
def getCardsWithAttribute(language, attributeName, attribute):
    conn=connDB()
    cursor=conn.execute("""SELECT id from {} where {} = "{}" """.format(language.upper(), attributeName, attribute))
    result=[row[0] for row in cursor]
    conn.close()
    return result

## retourne la flash Card complete selon le critere d'egalite donne
def getCompleteCardsWithAttribute(language, attributeName, attribute):
    result = []
    conn=connDB()
    cursor=conn.execute("""SELECT * from {} where {} = "{}" """.format(language.upper(), attributeName, attribute))
    for row in cursor:
        result.append(flashcard.FlashCards(*row))
    conn.close()
    return result

#returns ids of all cards for mot (there may be several, with different translations)
def getCardsWithMot(language, mot):
    return getCardsWithAttribute(language, "mot", mot)

def getCardsWithTraduction(language, traduction):
    return getCardsWithAttribute(language, "traduction", traduction)
    
def getSoundFileName(language, cardId):
    card = getCompleteCardWithAttribute(language, "ID", cardId)
    return card.pronounciation

def existsSameCard(language,mot,traduction):
    conn=connDB()
    #sql = "select count(*) from {} where mot = '{}' and traduction = '{}';".format(language.upper(),mot,traduction)
    cursor = conn.execute("select count(*) from '{}' where mot = ? and traduction = ? ".format(language.upper()),(mot,traduction))
    result = cursor.fetchone()[0]
    conn.close()
    if result:
        return True #existe une carte meme
    else:
        return False #existe pas une carte meme

#### match (meme carte) entre mot et trad dans cet ordre
def match(text1, text2, language):
    answer = False
    matching = getCompleteCardsWithAttribute(language, 'mot', text1)
    for card in matching:
        answer = answer or (text2==card.trad)
    return answer

def matchApprox(text1, text2, language):
    """
    We assume that text1 can be incomplete or incorrect whether text2 is either
    a word or a trad in the database and we return True if text1 is approximately
    the pendant of text2 (approx. in the sense "envoyer" is the same as
    "envoyer (qq)").
    So if text2 is " بعث"  and text1 is "envoyer", since "envoyer" is a good
    enough approximation of "envoyer (qq)", we return True.
    """
    answer = False
    matching_word = getCompleteCardsWithAttribute(language, 'mot', text2)
    matching_trad = getCompleteCardsWithAttribute(language, 'traduction', text2)
    text1 = ''.join(i for i in text1 if ord(i)<128)
    # assumes text1 is ASCII, no accent... improve ?
    # pb with l'époque -> l'poque
    # remove accents and replace punctuation with " " ?
    print(text1)
    text1_bits = text1.split()
    if len(text1_bits)==0:
        return False
    text1_main = text1_bits[argmax([len(bit) for bit in text1_bits])]
    print(text1_main)
    for card in matching_word:
        answer = answer or (True in [(text1_main==''.join(i for i in bit if ord(i)<128)) for bit in card.trad.split() if len(bit) > 2])
    for card in matching_trad:
        answer = answer or (True in [(text1_main==''.join(i for i in bit if ord(i)<128)) for bit in card.word.split() if len(bit) > 2])
    answer = answer or match(text1, text2, language) or match(text2, text1, language)
    return answer