﻿**EXECUTION DU JEU**:

    Prérequis: Pygame, les autres bibliothèques son inclues de base dans python.

    Pour lancer le jeu, exécutez simplement le fichier game.py.

    Pour selectionné les boutons il suffit de clicker dessus.
    Pour se déplacer il faut appuyer sur tab pour changer la molécule que l'on veut bouger
    et appuyé sur (a, z, q ou s) pour se déplacer dans la diagonale voulue.

**FONCTiONNEMENT**:
Le jeu est difivisé en 3 fichiers python chacune représentant une class:

-menu.py : **gestion du menu pour la sélection de niveau**

    Menu : gère l'affichage des boutons du menu de sélection de niveau.

    Le fichier utilise une variable terrains, contenant 5 listes de listes de chaînes de caractères (représenté par dificulter.), représentant différents niveaux. Selon le bouton cliqué, l'un de ces terrains est renvoyé, et game2.py lance la partie correspondante.
    Exemple de terrain :
    [
    ["y", "w", "w", "x"],
      ["x", "x", "x"],
    ["y", "w", "u", "g"],
      ["u", "u", "g"],
    ["x", "x", "d", "d"],
      ["x", "car", "d"],
    ["x", "x", "car", "x"],
    ]

-game.py : **gestion de la boucle du jeu et déroulement d'un niveau**

    Game : Contient la boucle principale et le déroulement du jeu.

      Affichage : En fonction de l'état de la variable stop, affiche soit le menu, soit la partie en cours.

      Mouvements : Lorsque le joueur appuie sur une touche (a, q, s, ou z), la fonction moveMolecule est appelée pour déplacer une pièce dans la direction demandée.

      Validation des mouvements : Le déplacement n'est effectué que si la fonction allValid retourne True. Cette fonction vérifie, pour chaque partie de la molécule sélectionnée, que la case cible est soit vide, soit une autre partie de la molécule, soit dans le terrain. Pour chaque élément, isValid vérifie que les mouvements sont permis. (case vide, autre partie de la molécule, ou dans le terrain). Si tout cela est vraie allValid return True si le déplacement en chaîne return True.

      Déplacements en chaîne : La fonction poussageRecursive permet de vérifier si une molécule peut se déplacer en "poussant" une autre. Si une autre molécule bloque le passage, poussageRecursive appelle à nouveau moveMolecule pour tenter de la déplacer. Si la molécule bloquante peut bouger, elle se déplace en premier, permettant le déplacement de la molécule initiale. sinon, le mouvement est annulé, et moveMolecule retourne False pour la première molécule. Ceci peux donc fonctionner pour plusieurs molécule de suite.

-terrain.py : **gestion de l'affichage du terrain**

      Terrain : Gère l'affichage du terrain et l'initialisation des images du jeu. Elle est activée après le choix d'un niveau. l'affichage dépant de la chaînes de caractère de la liste. ("car" affiche l'image du virus, "x" une case vide, "0" un block solid, une lettre au hasard créer une molécule.)

Un dossier images:

    Contenant les images des molécules, les cases vides, le background et un dossier pour les boutons (menu, rules, les niveaux)

Un dossier son:

    Contenant 3 sons de "bloop" qui se lance aléatoirement au mouvement d'une piece.
    Un son de fond fait par LogicMoon https://freesound.org/people/LogicMoon/sounds/712270/
