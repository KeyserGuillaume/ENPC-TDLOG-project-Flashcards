# ENPC-TDLOG-project-Flashcards
Creating a simple, comprehensive program to constitute a flashcard library and provide tools to learn vocabulary interactively

Le fichier flaschcards.py contient la definition de la classe flaschcards, et sa méthode d'affichage. Son but est de constituer un niveau d'abstraction entre interface et base de donnée
Les fichiers createcards.ui et interf_create.py sont le resultat du travail d'esquisse de l'interface sur QtDesigner ; il sera inutile de les conserver sur le long terme --> a supprimer
Le fichier createcardsInterf.py contient la definition de l'interface de creation de flash cards et par héritage de celle de modification d'une carte donnée ; l'execution affiche l'interface de creation a l'ecran puis après action de l'utilisateur sur cette interface (fermeture ou creation) tire une carte au hasard dans la base de donnée et affiche l'interface de modification associée ; cliquer sur create ou modifier enregistre la carte ou les changements dans la base de donnée FlashCards.db 
Le fichier interfaccueil.py contient la definition de l'interface d'accueil (qui s'affichera a l'ouverture de l'application) ; cliquer sur le bouton NewCard ouvre l'interface de creation de nouvelles cartes ; cliquer sur le bouton Modify ouvre l'interface de modification d'une carte au hasard dans la base de donnée.
Le fichier database.py contient les fonctions de recherche/ajout/modification relatives à nos bases de données (langues + cartes par langue)
gestion des noms pour eviter deux cartes de meme nom a venir
gestion de l'insertion d'image et de son a venir
gestion de l'affichage des raccourcis de l'accueil par analyse de la base de données en fonction de la mairise a venir
interfaces de lecture et de parcours des cartes a venir
interface de recherche intelligente de carte a venir
premiers jeus d'apprentissage a venir
