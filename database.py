######### stockage en base de donnees. Our database is called FlashCards.db
 #Table existante : LANGUAGES 
## fonction d'ajout d'une carte a une table demandee NomLangue (ex : Anglais)
# verification : une carte existe-t-elle deja ?

# a remplir en gardant le nom ou modifier partout
# appelee dans createcardsInterf.py
import sqlite3

#conn.execute('''CREATE TABLE LANGUAGES
#      (ID INT PRIMARY KEY      NOT NULL,
#       NAME           TEXT     NOT NULL);''')
       
def getNextId(tableName):
    return 1+conn.execute("SELECT Count(*) FROM {}".format(tableName.upper()))
    
# appelee dans createcardsInterf.py
def giveAllLanguages():
    return ["anglais"]
    conn = sqlite3.connect('FlashCards.db')
    cursor=conn.execute("SELECT name from LANGUAGES")
    result=[row[0] for row in cursor]
    conn.close()
    return result
    
def addLanguage(language):
    conn=sqlite3.connect('FlashCards.db')
    nextId=getNextId("LANGUAGES")
    conn.execute("INSERT INTO LANGUAGES (ID, NAME) \
        VALUES ({}, {})".format(nextId, language.upper()))
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
    conn.close()
           
def removeLanguage(language):
    return 0#a coder
    
def addFlashCard(name, mot, trad, ex, theme, diff, level, image, sound, nature, langue):
    conn=sqlite3.connect('FlashCards.db')
    nextId=getNextId(langue)
    conn.execute("INSERT INTO {} (ID, MOT, TRADUCTION, EXEMPLE, THEME, DIFFICULTE, MAITRISE, ILLUSTRATIONPATH, SOUNDPATH, NATURE, LANGUE) \
         VALUES({},{},{},{},{},{},{},{},{},{},{})".format(langue.upper(), name, mot, trad, ex, theme, diff, level, image, sound, nature, langue))
    conn.close()
    
def removeFlashCard(mot):
    return 0#a coder
    
def giveNewCardName(language):
    return getNextId(language)
    






