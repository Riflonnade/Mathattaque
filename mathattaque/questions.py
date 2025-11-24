
import random, io
import pygame
import matplotlib.pyplot as plt
from config import *

def render_latex(expr, fontsize=16, color='white'):
    """Retourne une surface pygame contenant la formule LaTeX rendue par matplotlib."""
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${expr}$", fontsize=fontsize, color=color)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05, transparent=True)
    plt.close(fig)
    buf.seek(0)
    img = pygame.image.load(buf, 'latex.png')
    scale = 0.5
    new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
    img = pygame.transform.smoothscale(img, new_size)
    return img.convert_alpha()

def new_question(selected_questions):
    expr, ans = random.choice(selected_questions)
    return expr, ans

def compute_precision(guess, true_ans):
    try:
        t = float(true_ans)
    except Exception:
        return 0.0
    try:
        g = float(guess)
    except Exception:
        return 0.0
    denom = max(1e-6, abs(t))
    err_ratio = abs(g - t) / denom
    err_ratio = min(1.0, err_ratio)
    return (1.0 - err_ratio) * 100.0




def resolve_quiz(a1, a2, true_ans):

    p1_prec = compute_precision(a1, true_ans)
    p2_prec = compute_precision(a2, true_ans)
    prec = 0
    if p1_prec > p2_prec:
        winner = 1
        prec = p1_prec
        scale = p1_prec / 100.0
        dmg = max(0, int(SPECIAL_DAMAGE * scale))

    elif p2_prec > p1_prec:
        prec = p2_prec
        winner = 2
        scale = p2_prec / 100.0
        dmg = max(0, int(SPECIAL_DAMAGE * scale))

    else:
        prec = 0
        winner = 0
        dmg = 0

    return winner, dmg, prec 