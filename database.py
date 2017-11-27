######### stockage en base de donnees. Our database is called FlashCards.db
 #Table existante : LANGUAGES 

import sqlite3
import flashcard
from random import randint
from scipy.stats import expon
from math import log, exp
#creation de la base de donnees :
#conn=sqlite3.connect('FlashCards.db')
#conn.execute('''CREATE TABLE LANGUAGES
<<<<<<< HEAD
#   (NAME TEXT PRIMARY KEY      NOT NULL);''')
=======
#      (NAME TEXT PRIMARY KEY      NOT NULL);''')
>>>>>>> 2d8f75519b722c2dcfbdbfd7d37be39fc69956d1
#conn.close()

def getALLtables():
    conn=sqlite3.connect('FlashCards.db')
    cursor=conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    result = [row[0] for row in cursor]
    conn.close()
    return result
#return a list of tables' names

def getAllcards(tableName):
    conn=sqlite3.connect('FlashCards.db')
    cursor=conn.execute("SELECT * FROM {}".format(tableName.upper()))
    result = [row[0:10] for row in cursor]
    conn.close()
    return result
#return a list of tuples
    

# ne peut pas modifier le mot et la langue
def modifyCard(tableName, Id, trad, ex, theme, diff, level, image, sound, nature):
    conn=sqlite3.connect('FlashCards.db')
    cursor=conn.execute("UPDATE {} SET TRADUCTION = '{}', EXEMPLE = '{}', THEME = '{}', DIFFICULTE = {}, MAITRISE = {}, ILLUSTRATIONPATH = '{}', SOUNDPATH = '{}', NATURE = '{}' \
                        WHERE ID = {}".format(tableName.upper(), trad, ex, theme, diff, level, image, sound, nature, Id))
    conn.commit()
    conn.close()
#modifyCard('ANGLAIS', 7, 'salut', 'Hello World', 'communication', 0, 10, '', '', 'jsp')



    
def getNextId(tableName):
    conn=sqlite3.connect('FlashCards.db')
    result=1+[x for x in conn.execute("SELECT Count(*) FROM {}".format(tableName.upper()))][0][0] #je sais pas pourquoi ça marche, mais ça marche
    conn.close()
    return result
        
    
# appelee dans createcardsInterf.py
def giveAllLanguages():
    #return ["anglais"]
    conn = sqlite3.connect('FlashCards.db')
    cursor=conn.execute("SELECT name from LANGUAGES")
    result=[row[0] for row in cursor]
    conn.close()
    return result
    
def addLanguage(language):
    conn=sqlite3.connect('FlashCards.db')
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
    conn=sqlite3.connect('FlashCards.db')
    conn.execute("DELETE from LANGUAGES where name = '{}';".format(language.upper()))
    conn.execute('drop table if exists {}'.format(language.upper()))
    conn.commit()
    conn.close()
    
def addCard(mot, trad, ex, theme, diff, level, image, sound, nature, langue):
    conn=sqlite3.connect('FlashCards.db')
    nextId=getNextId(langue)
    conn.execute("INSERT INTO {} (ID, MOT, TRADUCTION, EXEMPLE, THEME, DIFFICULTE, MAITRISE, ILLUSTRATIONPATH, SOUNDPATH, NATURE, LANGUE) \
         VALUES({}, '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}')".format(langue.upper(), nextId, mot, trad, ex, theme, int(diff), int(level), image, sound, nature, langue.upper()))
    conn.commit()
    conn.close()
    
#addFlashCard("1", "hello", "bonjour", "bonjour toi","salutations",0,10,"vide","vide","jsp","anglais") 

def register(flashcard):
    addCard(flashcard.word, flashcard.trad, flashcard.exemple, flashcard.thema, flashcard.howhard, flashcard.level, flashcard.image, flashcard.prononciation, flashcard.nature, flashcard.tablename)
   
def getCardById(language, name):
    conn=sqlite3.connect('FlashCards.db')
    cursor = conn.execute("SELECT * from {} where id = {}".format(language.upper(), name))
    for row in cursor:                        #il ne devrait y avoir qu'une seule row dans cursor
        return flashcard.FlashCards(*row )    #mais je ne sais pas comment le manipuler autrement qu'en le parcourant
    conn.close()
    
def removeCard(language, name):
    conn=sqlite3.connect('FlashCards.db')
    conn.execute("DELETE from {} where id = {};".format(language.upper(), name))
    conn.commit()
    conn.close()
    
def giveNewCardName(language):
    return getNextId(language)
    
def getRandomCard(language):
    n=giveNewCardName(language)
    a=randint(1,n-1)
    return a
    
#returns ids of all cards according to some attribute
def getCardsWithAttribute(language, attributeName, attribute):
    conn = sqlite3.connect('FlashCards.db')
    cursor=conn.execute("SELECT id from {} where {} = '{}'".format(language.upper(), attributeName, attribute))
    result=[row[0] for row in cursor]
    conn.close()
    return result
    
#returns ids of all cards for mot (there may be several, with different translations)
def getCardsWithMot(language, mot):
    return getCardsWithAttribute(language, "mot", mot)

def getCardsWithTraduction(language, traduction):
    return getCardsWithAttribute(language, "traduction", traduction)
    
def existeSameCard(language,mot,traduction):
    conn = sqlite3.connect('FlashCards.db')
    #sql = "select count(*) from {} where mot = '{}' and traduction = '{}';".format(language.upper(),mot,traduction)
    cursor = conn.execute("select count(*) from {} where mot = '{}' and traduction = '{}'".format(language.upper(),mot,traduction))
    result = cursor.fetchone()[0]
    conn.close()
    if result:
        return True #existe une carte meme
    else:
        return False #existe pas une carte meme


