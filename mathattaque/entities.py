
import pygame
import random
import math
from config import *
# Collisions / clamp
def clamp(x, a, b): 
    return max(a, min(b, x))

class PowerUp:

    def __init__(self, kind, pos):
        self.kind = kind
        self.pos = pygame.Vector2(pos)
        from config import POWERUP_RADIUS
        self.r = POWERUP_RADIUS
        self.alive = True

    def draw(self, surf):
        # cercle jaune avec point d'interrogation noir
        center = (int(self.pos.x), int(self.pos.y))
        pygame.draw.circle(surf, (230, 210, 80), center, self.r)
        pygame.draw.circle(surf, (255, 255, 255), center, self.r, 2)

        font = pygame.font.SysFont(None, 32)
        img = font.render("?", True, (0, 0, 0))
        rect = img.get_rect(center=center)
        surf.blit(img, rect)

    def collides(self, player):
        return (self.pos - player.pos).length_squared() <= (self.r + player.r) ** 2

class Projectile:
    def __init__(self, pos, vel, owner, special=False): 
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.dir = (self.vel.normalize()
                    if self.vel.length_squared() > 0
                    else pygame.Vector2(1, 0))
        self.r = PROJ_RADIUS
        self.spawn = pygame.time.get_ticks()
        self.alive = True
        self.owner = owner
        self.special = special          
        self.damage = SPECIAL_PROJ_DAMAGE if special else NORMAL_PROJ_DAMAGE

    def update(self, dt):
        self.pos += self.vel * dt
        if pygame.time.get_ticks() - self.spawn > PROJ_TTL:
            self.alive = False

    def draw(self, surf):
        if not self.special:
            # projectile classique (craie)
            pygame.draw.rect(surf, (255, 255, 255), ((int(self.pos.x - self.r), int(self.pos.y - self.r), 26, 7)))
        else:
            # projectile spécial en forme de "crayon"
            head = self.pos
            tail = self.pos - self.dir * 22
            pygame.draw.line(surf, (255, 220, 150),
                             (int(head.x), int(head.y)),
                             (int(tail.x), int(tail.y)), 6)

            # pointe du crayon
            ortho = pygame.Vector2(-self.dir.y, self.dir.x)
            tip = head + self.dir * 6
            p1 = (int(tip.x), int(tip.y))
            p2 = (int(head.x + ortho.x * 4), int(head.y + ortho.y * 4))
            p3 = (int(head.x - ortho.x * 4), int(head.y - ortho.y * 4))
            pygame.draw.polygon(surf, (200, 150, 100), [p1, p2, p3])
    def collides(self, player):
        """Retourne True si le projectile touche le joueur (collision simple cercle)."""
        return (self.pos - player.pos).length_squared() <= (self.r + player.r)**2

class Special(Projectile):

    def draw(self, surf):
        head = pygame.Vector2(self.pos.x + 10, self.pos.y - 6)
        tail = pygame.Vector2(self.pos.x - 10, self.pos.y + 6)

        # corps du crayon
        pygame.draw.line(surf, (255, 220, 150),
                            (int(head.x), int(head.y)),
                            (int(tail.x), int(tail.y)), 4)

        # petite pointe
        tip = head + pygame.Vector2(4, -2)
        pygame.draw.circle(surf, (200, 150, 100),
                            (int(tip.x), int(tip.y)), 3)

