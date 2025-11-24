import sys
import pygame
from config import *
from ui import draw_button, draw_text, load_heads

def draw_stat_bar(screen, x, y, label, value, color, max_val=10):
    
    draw_text(screen, label, 18, (200, 200, 200), (x - 60, y + 6), align="right")
    
    box_w, box_h = 12, 12
    gap = 4
    for i in range(max_val):
        bx = x + i * (box_w + gap)
        rect = pygame.Rect(bx, y, box_w, box_h)
        
        if i < value:
            pygame.draw.rect(screen, color, rect) 
        else:
            pygame.draw.rect(screen, (60, 60, 70), rect) 
            pygame.draw.rect(screen, (100, 100, 100), rect, 1) 

def draw_character_selector(screen, x, y, player_idx, heads_list, label, color):
  
    name, original_img, stats = heads_list[player_idx]
    
    img_size = 128
    if original_img.get_width() != img_size:
        img = pygame.transform.smoothscale(original_img, (img_size, img_size))
    else:
        img = original_img

    cx = int(x)
    cy_img = int(y) - 60 

    draw_text(screen, label, 42, color, (cx, cy_img - 110))

    up_rect = pygame.Rect(cx - 20, cy_img - 95, 40, 30)
    pygame.draw.polygon(screen, (200, 200, 200), [(cx, cy_img - 95), (cx - 15, cy_img - 75), (cx + 15, cy_img - 75)])
    
    img_rect = img.get_rect(center=(cx, cy_img))
    screen.blit(img, img_rect)
    pygame.draw.rect(screen, color, img_rect, 4, border_radius=8)

    down_rect = pygame.Rect(cx - 20, cy_img + 70, 40, 30)
    pygame.draw.polygon(screen, (200, 200, 200), [(cx, cy_img + 95), (cx - 15, cy_img + 75), (cx + 15, cy_img + 75)])

    draw_text(screen, name, 32, (255, 255, 255), (cx, cy_img + 120))

    stat_start_y = cy_img + 160
    line_h = 22
    start_x_bars = cx - 20 

    order = ["aura", "impact", "precision", "resistance"]
    
    for i, key in enumerate(order):
        val = stats.get(key, 0)
        draw_stat_bar(screen, start_x_bars, stat_start_y + i*line_h, key.capitalize(), val, color)

    return up_rect, down_rect

