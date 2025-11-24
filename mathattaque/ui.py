
import pygame

from config import *
from questions import compute_precision


def load_heads(size=66):
    items = []
    for name, path in HEAD_FILES.items():
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (size, size))
        except Exception:
            img = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(img, (120,120,120), (size//2, size//2), size//2)
            pygame.draw.circle(img, (255,255,255), (size//2, size//2), size//2, 2)
        
        stats = CHARACTER_STATS.get(name, {"aura": 5, "impact": 5, "precision": 5, "resistance": 5})
        
        items.append((name, img, stats))
    return items

def intervalle(a, b, t):
    return a + (b - a) * t

def green_from_precision(prec):
    light = pygame.Color(200, 255, 200) 
    dark  = pygame.Color(  0, 120,   0)  
    t = max(0.0, min(1.0, prec/100.0))
    r = int(intervalle(light.r, dark.r, t))
    g = int(intervalle(light.g, dark.g, t))
    b = int(intervalle(light.b, dark.b, t))
    return (r, g, b)

def draw_text(surf, text, sizefont, color, pos, align="center"):
    f = pygame.font.SysFont(None, sizefont)
    img = f.render(text, True, color)
    rect = img.get_rect()

    if align == "center":
        rect.center = pos          
    elif align == "left":
        rect.midleft = pos         
    elif align == "right":
        rect.midright = pos        
    else:
        raise ValueError("align doit être 'left', 'center' ou 'right'")

    surf.blit(img, rect)
    return rect


def draw_button(surf, rect, text, active=False):
    bg = (70, 90, 110) if not active else (110, 150, 200)
    pygame.draw.rect(surf, bg, rect, border_radius=12)
    pygame.draw.rect(surf, (255,255,255), rect, width=2, border_radius=12)
    draw_text(surf, text, 28, (255,255,255), rect.center)

def draw_hpbar(surf, p, x, y):
    w, h = 360, 18
    pygame.draw.rect(surf, (60,60,60), (x, y, w, h))
    ratio = p.hp / p.maxhp
    pygame.draw.rect(surf, (0,200,80), (x, y, int(w*ratio), h))
    pygame.draw.rect(surf, (255,255,255), (x, y, w, h), 2)

def draw_precision_meter(surf, center, precision):
    color = green_from_precision(precision)
    # bar
    w, h = 360, 16
    rect = pygame.Rect(0, 0, w, h); rect.center = (center[0], center[1]+24)
    pygame.draw.rect(surf, (60,60,60), rect, border_radius=10)
    fill = rect.copy(); fill.width = int(rect.width * (precision/100.0))
    pygame.draw.rect(surf, color, fill, border_radius=10)
    pygame.draw.rect(surf, (230,230,230), rect, 2, border_radius=10)

    # text
    txt = f"Précision : {int(round(precision))}%"
    draw_text(surf, txt, 28, color, (center[0], center[1]))

def draw_quizz(p1_answer, p2_answer, active_input, quiz_end_time, question_img, now, screen, mode):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,160))
    screen.blit(overlay, (0,0))
    remain = int((quiz_end_time - now)/1000) + 1
    draw_text(screen, "MATHATTAQUE !", 64, (255,230,0), (WIDTH//2, HEIGHT//2-140))
    qrect = question_img.get_rect(center=(WIDTH//2, HEIGHT//2-80))
    screen.blit(question_img, qrect)

    def draw_input_box(rect, label, text, active, color_edge):
        
        pygame.draw.rect(screen, (60,60,70), rect, border_radius=10)
        pygame.draw.rect(screen, color_edge if active else (230,230,230),
                        rect, 3 if active else 2, border_radius=10)
        draw_text(screen, f"{label}: {text}", 42, (color_edge if active else (220,220,220)), rect.center)
    p1_input_rect = pygame.Rect(0, 0, BOX_W, BOX_H)
    p1_input_rect.center = (WIDTH // 2, HEIGHT // 2 + 20) 
    draw_input_box(p1_input_rect, "P1", p1_answer, active_input == 1, (120,200,255))
    if mode == "Local 2P":
        p2_input_rect = pygame.Rect(0, 0, BOX_W, BOX_H)
        p2_input_rect.center = (WIDTH // 2, HEIGHT // 2 + 70)
        draw_input_box(p2_input_rect, "P2", p2_answer, active_input == 2, (255,150,150))

    draw_text(screen, f"Temps restant: {remain}s", 36, (255,230,0), (WIDTH//2, HEIGHT//2+120))

def draw_winning_screen(screen, p1):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,200)); screen.blit(overlay, (0,0))
    win = "P2 gagne !" if p1.hp<=0 else "P1 gagne !"
    draw_text(screen, "K.O.", 96, (255,70,70), (WIDTH//2, HEIGHT//2-40))
    draw_text(screen, win, 48, (255,255,255), (WIDTH//2, HEIGHT//2+30))
    draw_text(screen, "R pour recommencer | M pour menu | Esc pour quitter", 28, (230,230,230), (WIDTH//2, HEIGHT//2+90))
    pygame.display.flip()

def draw_background(screen, p1, p2, projectiles, flash_time, now, winner_last):
        
        bg_img = pygame.image.load("assets/tableau.jpg").convert()
        bg_img = pygame.transform.smoothscale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))

        for proj in projectiles:
            proj.draw(screen)
    
        if flash_time > now and winner_last in (1,2):
            flame = pygame.image.load("assets/flamme.png")             
            flame = pygame.transform.smoothscale(flame, (300, 300))

            if winner_last == 1:
                 flame_rect = flame.get_rect(center=(int(p2.pos.x), int(p2.pos.y)))
            else:
                flame_rect = flame.get_rect(center=(int(p1.pos.x), int(p1.pos.y)))
            screen.blit(flame, flame_rect)


        p1.draw(screen); p2.draw(screen)
        draw_hpbar(screen, p1, 40, 20)
        draw_hpbar(screen, p2, WIDTH-400, 20)

        draw_text(screen, "P1: ZQSD + SPACE | P2: FLÈCHES + ENTER", 26, (0,0,0), (WIDTH//2, 50))
        draw_text(screen, "Échap = Pause/Menu", 22, (210,210,210), (WIDTH//2, 75))

def draw_quiz_results(screen, p1_answer, p2_answer, true_ans):
    p1_prec = compute_precision(p1_answer, true_ans)
    p2_prec = compute_precision(p2_answer, true_ans)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    screen.blit(overlay, (0,0))

    draw_text(screen, "Résultats du Quiz", 56, (255,230,0), (WIDTH//2, HEIGHT//2 - 160))

    draw_text(screen, f"P1 a répondu : {p1_answer}", 36, (120,200,255), (WIDTH//2, HEIGHT//2 - 60))
    draw_text(screen, f"Précision : {int(p1_prec)}%", 30, (120,200,255), (WIDTH//2, HEIGHT//2 - 20))

    draw_text(screen, f"P2 a répondu : {p2_answer}", 36, (255,150,150), (WIDTH//2, HEIGHT//2 + 40))
    draw_text(screen, f"Précision : {int(p2_prec)}%", 30, (255,150,150), (WIDTH//2, HEIGHT//2 + 80))

    draw_text(screen, f"Bonne réponse : {true_ans}", 40, (255,255,255), (WIDTH//2, HEIGHT//2 + 150))

    pygame.display.flip()