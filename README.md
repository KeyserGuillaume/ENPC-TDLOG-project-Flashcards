# ENPC-TDLOG-project-Flashcards
**Creating a simple, comprehensive program to constitute a flashcard library and provide tools to learn vocabulary interactively**

Petit programme pour constituer, carte par carte, une bibliothèque de cartes de vocabulaire (flash cards). Chaque carte a un mot et sa traduction au minimum. On peut s'auto-enregistrer pour avoir la prononciation du mot, ou choisir une image via une recherche sur la base d'images pixabay.

L'apprentissage du vocabulaire se fait via des jeux interactifs qui consistent à associer un mot à sa traduction, donner le mot à partir de se traduction et vice-versa, associer le mot à l'image...

Le programme est fait pour que les mots que l'utilisateur maîtrise le moins reviennent plus souvent.

L'application n'est testée que sous linux et ne fonctionnera vraisemblablement pas sous windows. Elle requiert l'installation de python3 et des modules sqlite, pyqt5, pyaudio, wave... 
L'application est lancée à l'éxécution de main.py

### Description of the repository content

Les fichiers clés de ce projet sont à ce jour :

* README.md : description du projet, des données, des méthodes
* main.py : lancement de l'application python
* FlashCards.db : la base de donnée
* model.flaschcards.py : la definition de la classe flashcards, et sa méthode d'affichage. Son but est de constituer un niveau d'abstraction entre interface et base de donnée
* model.database.py : les fonctions de recherche/ajout/modification relatives à nos bases de données (langues + cartes par langue)
* model.rechercheFonct.py : les fonctions de recherche a partir des demandes reçues
* controller.AccessSettings.py et controller.AppSettings.xml : gestion, stockage et accès des paramètres utilisateurs.
* view.interfaccueil.py : la definition de l'interface d'accueil (qui s'affichera a l'ouverture de l'application) ; cliquer sur le bouton NewCard ouvre l'interface de creation de nouvelles cartes; cliquer sur les mots de la bande gauche ouvre une interface de lecture sur l'échantillon; cliquer sur les dossiers ouvre  l'interface de parcours associée ; cliquer sur les icones de jeux ouvre une partie.
* view.createcardsInterf.py : la definition de l'interface de création et de modification de flash cards; cliquer sur create ou modify enregistre la carte ou les changements dans la base de donnée FlashCards.db
* view.icons : fichier image and conversion en fichier de ressources pour les diverses icones et fonds des interfaces.
* view.parcours.py : la definition de l'interface de parcours pour l'ensemble des langues (affichage de dossiers), pour les jeux (affichage d'icones), pour les flash cards (cartes).
* view.rechercheInterf.py : interface de recherche.
* view.viewCard.py : affichage de lecture de FlashCards i.e. affiche sur joli fond une carte qui se retourne avec les infos intéressantes, avec un bouton pour la modifier, un autre pour écouter le son, un autre pour visualiser l'image.
* view.settingsInterf.py : interface d'ajustement des paramètres utilisateurs.
* view.games.gameWindow.py : interface de jeu - fenetre global avec chrono et décompte d'erreurs.
* view.games.dragAndDrop.py ; view.games.hotColdGame.py ; view.games.memory.py ; view.games.pointToCard.py ; view.games.vraiOuFaux.py : interface et fonctionnement des 5 jeux d'apprentissage du projet.

### Further possibilites

Nous indiquons ici les développements potentiels que nous avons identifié:

* recherche de sons ou traduction sur base de données externes
* jeux pour associer le mot et/ou la traduction à la prononciation