class Player:
    def __init__(self, x, color, left_keys, right_keys, up_keys, down_keys, attack_key, sprite=None):
        self.pos = pygame.Vector2(x, HEIGHT*0.75)
        self.vel = pygame.Vector2()
        self.speed = 5
        self.sprite = sprite
        self.r = (sprite.get_width() // 2) if sprite else 32
        self.color = color
        self.hp = 100
        self.maxhp = 100
        self.cooldown = 0
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.up_keys = up_keys
        self.down_keys = down_keys
        self.attack_key = attack_key
        self.facing = 1

        # NEW ---- états de super-pouvoirs ----
        self.has_shield = False
        self.shield_until = 0

        self.reverse_controls = False
        self.reverse_controls_until = 0

        self.use_special_projectile = False
        self.special_proj_until = 0

        self.speed_factor = 1.0
        self.speed_effect_until = 0
        self.speed_effect_factor = 1.0
        
    def reset_effects(self):
        self.has_shield = False
        self.shield_until = 0
        self.reverse_controls = False
        self.reverse_controls_until = 0
        self.use_special_projectile = False
        self.special_proj_until = 0
        self.speed_factor = 1.0
        self.speed_effect_until = 0
        self.speed_effect_factor = 1.0

    def input(self, keys):
        effective_speed = self.speed * self.speed_factor

        if not self.reverse_controls:
            # contrôles normaux
            if keys[self.left_keys]:
                self.vel.x = -effective_speed
                self.facing = -1
            elif keys[self.right_keys]:
                self.vel.x = effective_speed
                self.facing = 1
            else:
                self.vel.x = 0

            if keys[self.up_keys]:
                self.vel.y = -effective_speed
            elif keys[self.down_keys]:
                self.vel.y = effective_speed
            else:
                self.vel.y = 0
        else:
            #contrôles inversés (tête qui tourne)
            if keys[self.left_keys]:
                self.vel.x = effective_speed
                self.facing = 1
            elif keys[self.right_keys]:
                self.vel.x = -effective_speed
                self.facing = -1
            else:
                self.vel.x = 0

            if keys[self.up_keys]:
                self.vel.y = effective_speed
            elif keys[self.down_keys]:
                self.vel.y = -effective_speed
            else:
                self.vel.y = 0
    def update(self):
        self.pos += self.vel
        self.pos.x = clamp(self.pos.x, self.r, WIDTH - self.r)
        self.pos.y = clamp(self.pos.y, self.r + 60, HEIGHT - self.r)
        if self.cooldown > 0: self.cooldown -= 1


    def draw(self, surf):

        if self.sprite:
            img = self.sprite
            if self.facing == -1:
                img = pygame.transform.flip(img, True, False)
            rect = img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            surf.blit(img, rect)
        else:
            pygame.draw.circle(surf, self.color, self.pos, self.r)
            eye = pygame.Vector2(12*self.facing, -6)
            pygame.draw.circle(surf, (20,20,20), self.pos + eye, 6)

        # NEW ---- Overlays visuels pour les powerups ----

        # Bouclier (protection) : "livre" autour de la tête
                # Bouclier (protection) : "livre" autour de la tête
                # NEW ---- Visuel "Livre" stylisé pour le powerup protection ----
        if self.has_shield:
            cx, cy = int(self.pos.x), int(self.pos.y)

            # dimensions du livre
            w = self.r * 2.2
            h = self.r * 1.5

            # coin haut gauche
            x = cx - w // 2
            y = cy - h // 2

            # pages (gauche et droite)
            left_page = pygame.Rect(x, y, w//2, h)
            right_page = pygame.Rect(x + w//2, y, w//2, h)

            # couleurs
            page_color = (245, 245, 250)   # blanc cassé
            edge_color = (80, 50, 20)      # brun
            spine_color = (150, 120, 60)   # beige doré

            # dessiner pages
            pygame.draw.rect(surf, page_color, left_page, border_radius=5)
            pygame.draw.rect(surf, page_color, right_page, border_radius=5)

            # bordures pages
            pygame.draw.rect(surf, edge_color, left_page, 2, border_radius=5)
            pygame.draw.rect(surf, edge_color, right_page, 2, border_radius=5)

            # ligne de reliure au centre
            pygame.draw.line(surf, spine_color,
                             (cx, y + 4),
                             (cx, y + h - 4), 3)

        # Vitesse boostée : petits éclairs autour du joueur
        if self.speed_factor > 1.0:
            x, y = int(self.pos.x), int(self.pos.y + self.r + 4)
            pygame.draw.line(surf, (255, 255, 0), (x-10, y), (x-4, y+12), 2)
            pygame.draw.line(surf, (255, 255, 0), (x+10, y), (x+4, y+12), 2)

        # Contrôles inversés : "dizzy" au-dessus de la tête
        if self.reverse_controls:
            center = (int(self.pos.x), int(self.pos.y - self.r - 10))
            pygame.draw.circle(surf, (255, 230, 120), center, 8, 2)
            pygame.draw.circle(surf, (255, 200, 80), center, 3)
                # Projectile spécial actif : petit crayon près du joueur
        if self.use_special_projectile:
            # mini crayon à côté du joueur (à droite de la tête)
            base_x = self.pos.x + self.r + 12
            base_y = self.pos.y

            head = pygame.Vector2(base_x + 10, base_y - 6)
            tail = pygame.Vector2(base_x - 10, base_y + 6)

            # corps du crayon
            pygame.draw.line(surf, (255, 220, 150),
                             (int(head.x), int(head.y)),
                             (int(tail.x), int(tail.y)), 4)

            # petite pointe
            tip = head + pygame.Vector2(4, -2)
            pygame.draw.circle(surf, (200, 150, 100),
                               (int(tip.x), int(tip.y)), 3)

    def rect(self):
        return pygame.Rect(self.pos.x - self.r, self.pos.y - self.r, self.r*2, self.r*2)

    def basic_attack(self, other, projectiles):
        if self.cooldown > 0:
            return False

        dir_vec = other.pos - self.pos
        if dir_vec.length_squared() < 1e-6:
            dir_vec = pygame.Vector2(self.facing, 0)
        dir_unit = dir_vec.normalize()

        spawn_offset = dir_unit * (self.r + 8)
        from config import PROJ_SPEED  # local import to avoid circularity

        # NEW : projectile spécial si superpower actif
        special = self.use_special_projectile
        if self.use_special_projectile:
            proj = Special(self.pos + spawn_offset, dir_unit * PROJ_SPEED, self)
        else:
            proj = Projectile(self.pos + spawn_offset, dir_unit * PROJ_SPEED, self)
        projectiles.append(proj)

        self.cooldown = FPS // 4
        return True


    def special(self, other, damage):

        # direction vers l'adversaire
        dir_vec = other.pos - self.pos
        if dir_vec.length_squared() < 1e-6:
            dir_vec = pygame.Vector2(self.facing, 0)
        dir_unit = dir_vec.normalize()

        from config import PROJ_SPEED

        # on le fait partir comme un tir normal, juste devant le joueur
        spawn_offset = dir_unit * (self.r + 8)

        proj = Special(
            self.pos + spawn_offset,
            dir_unit * PROJ_SPEED,
            self
        )

        # le projectile porte les dégâts calculés par le quiz
        proj.damage = int(damage)
        other.hp = max(0, other.hp - int(damage))

        

        return proj

class BotPlayer(Player):
    def __init__(self, x, color, sprite=None):
        super().__init__(
            x=x,
            color=color,
            left_keys=None, right_keys=None,
            up_keys=None, down_keys=None,
            attack_key=None,
            sprite=sprite
        )

        self.speed = BOT_SPEED
        self.move_dir = pygame.Vector2(0, 0)
        self.next_dir_change = 0

    def update_bot(self, target, projectiles, now):
        # ---- déplacement fluide ----
        if now >= self.next_dir_change:
            angle = random.uniform(0, 2*math.pi)
            self.move_dir = pygame.Vector2(
                math.cos(angle),
                math.sin(angle)
            )

            self.next_dir_change = now + BOT_MOVE_INTERVAL

        self.vel = self.move_dir * self.speed

        # update comme un joueur
        Player.update(self)

        # ---- tir automatique ----
        from config import BOT_FREQ
        if self.cooldown <= 0:
            # tire vers le joueur
            self.basic_attack(target, projectiles)
            self.cooldown = BOT_FREQ // (1000 / FPS)

class FallingNumber:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, 0)
        self.speed = random.uniform(100, 250)  # px/s
        self.text = str(random.randint(0, 9))
        self.font = pygame.font.SysFont(None, random.randint(24, 48))
        self.color = (255, 255, 0)
        self.alive = True

    def update(self, dt):
        self.y += self.speed * dt
        if self.y > HEIGHT:
            self.alive = False

    def draw(self, screen):
        img = self.font.render(self.text, True, self.color)
        screen.blit(img, (self.x, self.y))


class NumberRain:
    def __init__(self):
        self.numbers = []  # liste de FallingNumber

    def trigger(self, count=25):
        """Ajoute count nombres qui tombent."""
        for _ in range(count):
            self.numbers.append(FallingNumber())

    def update(self, dt):
        """Met a jour la position des nombres et supprime ceux hors ecran."""
        for num in self.numbers[:]:
            num.update(dt)
            if not num.alive:
                self.numbers.remove(num)

    def draw(self, screen):
        """Dessine tous les nombres sur l ecran."""
        for num in self.numbers:
            num.draw(screen)

    def check_collision(self, player, damage):
        """Inflige des degats si un nombre touche le joueur."""
        for num in self.numbers[:]:
            if player.rect().collidepoint(num.x, num.y):
                player.hp = max(0, player.hp - damage)
                self.numbers.remove(num)
