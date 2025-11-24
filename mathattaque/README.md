# MATHATTAQUE


## Sommaire
- [Aperçu](#-aperçu)
- [Bibliothèques Utilisées](#-bibliothèques-utilisées)
- [Contenu du Code](#-contenu-du-code)
- [Installation](#-installation)
- [Lancement du Jeu](#-lancement-du-jeu)
- [Équipe](#-équipe)

---

## Aperçu

Mathattaque est un PVP inspiré par streetfighter et headsoccer mettant au défi votre intuition mathématique et votre rigueur de calcul pour vaincre votre adversaire! 
Vous aurez la chance d'incarner les plus grands mathématiciens de notre ère, d'Euclide à Cédric Viliani en passant par Newton, Gauss, Galois et Ramanujan. Mêlez stratégie de déplacement et anticipation pour éviter les craies de votre adversaire et lui infliger les vôtres dans l'arène puis retrouvez vous régulièrement au duel face à une question mathématique. Le plus proche de l'expression exacte pourra libérer son attaque spéciale !
Bonne chance et que les maths soient avec vous !
---

## Bibliothèques Utilisées

- **Python 3**
- Bibliothèques :
  - `pygame`
  - `random`
  - `maths`
  - `matplotlib`
  - `pytest`

---

## Contenu du Code

- main.py : la boucle de jeu
- ui.py : fonctions de base utilisant l'interface graphique pygame pour faire boutons, texte...
- menu.py : fonctions d'affichage et d'interaction avec le menu utilisant abondament les fonctions de ui.py
- questions.py : fonctions relatives au quiz
- son.py : fonctions lançant les bruitages
- config.py : contient l'ensemble des constantes du code

- calcul_questions_difficiles.py : calcul des expressions mathématiques du mode difficile
- test.py : test de certaines des fonctions du code

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://gitlab-cw1.centralesupelec.fr/hugo.dunias/mathattaque.git

2. Accédez au dossier :
   ```bash
   cd mathattaque

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt


## Lancement

### Windows
```bash
python main.py
```

### Linux / Mac
```bash
python3 main.py
```

---

## ÉQUIPE

Maxime Vitry — maxime.vitry@student-cs.fr  
Jean Castel — jean.castel@student-cs.fr  
Baptiste Blasini — baptiste.blasini@student-cs.fr  
Zélie Forgeard — zelie.forgeard@student-cs.fr  
Toufic Najem — toufic.najem@student-cs.fr  
Hugo Dunias — hugo.dunias@student-cs.fr  
