# ENPC-TDLOG-project-Flashcards
**Creating a simple, comprehensive program to constitute a flashcard library and provide tools to learn vocabulary interactively**

Le projet se propose de munir l'utilisateur d'une (de) base(s) de données de flashcards, et d'interfaces pour naviguer (accueil, parcours,lecture), pour gérer (ajout, modification, recherche), pour jouer (jeux drag and drop, ...) 

### Description of the repository content

_Ce projet contient à ce jour les fichiers suivants_ :

* README.md : description du projet, des données, des méthodes
* flaschcards.py : la definition de la classe flaschcards, et sa méthode d'affichage. Son but est de constituer un niveau d'abstraction entre interface et base de donnée
* createcards.ui et interf_create.py : le resultat du travail d'esquisse de l'interface sur QtDesigner ; il sera inutile de les conserver sur le long terme = à supprimer
* __createcardsInterf.py__ : la definition de l'interface de creation de flash cards et par héritage de celle de modification d'une carte tirée une carte au hasard ou donnée ; cliquer sur create ou modify enregistre la carte ou les changements dans la base de donnée FlashCards.db 
* __interfaccueil.py__ : la definition de l'interface d'accueil (qui s'affichera a l'ouverture de l'application) ; cliquer sur le bouton NewCard ouvre l'interface de creation de nouvelles cartes ; cliquer sur le bouton Modify ouvre l'interface de modification d'une carte au hasard dans la base de donnée ; cliquer sur les mots de la bande gauche ouvre une interface de lecture sur l'échantillon ; cliquer sur Search ouvre  l'interface de recherche ; cliquer sur les dossiers ouvre  l'interface de parcours associée ; cliquer sur les icones de jeux ouvre une partie
* __database.py__ : les fonctions de recherche/ajout/modification relatives à nos bases de données (langues + cartes par langue)
* __FlaschCards.db__ : la base de donnée 
* /icons : fichier image and conversion en fichier de ressources pour les diverses iconnes et fonds des interfaces
* /web et app.py : element de consertion vers une appli web
* __parcours.py__ : la definition de l'interface de parcours pour l'ensemble des langues (affichage de dossiers), pour les jeux (affichage d'icones), pour les flash cards (cartes)
* rechercheFonct.py et rechercheInterf.py : interface et fonctions de recherche
* __viewCard.py__ : affichage de lecture de FlashCards i.e. affiche sur joli fonds une carte qui se retourne avec les infos interessantes et des fleches pour aller de l'une a l'autre + sur la carte bouton pour la modifier, ou ecouter le son
* ... (a completer)

### What is coming

* ajout d'une barre de scrolling dans les interface de parcours a venir
* mise a jour des modifications en temps réel dans les interfaces de parcours et lectures
* access du son et des images depuis la lecture
* recherche plus intelligente a venir
* autres jeus d'apprentissage a venir
* nettoyage de la base de données a venir


### And possibly ...

* recherche de son et images sur internet
* recherche dans des batabases extérieures de tous les composants d'une nouvelle carte d'après le mot



