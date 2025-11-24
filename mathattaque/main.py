import sys
import pygame
import random

from config import *
from entities import *
from menus import *
from questions import *
from ui import *
from son import *


def apply_powerup(owner, other, kind, now):
    if kind == "shield":
        owner.shield_until = now + POWERUP_DURATION
        other.shield_until = 0

    elif kind == "reverse":
        owner.reverse_controls_until = 0
        other.reverse_controls_until = now + POWERUP_DURATION

    elif kind == "special_proj":
        owner.special_proj_until = now + POWERUP_DURATION
        other.special_proj_until = 0

    elif kind == "speed":
        owner.speed_effect_until = now + POWERUP_DURATION
        owner.speed_effect_factor = 1.5

        other.speed_effect_until = now + POWERUP_DURATION
        other.speed_effect_factor = 0.6
def refresh_player_effects(player, now):
    """Met à jour les booléens (has_shield, reverse_controls, etc.) à partir des timestamps."""
    player.has_shield = now < player.shield_until
    player.reverse_controls = now < player.reverse_controls_until
    player.use_special_projectile = now < player.special_proj_until

    if now < player.speed_effect_until:
        player.speed_factor = player.speed_effect_factor
    else:
        player.speed_factor = 1.0
        

def initialize_game(screen, clock):
    mode, selected_questions, p1_sprite, p2_sprite = menu(screen, clock)

    p1 = Player(WIDTH*0.25, (80,180,255),
                pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s, pygame.K_SPACE,
                sprite=p1_sprite)

    if mode == "VS Computer":
        p2 = BotPlayer(WIDTH*0.75, (255,120,120), sprite=p2_sprite)
    else:
        p2 = Player(WIDTH*0.75, (255,120,120),
                    pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN,
                    sprite=p2_sprite)

    last_question_time = pygame.time.get_ticks()
    in_quiz = False
    quiz_end_time = 0
    question, true_ans = None, None
    p1_answer, p2_answer = "", ""
    flash_time = 0
    winner_last = None
    winner_last_precision = 0.0
    projectiles = []
    active_input = 2 
    last_powerup_time = pygame.time.get_ticks()
    powerups = []
    number_rain = NumberRain()


    return (
        mode, selected_questions,
        p1, p2,
        last_question_time, in_quiz, quiz_end_time,
        question, true_ans, p1_answer, p2_answer,
        flash_time, winner_last, winner_last_precision,
        projectiles, active_input,  last_powerup_time, powerups, number_rain
    )


