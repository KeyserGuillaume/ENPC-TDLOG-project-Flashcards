# -*- coding: utf-8 -*-
import sqlite3
#faire le lien a bade de donnees "Flashcards,db" et renvoyer la connection
def connDB():
    conn = sqlite3.connect('FlashCards.db')
    return conn