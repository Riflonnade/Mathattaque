import random

WIDTH, HEIGHT = 960, 540
FPS = 60

BOT_FREQ = 800        #le temps entre chaque tir  
BOT_INTER = 20         #l'erreur maximum en pourcentage aux quizz 
BOT_MOVE_INTERVAL = 900 #le temps entre chaque changement de direction
BOT_SPEED = 4.2       #sa vitesse

BOX_W, BOX_H = 480, 46

MATH_INTERVAL = 13_000
MATH_DURATION = 12_000

SPECIAL_DAMAGE = 20
KNOCKBACK = 22
SPECIAL_PROJ_DAMAGE = 6        
NORMAL_PROJ_DAMAGE = 4         
SPECIAL_PROJ_KNOCKBACK = 1.6 

POWERUP_INTERVAL = 12000        
POWERUP_DURATION = 10000        
POWERUP_RADIUS = 24             

   


PROJ_SPEED = 700      
PROJ_RADIUS = 6       
PROJ_TTL = 1200       
PROJ_KNOCKBACK = 12 

def questions_faciles():
    a, b = random.randint(1, 20), random.randint(1, 20)
    op = random.choice(["+","-","*"])
    if op == "+": ans = a + b
    elif op == "-": ans = a - b
    else: ans = a * b
    return f"{a} {op} {b} ", ans

def questions_moyennes():
    a, b = random.randint(11, 99), random.randint(11, 99)
    op = random.choice(["*", "/"])
    if op == "*": ans = a * b
    else : ans = a / b
    return f"{a} {op} {b} ", ans

QUESTIONS_FACILES = [questions_faciles() for _ in range(200)]
QUESTIONS_MOYENNES = [questions_moyennes() for _ in range(200)]
QUESTIONS_DIFFICILES = [
    (r"e^{e^{\pi}}", 11216958622),
    (r"\sum_{n=1}^{10000} \frac{1}{n}",  9.7876),
    (r"|{p\ premier : p<10000}|", 1229),
    (r"|GL2(Z/7Z)|", 2016),
    (r"\sum_{n=1}^{10^{6}} \frac{(-1)^{n}}{n}", -0.6931),
    (r"\int_0^{100} \frac{\sin x}{x}\,dx", 1.5622),
    (r"\prod_{p<10000} (1-\frac{1}{p})^{-1}", 16.424),
    (r"\binom{10}{5}", 252),
    (r"\log(100!)", 363.739),
    (r"\phi(63)", 36)
]

HEAD_FILES = {
    # --- Les originaux ---
    "Galois":       "assets/heads/Galois.png",
    "Euler":        "assets/heads/Euler.png",
    "Newton":       "assets/heads/Newton.png",
    "Ramanujan":    "assets/heads/Ramanujan.png",
    "Villani":      "assets/heads/Villani.png",
    "Euclide":      "assets/heads/Euclide.png",
    "Pythagore":    "assets/heads/Pythagore.png",
    "Archimède":    "assets/heads/Archimède.png",
    "Al-Khwarizmi": "assets/heads/Al-Khwarizmi.png",
    "Descartes":    "assets/heads/Descartes.png",
    "Fermat":       "assets/heads/Fermat.png",
    "Pascal":       "assets/heads/Pascal.png",
    "Leibniz":      "assets/heads/Leibniz.png",
    "Gauss":        "assets/heads/Gauss.png",
    "Lovelace": "assets/heads/Lovelace.png",
    "Riemann":      "assets/heads/Riemann.png",
    "Cantor":       "assets/heads/Cantor.png",
    "Poincaré":     "assets/heads/Poincaré.png",
    "Hilbert":      "assets/heads/Hilbert.png",
}

CHARACTER_STATS = {
    # --- Les originaux ---
    "Galois":       {"aura": 8,  "impact": 9,  "precision": 7,  "resistance": 3},
    "Euler":        {"aura": 9,  "impact": 8,  "precision": 10, "resistance": 8},
    "Newton":       {"aura": 10, "impact": 10, "precision": 9,  "resistance": 6},
    "Ramanujan":    {"aura": 9,  "impact": 7,  "precision": 10, "resistance": 4},
    "Villani":      {"aura": 8,  "impact": 6,  "precision": 8,  "resistance": 7},
    "Euclide":      {"aura": 7,  "impact": 8,  "precision": 9,  "resistance": 10},
    "Pythagore":    {"aura": 9,  "impact": 8,  "precision": 6,  "resistance": 6}, # Mystique
    "Archimède":    {"aura": 8,  "impact": 9,  "precision": 8,  "resistance": 9}, # Solide (Eurêka !)
    "Al-Khwarizmi": {"aura": 7,  "impact": 10, "precision": 8,  "resistance": 6}, # Père de l'algo
    "Descartes":    {"aura": 8,  "impact": 8,  "precision": 9,  "resistance": 5}, # Analytique
    "Fermat":       {"aura": 9,  "impact": 7,  "precision": 6,  "resistance": 8}, # Enigmatique
    "Pascal":       {"aura": 7,  "impact": 8,  "precision": 8,  "resistance": 4}, # Santé fragile
    "Leibniz":      {"aura": 9,  "impact": 9,  "precision": 8,  "resistance": 7}, # Universel
    "Gauss":        {"aura": 10, "impact": 10, "precision": 10, "resistance": 8}, # Le Prince (OP)
    "Lovelace": {"aura": 8,  "impact": 8,  "precision": 7,  "resistance": 5}, # Visionnaire
    "Riemann":      {"aura": 9,  "impact": 9,  "precision": 8,  "resistance": 3}, # Génie fragile
    "Cantor":       {"aura": 9,  "impact": 10, "precision": 9,  "resistance": 2}, # L'infini rend fou
    "Poincaré":     {"aura": 9,  "impact": 9,  "precision": 7,  "resistance": 7}, # Dernier universaliste
    "Hilbert":      {"aura": 9,  "impact": 10, "precision": 10, "resistance": 8}, # Rigueur absolue
}