def initialize_quiz(now, selected_questions):
    in_quiz = True
    quiz_end_time = now + MATH_DURATION

    question, true_ans = new_question(selected_questions)
    question_img = render_latex(question, fontsize=48, color='white')

    p1_answer = ""
    p2_answer = ""

    p1_input_rect = pygame.Rect(0, 0, BOX_W, BOX_H)
    p1_input_rect.center = (WIDTH // 2, HEIGHT // 2 + 20)
    p2_input_rect = pygame.Rect(0, 0, BOX_W, BOX_H)
    p2_input_rect.center = (WIDTH // 2, HEIGHT // 2 + 70)

    active_input = 2

    return (
        in_quiz, quiz_end_time,
        question, true_ans, question_img,
        p1_answer, p2_answer,
        p1_input_rect, p2_input_rect,
        active_input
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Math Fighters")
    clock = pygame.time.Clock()

    (
        mode, selected_questions,
        p1, p2,
        last_question_time, in_quiz, quiz_end_time,
        question, true_ans, p1_answer, p2_answer,
        flash_time, winner_last, winner_last_precision,
        projectiles, active_input,  last_powerup_time, powerups, number_rain,
    ) = initialize_game(screen, clock)

    musique_fond(selected_questions)

    running = True
    while running:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choice = pause_menu(screen, clock)
                if choice == "quit":
                    pygame.quit(); sys.exit(0)
                elif choice == "menu":
                    (
                        mode, selected_questions,
                        p1, p2,
                        last_question_time, in_quiz, quiz_end_time,
                        question, true_ans, p1_answer, p2_answer,
                        flash_time, winner_last, winner_last_precision,
                        projectiles, active_input,last_powerup_time, powerups,number_rain,
                    ) = initialize_game(screen, clock)
                    continue

            if not in_quiz:
                if isinstance(p2, Player) and not isinstance(p2, BotPlayer):
                    if event.type == pygame.KEYDOWN:
                        if event.key == p1.attack_key: p1.basic_attack(p2, projectiles)
                        if event.key == p2.attack_key: p2.basic_attack(p1, projectiles)

                else: 
                    if event.type == pygame.KEYDOWN:
                        if event.key == p1.attack_key: p1.basic_attack(p2, projectiles)

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if active_input == 1: p1_answer = p1_answer[:-1]
                        else:                 p2_answer = p2_answer[:-1]
                    elif event.key == pygame.K_MINUS:
                        if active_input == 1: p1_answer += "-"
                        else:                 p2_answer += "-"
                    else:
                        ch = event.unicode
                        if ch.isdigit()  or ch in ['.', ',','-']:
                            if active_input == 1: p1_answer += ch
                            else:                 p2_answer += ch

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if p1_input_rect.collidepoint(event.pos):
                        active_input = 1
                    elif p2_input_rect.collidepoint(event.pos):
                        active_input = 2

        keys = pygame.key.get_pressed()

        refresh_player_effects(p1, now)
        refresh_player_effects(p2, now)

         
        if not in_quiz and now - last_powerup_time >= POWERUP_INTERVAL and len(powerups) == 0:
            kind = random.choice(["shield", "reverse", "special_proj", "speed"])
            x = random.randint(80, WIDTH - 80)
            y = random.randint(int(HEIGHT * 0.4), int(HEIGHT * 0.8))
            powerups.append(PowerUp(kind, (x, y)))
            last_powerup_time = now


        if not in_quiz and now - last_question_time >= MATH_INTERVAL:
            (
                in_quiz, quiz_end_time,
                question, true_ans, question_img,
                p1_answer, p2_answer,
                p1_input_rect, p2_input_rect,
                active_input
            ) = initialize_quiz(now, selected_questions)

        if in_quiz and now >= quiz_end_time:

            if mode == "VS Computer":
                p2_answer = str(true_ans*(1 + random.randint(-BOT_INTER, BOT_INTER)/100))

            def parse(s):
                try:
                    s = s.replace(',', '.')
                    if any(ch.isdigit() for ch in s):
                        return float(s)
                    else:
                        return None
                except:
                    return None

            a1, a2 = parse(p1_answer), parse(p2_answer)
            winner_last, damage, winner_last_precision = resolve_quiz(a1, a2, true_ans)
            pygame.display.flip()
            draw_quiz_results(screen, p1_answer, p2_answer, true_ans)
            pygame.time.delay(3200)

            flash_time = now + 5000
            in_quiz = False
            last_question_time = now
            if winner_last == 1 or winner_last == 2:
                number_rain.trigger(25)
            if winner_last == 1:
                proj = p1.special(p2, damage)
                projectiles.append(proj)
            elif winner_last == 2:
                proj = p2.special(p1, damage)
                projectiles.append(proj)

        if not in_quiz:

            p1.input(keys)
            p1.update()
            if isinstance(p2, BotPlayer):
                p2.update_bot(p1, projectiles, now)
            else:
                p2.input(keys)
                p2.update()

            dt_sec = dt / 1000.0
            for proj in projectiles[:]:
                proj.update(dt_sec)

                if (not proj.alive or proj.pos.x < -20 or proj.pos.x > WIDTH + 20 or
                    proj.pos.y < -20 or proj.pos.y > HEIGHT + 20):
                    projectiles.remove(proj)
                    continue

                target = p2 if proj.owner is p1 else p1
                if proj.collides(target):
                    if not target.has_shield:
                        bruitage_collision() 
                        target.hp = max(0, target.hp - proj.damage)
                        from config import SPECIAL_PROJ_KNOCKBACK
                        kb_amount = PROJ_KNOCKBACK * (SPECIAL_PROJ_KNOCKBACK if proj.special else 1.0)
                        kb = proj.dir * kb_amount
                        target.pos += kb
                    projectiles.remove(proj)

            for pu in powerups[:]:
                if pu.collides(p1):
                    apply_powerup(p1, p2, pu.kind, now)
                    powerups.remove(pu)
                    continue
                if pu.collides(p2):
                    apply_powerup(p2, p1, pu.kind, now)
                    powerups.remove(pu)
                    continue

            number_rain.update(dt_sec)
            if winner_last == 1:
                number_rain.check_collision(p2, SPECIAL_DAMAGE)
            elif winner_last == 2:
                number_rain.check_collision(p1, SPECIAL_DAMAGE)
                


        draw_background(screen, p1, p2, projectiles, flash_time, now, winner_last)
         
        for pu in powerups:
            pu.draw(screen)
        if in_quiz:
            draw_quizz(p1_answer, p2_answer, active_input, quiz_end_time, question_img, now, screen, mode)

        if not in_quiz and winner_last is not None and flash_time > now - 1000:
            if winner_last == 0:
                msg = "Égalité !"
                draw_text(screen, msg, 36, (255,255,255), (WIDTH//2, 100))
            else:
                msg = f"Attaque spéciale P{winner_last} !"
                draw_text(screen, msg, 36, (255,255,255), (WIDTH//2, 90))
                draw_precision_meter(screen, (WIDTH//2, 130), winner_last_precision)
        number_rain.draw(screen) 
        
        if p1.hp <= 0 or p2.hp <= 0:
            draw_winning_screen(screen, p1)

            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit(0)
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_ESCAPE:
                            pygame.quit(); sys.exit(0)
                        if e.key == pygame.K_m:
                            mode, selected_questions, p1_sprite, p2_sprite = menu(screen, clock)
                            p1 = Player(WIDTH*0.25, (80,180,255), pygame.K_q, pygame.K_d, pygame.K_z, pygame.K_s, pygame.K_SPACE, sprite=p1_sprite)
                            p2 = Player(WIDTH*0.75, (255,120,120), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN, sprite=p2_sprite)
                            p1.hp = p2.hp = 100
                            p1.pos.update(WIDTH*0.25, HEIGHT*0.75)
                            p2.pos.update(WIDTH*0.75, HEIGHT*0.75)
                            p1.reset_effects()   
                            p2.reset_effects()   
                            powerups.clear()     
                            number_rain = NumberRain()

                            last_question_time = pygame.time.get_ticks()
                            in_quiz = False
                            flash_time = 0
                            winner_last = None
                            projectiles.clear()
                            continue
                        if e.key == pygame.K_r:
                            p1.hp = p2.hp = 100
                            p1.pos.update(WIDTH*0.25, HEIGHT*0.75)
                            p2.pos.update(WIDTH*0.75, HEIGHT*0.75)
                            p1.reset_effects()   
                            p2.reset_effects()   
                            powerups.clear()     
                            last_question_time = pygame.time.get_ticks()
                            winner_last = None
                            flash_time = 0
                            waiting = False
                clock.tick(30)
            continue

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
