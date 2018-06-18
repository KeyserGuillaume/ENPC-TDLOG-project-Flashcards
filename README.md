# ENPC-TDLOG-project-Flashcards
**Creating a simple, comprehensive program to constitute a flashcard library and provide tools to learn vocabulary interactively**

Le projet propose de munir l'utilisateur d'une (de) base(s) de données de flashcards, et d'interfaces pour naviguer (accueil, parcours,lecture), pour gérer (ajout, modification, recherche), pour jouer (jeux drag and drop, memory, hotcol,...), ainsi que de paramètres sur ses préférences d'uitlisation.

L'application telle quelle requiert l'installation de python3 et des modules sqlite et pyqt5
L'application sera lancée à l'éxécution de main.py

### Description of the repository content

_Les fichiers clés de ce projet sont à ce jour _ :

* README.md : description du projet, des données, des méthodes
* __main.py__ : lancement de l'application python
* __FlaschCards.db__ : la base de donnée
* model.flaschcards.py : la definition de la classe flaschcards, et sa méthode d'affichage. Son but est de constituer un niveau d'abstraction entre interface et base de donnée
* __model.database.py__ : les fonctions de recherche/ajout/modification relatives à nos bases de données (langues + cartes par langue)
* model.rechercheFonct.py : les fonctions de recherche flou ou non a partir des demandes reçues
* controller.AccessSettings.py et controller.AppSettings.xml : gestion, stockage et accès des paramètre utilisateurs
* web et app.py : elements de consertion  du projet vers une appli web, fournis par Hicham Dakhli
* __view.interfaccueil.py__ : la definition de l'interface d'accueil (qui s'affichera a l'ouverture de l'application) ; cliquer sur le bouton NewCard ouvre l'interface de creation de nouvelles cartes ; cliquer sur le bouton Modify ouvre l'interface de modification d'une carte au hasard dans la base de donnée ; cliquer sur les mots de la bande gauche ouvre une interface de lecture sur l'échantillon ; cliquer sur Search ouvre  l'interface de recherche ; cliquer sur les dossiers ouvre  l'interface de parcours associée ; cliquer sur les icones de jeux ouvre une partie
* view.createcardsInterf.py : la definition de l'interface de creation de flash cards et par héritage de celle de modification d'une carte tirée une carte au hasard ou donnée ; cliquer sur create ou modify enregistre la carte ou les changements dans la base de donnée FlashCards.db
* view.icons : fichier image and conversion en fichier de ressources pour les diverses iconnes et fonds des interfaces
* view.parcours.py : la definition de l'interface de parcours pour l'ensemble des langues (affichage de dossiers), pour les jeux (affichage d'icones), pour les flash cards (cartes)
* view.rechercheInterf.py : interface de recherche
* view.viewCard.py : affichage de lecture de FlashCards i.e. affiche sur joli fonds une carte qui se retourne avec les infos interessantes et des fleches pour aller de l'une a l'autre + sur la carte bouton pour la modifier, ou ecouter le son
* view.settingsInterf.py : interface d'ajustement des paramètres utilisateurs
* view.games.gameWindow.py : interface de jeu - fenetre global avec chrono et décompte d'erreurs
* view.games.dragAndDrop.py ; view.games.hotColdGame.py ; view.games.memory.py ; view.games.pointToCard.py ; view.games.vraiOuFaux.py : interface et fonctionnement des 5 jeux d'apprentissage du projet

### Further possibilites

_Nous indiquons ici les développements potentiels que nous avons identifié _ :

* recherche de son et images sur internet sur don du mot ou de la traduction voire d'un attibut moins déterminant (example)
* recherche dans des batabases extérieures de tous les composants d'une nouvelle carte d'après le mot (ou un attibut moins déterminant)