def menu(screen, clock):

    DIFFS = [
        ("Facile",   QUESTIONS_FACILES),
        ("Moyen",    QUESTIONS_MOYENNES),
        ("Difficile", QUESTIONS_DIFFICILES),
    ]
    diff_idx = 1
    modes = ["Local 2P", "VS Computer"]
    mode_idx = 0

    HEADS = load_heads(size=128)
    p1_idx, p2_idx = 0, 1

    start_rect = pygame.Rect(WIDTH//2 - 140, HEIGHT - 300, 280, 50) 
    bio_button_rect = pygame.Rect(30, 30, 160, 40) 

    while True:
        screen.fill((25,25,35))

        draw_button(screen, bio_button_rect, "Biographies", active=True)
        draw_text(screen, "MATH FIGHTERS", 72, (255,230,0), (WIDTH//2, 60))
        
        draw_text(screen, f"<  Difficulté : {DIFFS[diff_idx][0]}  >", 28, (230,230,230), (WIDTH//2, 120))
        diff_rect_click = pygame.Rect(WIDTH//2 - 200, 100, 400, 40)

        p1_up_rect, p1_down_rect = draw_character_selector(
            screen, WIDTH * 0.22, HEIGHT * 0.52, p1_idx, HEADS, "JOUEUR 1", (120, 200, 255)
        )
        
        p2_up_rect, p2_down_rect = draw_character_selector(
            screen, WIDTH * 0.78, HEIGHT * 0.52, p2_idx, HEADS, "JOUEUR 2", (255, 120, 120)
        )

        draw_text(screen, "Z/S", 20, (100, 180, 230), (WIDTH * 0.22, HEIGHT * 0.92))
        draw_text(screen, "Haut/Bas", 20, (230, 100, 100), (WIDTH * 0.78, HEIGHT * 0.92))

        draw_button(screen, start_rect, "COMMENCER", active=True)

        mode_rects = []
        for i, name in enumerate(modes):
            rect = pygame.Rect(WIDTH - 260 + i*125, 30, 120, 40)
            draw_button(screen, rect, name, active=(i == mode_idx))
            mode_rects.append(rect)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit(0)
                if e.key == pygame.K_RETURN:
                    _, Q = DIFFS[diff_idx]
                    return modes[mode_idx], Q, HEADS[p1_idx][1], HEADS[p2_idx][1]

                if e.key == pygame.K_LEFT: diff_idx = (diff_idx - 1) % len(DIFFS)
                if e.key == pygame.K_RIGHT: diff_idx = (diff_idx + 1) % len(DIFFS)
                if e.key == pygame.K_z: p1_idx = (p1_idx - 1) % len(HEADS)
                if e.key == pygame.K_s: p1_idx = (p1_idx + 1) % len(HEADS)
                if e.key == pygame.K_UP: p2_idx = (p2_idx - 1) % len(HEADS)
                if e.key == pygame.K_DOWN: p2_idx = (p2_idx + 1) % len(HEADS)

            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                if diff_rect_click.collidepoint(mx, my): diff_idx = (diff_idx + 1) % len(DIFFS)
                if bio_button_rect.collidepoint(mx, my): biographies_screen(screen, clock)
                if start_rect.collidepoint(mx, my):
                    _, Q = DIFFS[diff_idx]
                    return modes[mode_idx], Q, HEADS[p1_idx][1], HEADS[p2_idx][1]
                for i, r in enumerate(mode_rects):
                    if r.collidepoint(mx, my): mode_idx = i
                if p1_up_rect.collidepoint(mx, my): p1_idx = (p1_idx - 1) % len(HEADS)
                if p1_down_rect.collidepoint(mx, my): p1_idx = (p1_idx + 1) % len(HEADS)
                if p2_up_rect.collidepoint(mx, my): p2_idx = (p2_idx - 1) % len(HEADS)
                if p2_down_rect.collidepoint(mx, my): p2_idx = (p2_idx + 1) % len(HEADS)

        clock.tick(60)

def pause_menu(screen, clock):
    from config import WIDTH, HEIGHT

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    btn_w, btn_h = 260, 58
    btn_y0 = HEIGHT//2 - 40
    r_resume = pygame.Rect(WIDTH//2 - btn_w//2, btn_y0, btn_w, btn_h)
    r_menu   = pygame.Rect(WIDTH//2 - btn_w//2, btn_y0 + 70, btn_w, btn_h)
    r_quit   = pygame.Rect(WIDTH//2 - btn_w//2, btn_y0 + 140, btn_w, btn_h)

    while True:
        overlay.fill((0,0,0,180))
        screen.blit(overlay, (0,0))
        draw_text(screen, "PAUSE", 64, (255,230,0), (WIDTH//2, HEIGHT//2 - 120))

        def _btn(rect, text):
            pygame.draw.rect(screen, (70,90,110), rect, border_radius=12)
            pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=12)
            draw_text(screen, text, 28, (255,255,255), rect.center)

        _btn(r_resume, "Reprendre  (R / Échap)")
        _btn(r_menu,   "Retour menu  (M)")
        _btn(r_quit,   "Quitter  (Q)")

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_r):
                    return "resume"
                if e.key == pygame.K_m:
                    return "menu"
                if e.key == pygame.K_q:
                    return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if r_resume.collidepoint(e.pos): return "resume"
                if r_menu.collidepoint(e.pos):   return "menu"
                if r_quit.collidepoint(e.pos):   return "quit"

        clock.tick(60)

BIOS = {
    "Evariste Galois": "Dans ce jeu Évariste Galois a autant de point de vie que son héritage mathématique est grandiose, autrement dit il est immortel mais c’est là tout le paradoxe\n (#contradictoire #impossibilitélogique #théorèmed’incomplétudedeGodel) : En effet dans la réalité, le génie fulgurant qui a renouvelé l’algèbre moderne n’a eu\n que vingt ans pour vivre – assez pour révolutionner les mathématiques, trop peu pour échapper à la fatalité qui l’a fauché avant même de voir l’ampleur de son\npropre héritage.", 
    "Isaac Newton": "Dans une réalité parallèle, Newton aurait tonné ces paroles étranges — à déclamer d’une voix solennelle : « ouane apeulle euh deille quipse zeu doctor euhouai ».\n Dans cet univers dévié, le grand maître de la gravitation ne redoute point les docteurs, mais bien ses pairs mathématiciens, qu’il repousse en leur projetant\n des pommes comme autant de projectiles célestes. Maître des équations du mouvement, il calcule chaque trajectoire avec une majesté implacable :\n jamais son tir ne vacille, jamais sa cible n’échappe à la rigueur de son génie. ",
    "Cédric Villani": "Cédric Villani est avant tout cèlèbre pour son engagement politique et pour l’affection singulière qu’il voue aux araignées. Il aime afficher cet créature à 8 \nappendice sur sa veste tel le blason d’une noble maison. Il a été rapporté qu’il s’intéressait aux mathématiques dans ses heures perdues.\n Il a paraît-il  apporté de mineures contributions dans le domaine de la physique statistique grâce à ses travaux sur l'amortissement de Landau,\n qui décrit l'évolution du champ électrique dans un plasma, travaux pour lesquels il a reçu une médaille en chocolat.", 
    "Euclide": "Euclide doué d’un sens de l’orientation extraordinaire a la capacité de trouver son chemin où qu’il aille à condition que la géométrie soit euclidienne ce qui lui\n crée de grandes difficultés au quotidien. En effet le papa de la géométrie ne sait se repérer qu’à condition d’avoir vérifié au préalable que : \n1° un segment de droite peut être tracé en joignant deux points quelconques distincts; \n2° un segment de droite peut être prolongé indéfiniment en une ligne droite ; \n3° étant donné un segment de droite quelconque, un cercle peut être tracé en prenant ce segment comme rayon et l'une de ses extrémités comme centre ; \n4° tous les angles droits sont congruents ; \n5° si deux droites sont sécantes avec une troisième de telle façon que la somme des angles intérieurs d'un côté est strictement inférieure à deux angles droits,\n alors ces deux droites sont forcément sécantes de ce côté.",
    "Srinivasa Ramanujan": "Srinivasa Ramanujan, génie autodidacte au renom mondial, fascine par l’éclat singulier de son esprit. On dit que son QI frôlait les sommets, estimé à 185,\n et pourtant, curieusement, les simples additions semblaient parfois lui échapper.\n Il soutenait avec une conviction presque mystique que la somme infinie 1+2+3+4+5+6+…1 + 2 + 3 + 4 + 5 + 6 +  valait −1/12,\nun résultat qui déroute et scandalise à la fois, car pour les mortels de l’arithmétique, la réalité est bien plus triviale. Mais c’est précisément ce mélange \nd’intuition vertigineuse et de décalage avec le commun des mortels qui fait de Ramanujan une légende intemporelle, oscillant entre le concret et le sublime.",
    "Leonard Euler": "Globalement Euler a tout fait, pas un seul domaine n’a échappé à ses griffes. Au tournoi des mathématiciens il est tout simplement premier,\n il a remporté des séries infinies de médailles, si bien que Pierre-Simon de Laplace se serait fendu d’un tweet élogieux :\n « Lisez Euler, lisez Euler, c’est notre maître à tous ! #lesmathématiquesneluirésistentpas #àlafoispasseuretbuteur ». "}

def draw_text_multiline_utility(screen, text, size, color, x_start, y_start, line_height_factor=1.2):
    lines = text.split('\n')
    current_y = y_start
    
    for line in lines:
        draw_text(screen, line, size, color, (x_start, current_y), align="left")
        current_y += int(size * line_height_factor)
        
    return current_y

def biographies_screen(screen, clock):
    """Affiche la liste complète des mathématiciens et leurs biographies, avec défilement."""
    
    back_button_rect = pygame.Rect(WIDTH - 250, HEIGHT - 80, 200, 50)
    
    scroll_offset = 0
    SCROLL_SPEED = 20
    START_Y = 120

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                if back_button_rect.collidepoint(mx, my):
                    return 
                    
            if e.type == pygame.MOUSEWHEEL:
                scroll_offset += e.y * SCROLL_SPEED 
                if scroll_offset > 0:
                    scroll_offset = 0

        screen.fill((25,25,35))
        draw_text(screen, "Encyclopédie Mathématique", 48, (255,230,0), (WIDTH//2, 50))
        
        y_pos = START_Y + scroll_offset
        
        for name, bio in BIOS.items():
            
            if y_pos < HEIGHT - 80: 
                draw_text(screen, name, 32, (255, 180, 80), (50, y_pos), align="left")
                y_pos += 35
                
                y_pos = draw_text_multiline_utility(screen, bio, 18, (200, 200, 200), 50, y_pos)
            else:
                y_pos = draw_text_multiline_utility(screen, bio, 18, (200, 200, 200), 50, y_pos) 
            y_pos += 25 
        
        draw_button(screen, back_button_rect, "Retour au Menu", active=True)
        
        pygame.display.flip()