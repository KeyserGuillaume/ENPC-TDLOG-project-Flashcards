######### stockage en base de donnees. Our database is called FlashCards.db
 #Table existante : LANGUAGES

import sqlite3
import os
import flashcard
from random import randint
from scipy.stats import expon
from math import log, exp
from connDB import connDB
#creation de la base de donnees :
#conn=sqlite3.connect('FlashCards.db')
#conn.execute('''CREATE TABLE LANGUAGES
#      (NAME TEXT PRIMARY KEY      NOT NULL);''')
#conn.close()



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
#modifyCard('ANGLAIS', 7, 'salut', 'Hello World', 'communication', 0, 10, '', '', 'jsp')




def getNextId(tableName):
    conn=connDB()
    a=[x for x in conn.execute("SELECT max(ID) FROM {}".format(tableName.upper()))][0][0]
    if (a):
        result=1+a
    else:
        result=1
    conn.close()
    return result


# appelee dans createcardsInterf.py
# appelee dans rechercheInterf.py
## appelee dans rechercheFonct.py
def giveAllLanguages():
    #return ["anglais"]
    conn=connDB()
    cursor=conn.execute("SELECT name from LANGUAGES")
    result=[row[0] for row in cursor]
    conn.close()
    return result

def existsLanguage(language):
    conn=connDB()
    cursor = conn.execute("select count(*) from LANGUAGES where name = '{}'".format(language.upper()))
    result = cursor.fetchone()[0]
    conn.close()
    if result:
        return True
    else:
        return False

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

#addFlashCard("1", "hello", "bonjour", "bonjour toi","salutations",0,10,"vide","vide","jsp","anglais")

def register(flashcard):
    addCard(flashcard.word, flashcard.trad, flashcard.exemple, flashcard.thema, flashcard.howhard, flashcard.level, flashcard.image, flashcard.prononciation, flashcard.nature, flashcard.tablename)

## appelee dans rechercheFonct.py
def getCardById(language, name):
    conn=connDB()
    cursor = conn.execute("SELECT * from {} where id = {}".format(language.upper(), name))
    for row in cursor:                        #il ne devrait y avoir qu'une seule row dans cursor
        return flashcard.FlashCards(*row )    #mais je ne sais pas comment le manipuler autrement qu'en le parcourant
    conn.close()

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
    conn.execute("DELETE from {} where id = {};".format(language.upper(), name))
    conn.commit()
    conn.close()

def giveNewCardName(language):
    return getNextId(language)

def getRandomCard(language):
    cardList=getAllCards(language)
    n=len(cardList)
    a=randint(1,n-1)
    return cardList[a].name
    
def removeLastCard(language):
    removeCard(language, getNextId(language)-1)

##appelee dans rechercheFonct.py
#returns ids of all cards according to some attribute
def getCardsWithAttribute(language, attributeName, attribute):
    conn=connDB()
    cursor=conn.execute("SELECT id from {} where {} = '{}'".format(language.upper(), attributeName, attribute))
    result=[row[0] for row in cursor]
    conn.close()
    return result

## retourne la flash Card complete selon le critere d'egalite donne
def getCompleteCardsWithAttribute(language, attributeName, attribute):
    result = []
    conn=connDB()
    cursor=conn.execute("SELECT * from {} where {} = '{}'".format(language.upper(), attributeName, attribute))
    for row in cursor:
        result.append(flashcard.FlashCards(*row))
    conn.close()
    return result

#returns ids of all cards for mot (there may be several, with different translations)
def getCardsWithMot(language, mot):
    return getCardsWithAttribute(language, "mot", mot)

def getCardsWithTraduction(language, traduction):
    return getCardsWithAttribute(language, "traduction", traduction)

def existeSameCard(language,mot,traduction):
    conn=connDB()
    #sql = "select count(*) from {} where mot = '{}' and traduction = '{}';".format(language.upper(),mot,traduction)
    cursor = conn.execute("select count(*) from '{}' where mot = ? and traduction = ? ".format(language.upper()),(mot,traduction))
    result = cursor.fetchone()[0]
    conn.close()
    if result:
        return True #existe une carte meme
    else:
        return False #existe pas une carte meme

#create a table of picture
def create_picturetable():
    conn=connDB()
    sql = "create table IF NOT EXISTS PICTURES(p_id INTEGER PRIMARY KEY AUTOINCREMENT,picture BLOB,type TEXT,file_name TEXT);"
    conn.execute(sql)
    conn.close()

#insert into the table one picture with its name
def insert_picture(picture_file):
    with open(picture_file,'rb') as input_file:
        ablob = input_file.read()
        base = os.path.basename(picture_file)
        afile,ext  = os.path.splitext(base)
        sql = "INSERT INTO PICTURES(picture, type, file_name) VALUES(?, ?, ?);"
        conn=connDB()
        conn.execute(sql,[sqlite3.Binary(ablob),ext,afile])
        conn.commit()
        conn.close()

#extract a picture with its id, returns the name of the picture
def extract_picture(p_id):
    sql = "SELECT picture,type,file_name FROM PICTURES where p_id = :id;"
    p_id = {'id':p_id}
    conn=connDB()
    pic = conn.execute(sql,p_id)
    ablob, ext, afile = pic.fetchone()
    filename = './PICTURES/' + afile + ext
    with open(filename,'wb') as output_file:
        output_file.write(ablob)
    return filename

#create a db of audio
def create_audiotable():
    conn=connDB()
    sql = "create table IF NOT EXISTS AUDIOS(a_id INTEGER PRIMARY KEY AUTOINCREMENT,audio BLOB,type TEXT,file_name TEXT);"
    conn.execute(sql)
    conn.close()

#insert into the table one audio with its name
def insert_audio(audio_file):
    with open(audio_file,'rb') as input_file:
        ablob = input_file.read()
        base = os.path.basename(audio_file)
        afile,ext  = os.path.splitext(base)
        sql = "INSERT INTO AUDIOS(audio, type, file_name) VALUES(?, ?, ?);"
        conn=connDB()
        conn.execute(sql,[sqlite3.Binary(ablob),ext,afile])
        conn.commit()
        conn.close()

#extract a picture with its id, returns the name of the picture
def extract_audio(a_id):
    sql = "SELECT audio,type,file_name FROM AUDIOS where a_id = :id;"
    a_id = {'id':a_id}
    conn=connDB()
    aud = conn.execute(sql,a_id)
    ablob, ext, afile = aud.fetchone()
    filename = './AUDIOS/' + afile + ext
    with open(filename,'wb') as output_file:
        output_file.write(ablob)
    return filename