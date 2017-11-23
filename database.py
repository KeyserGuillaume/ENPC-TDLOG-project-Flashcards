######### stockage en base de donnees. Our database is called FlashCards.db
 #Table existante : LANGUAGES 

import sqlite3
#creation de la base de donnees :
#conn=sqlite3.connect('FlashCards.db')
#conn.execute('''CREATE TABLE LANGUAGES
#      (NAME TEXT PRIMARY KEY      NOT NULL);''')
#conn.close()
       
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
    
    
def addFlashCard(mot, trad, ex, theme, diff, level, image, sound, nature, langue):
    conn=sqlite3.connect('FlashCards.db')
    nextId=getNextId(langue)
    conn.execute("INSERT INTO {} (ID, MOT, TRADUCTION, EXEMPLE, THEME, DIFFICULTE, MAITRISE, ILLUSTRATIONPATH, SOUNDPATH, NATURE, LANGUE) \
         VALUES({}, '{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}')".format(langue.upper(), nextId, mot, trad, ex, theme, diff, level, image, sound, nature, langue.upper()))
    conn.commit()
    conn.close()
    
#addFlashCard("1", "hello", "bonjour", "bonjour toi","salutations",0,10,"vide","vide","jsp","anglais")    
    
def removeFlashCard(language, name):
    conn=sqlite3.connect('FlashCards.db')
    conn.execute("DELETE from {} where id = {};".format(language.upper(), name))
    conn.commit()
    conn.close()
    
def giveNewCardName(language):
    return getNextId(language)
    
def getRandomFlashCard(language):
    return 0 #a coder
    
def motExiste(language, mot):
    return 0#a coder. renvoie false si le mot n'existe pas dans les flashcards, la liste des
            #traductions existantes sinon (car il peut deja y avoir plusieurs flashcards pour ce mot)



