from array import array
import math
import random
import sys
import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
WIDTH, HEIGHT = 940, 930
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Memory Deluxe")
clock = pygame.time.Clock()


def make_tone(f1, f2, dur, vol=0.25):
    try:
        sr = 44100
        n = int(sr * dur)
        buf = array("h")
        for i in range(n):
            t = i / sr
            prog = i / n
            f = f1 + (f2 - f1) * prog
            env = (1.0 - prog) ** 1.5
            val = int(math.sin(2 * math.pi * f * t) * 32767 * vol * env)
            buf.append(val)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


SND_FLIP = make_tone(340, 600, 0.08, 0.2)
SND_MATCH = make_tone(520, 1040, 0.22, 0.3)
SND_MISS = make_tone(240, 140, 0.20, 0.2)
SND_CLICK = make_tone(480, 650, 0.06, 0.2)
SND_WIN = make_tone(440, 880, 0.45, 0.35)
SND_LOSE = make_tone(320, 110, 0.55, 0.35)
SND_TICK = make_tone(750, 750, 0.05, 0.15)


def play_snd(snd):
    if snd:
        try:
            snd.play()
        except Exception:
            pass


FRUITS = [
    "apple",
    "orange",
    "watermelon",
    "grapes",
    "strawberry",
    "cherry",
    "lemon",
    "pear",
    "blueberry",
    "kiwi",
    "banana",
    "pineapple",
    "avocado",
    "coconut",
    "peach",
    "plum",
]

TIME_LIMITS = {4: 45, 6: 100, 8: 180, 10: 300}


def draw_fruit_graphic(surface, fruit, cx, cy, r):
    if fruit == "apple":
        pygame.draw.circle(surface, (225, 35, 45), (cx, cy + r // 6), r)
        pygame.draw.circle(surface, (255, 130, 130), (cx - r // 3, cy - r // 6), max(2, r // 4))
        pygame.draw.line(surface, (110, 65, 25), (cx, cy - r // 2), (cx, cy - r - r // 4), max(2, r // 5))
        pygame.draw.ellipse(surface, (45, 190, 55), (cx, cy - r - r // 6, r // 2, r // 3))
    elif fruit == "orange":
        pygame.draw.circle(surface, (255, 140, 0), (cx, cy + r // 8), r)
        pygame.draw.circle(surface, (255, 200, 90), (cx - r // 3, cy - r // 5), max(2, r // 4))
        pygame.draw.ellipse(surface, (45, 190, 55), (cx - r // 4, cy - r, r // 2, r // 3))
    elif fruit == "watermelon":
        pygame.draw.circle(surface, (35, 160, 50), (cx, cy), r)
        pygame.draw.circle(surface, (185, 235, 175), (cx, cy), int(r * 0.88))
        pygame.draw.circle(surface, (240, 50, 65), (cx, cy), int(r * 0.78))
        for dx, dy in [(-1, -1), (1, -1), (0, 1), (-1, 1), (1, 1)]:
            pygame.draw.circle(surface, (25, 25, 25), (cx + dx * r // 3, cy + dy * r // 3), max(1, r // 8))
    elif fruit == "grapes":
        sr = max(3, int(r * 0.38))
        offsets = [(-sr, -sr // 2), (0, -sr // 2), (sr, -sr // 2), (-sr // 2, sr // 2), (sr // 2, sr // 2), (0, int(sr * 1.4))]
        for ox, oy in offsets:
            pygame.draw.circle(surface, (145, 45, 180), (cx + ox, cy + oy), sr)
            pygame.draw.circle(surface, (200, 130, 230), (cx + ox - sr // 4, cy + oy - sr // 4), max(1, sr // 3))
        pygame.draw.line(surface, (100, 60, 20), (cx, cy - sr), (cx, cy - r), max(2, r // 6))
    elif fruit == "strawberry":
        pts = [(cx - r, cy - r // 2), (cx + r, cy - r // 2), (cx, cy + r)]
        pygame.draw.polygon(surface, (235, 30, 55), pts)
        pygame.draw.ellipse(surface, (235, 30, 55), (cx - r, cy - r, r * 2, r))
        pygame.draw.ellipse(surface, (45, 190, 55), (cx - r // 2, cy - r - r // 6, r, r // 2))
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            pygame.draw.circle(surface, (255, 225, 110), (cx + dx * r // 3, cy + dy * r // 3), max(1, r // 8))
    elif fruit == "cherry":
        cr = max(3, int(r * 0.48))
        pygame.draw.line(surface, (45, 170, 45), (cx - cr, cy + cr // 2), (cx, cy - r), max(2, r // 7))
        pygame.draw.line(surface, (45, 170, 45), (cx + cr, cy + cr // 2), (cx, cy - r), max(2, r // 7))
        pygame.draw.circle(surface, (210, 15, 40), (cx - cr, cy + cr // 2), cr)
        pygame.draw.circle(surface, (210, 15, 40), (cx + cr, cy + cr // 2), cr)
        pygame.draw.circle(surface, (255, 130, 140), (cx - cr - cr // 4, cy + cr // 4), max(1, cr // 3))
        pygame.draw.circle(surface, (255, 130, 140), (cx + cr - cr // 4, cy + cr // 4), max(1, cr // 3))
    elif fruit == "lemon":
        rect = (cx - r, cy - int(r * 0.7), r * 2, int(r * 1.4))
        pygame.draw.ellipse(surface, (250, 220, 20), rect)
        pygame.draw.circle(surface, (250, 220, 20), (cx - r, cy), max(2, r // 4))
        pygame.draw.circle(surface, (250, 220, 20), (cx + r, cy), max(2, r // 4))
        pygame.draw.ellipse(surface, (255, 245, 150), (cx - r // 2, cy - r // 3, r, r // 3))
    elif fruit == "pear":
        pygame.draw.circle(surface, (160, 210, 40), (cx, cy + r // 3), int(r * 0.75))
        pygame.draw.circle(surface, (160, 210, 40), (cx, cy - r // 3), int(r * 0.5))
        pygame.draw.circle(surface, (215, 240, 120), (cx - r // 4, cy + r // 4), r // 4)
        pygame.draw.line(surface, (100, 60, 20), (cx, cy - int(r * 0.8)), (cx, cy - r - r // 5), max(2, r // 6))
    elif fruit == "blueberry":
        pygame.draw.circle(surface, (40, 85, 205), (cx, cy + r // 8), r)
        pygame.draw.circle(surface, (110, 160, 250), (cx - r // 3, cy - r // 6), max(2, r // 4))
        pygame.draw.circle(surface, (20, 40, 110), (cx, cy - r // 3), max(2, r // 3))
    elif fruit == "kiwi":
        pygame.draw.circle(surface, (135, 85, 40), (cx, cy), r)
        pygame.draw.circle(surface, (135, 200, 50), (cx, cy), int(r * 0.82))
        pygame.draw.circle(surface, (230, 250, 190), (cx, cy), int(r * 0.36))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pygame.draw.circle(surface, (25, 25, 25), (cx + dx * int(r * 0.55), cy + dy * int(r * 0.55)), max(1, r // 9))
    elif fruit == "banana":
        pygame.draw.arc(surface, (250, 215, 25), (cx - r, cy - r, r * 2, r * 2), 0.4, 2.7, max(4, int(r * 0.55)))
        pygame.draw.arc(surface, (255, 240, 120), (cx - r, cy - r, r * 2, r * 2), 0.6, 2.5, max(2, int(r * 0.2)))
    elif fruit == "pineapple":
        pts = [(cx, cy - r - r // 3), (cx - r // 2, cy - r // 2), (cx + r // 2, cy - r // 2)]
        pygame.draw.polygon(surface, (40, 175, 55), pts)
        rect = (cx - int(r * 0.75), cy - r // 2, int(r * 1.5), int(r * 1.5))
        pygame.draw.ellipse(surface, (240, 175, 25), rect)
        pygame.draw.line(surface, (185, 115, 15), (cx - r // 2, cy), (cx + r // 2, cy + r // 2), max(1, r // 8))
        pygame.draw.line(surface, (185, 115, 15), (cx + r // 2, cy), (cx - r // 2, cy + r // 2), max(1, r // 8))
    elif fruit == "avocado":
        pygame.draw.ellipse(surface, (45, 120, 45), (cx - int(r * 0.8), cy - r, int(r * 1.6), r * 2))
        pygame.draw.ellipse(surface, (175, 225, 100), (cx - int(r * 0.62), cy - int(r * 0.8), int(r * 1.24), int(r * 1.6)))
        pygame.draw.circle(surface, (115, 65, 30), (cx, cy + r // 5), int(r * 0.42))
        pygame.draw.circle(surface, (160, 105, 60), (cx - r // 8, cy + r // 8), max(1, r // 7))
    elif fruit == "coconut":
        pygame.draw.circle(surface, (105, 62, 30), (cx, cy), r)
        pygame.draw.circle(surface, (245, 245, 245), (cx, cy), int(r * 0.78))
        pygame.draw.circle(surface, (200, 235, 250), (cx, cy), int(r * 0.42))
    elif fruit == "peach":
        pygame.draw.circle(surface, (255, 125, 95), (cx - r // 5, cy + r // 8), int(r * 0.82))
        pygame.draw.circle(surface, (255, 145, 110), (cx + r // 5, cy + r // 8), int(r * 0.82))
        pygame.draw.ellipse(surface, (55, 185, 60), (cx, cy - r, r // 2, r // 3))
    elif fruit == "plum":
        pygame.draw.ellipse(surface, (115, 35, 135), (cx - int(r * 0.85), cy - int(r * 0.9), int(r * 1.7), int(r * 1.85)))
        pygame.draw.circle(surface, (175, 95, 195), (cx - r // 3, cy - r // 4), max(2, r // 4))
        pygame.draw.line(surface, (100, 60, 25), (cx, cy - int(r * 0.85)), (cx + r // 4, cy - r - r // 5), max(2, r // 6))


def draw_star(surface, cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = i * math.pi / 5 - math.pi / 2
        d = r if i % 2 == 0 else r * 0.42
        pts.append((cx + d * math.cos(ang), cy + d * math.sin(ang)))
    pygame.draw.polygon(surface, color, pts)
    pygame.draw.polygon(surface, (120, 80, 10), pts, 2)


def create_menu_bg():
    surf = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        p = y / HEIGHT
        r = int(85 + p * 110)
        g = int(190 + p * 55)
        b = int(250 - p * 35)
        pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))

    pygame.draw.circle(surf, (255, 245, 160), (140, 130), 65)
    pygame.draw.circle(surf, (255, 230, 90), (140, 130), 52)

    pygame.draw.ellipse(surf, (110, 205, 75), (-150, HEIGHT - 280, 650, 360))
    pygame.draw.ellipse(surf, (90, 185, 60), (320, HEIGHT - 310, 750, 380))
    pygame.draw.ellipse(surf, (65, 155, 45), (-100, HEIGHT - 180, WIDTH + 200, 260))

    for x in range(40, WIDTH, 90):
        pygame.draw.rect(surf, (160, 105, 50), (x, HEIGHT - 150, 18, 65), border_radius=4)
    pygame.draw.rect(surf, (145, 90, 40), (0, HEIGHT - 135, WIDTH, 12))
    pygame.draw.rect(surf, (145, 90, 40), (0, HEIGHT - 110, WIDTH, 12))
    return surf


def create_game_bg():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill((55, 140, 50))
    for i in range(0, WIDTH, 40):
        pygame.draw.circle(surf, (45, 125, 42), (i, 15), 28)
        pygame.draw.circle(surf, (45, 125, 42), (i, HEIGHT - 15), 28)

    board_rect = pygame.Rect(35, 118, WIDTH - 70, HEIGHT - 140)
    pygame.draw.rect(surf, (30, 65, 25), (board_rect.x + 8, board_rect.y + 10, board_rect.w, board_rect.h), border_radius=28)
    pygame.draw.rect(surf, (155, 95, 45), board_rect, border_radius=28)

    for y in range(board_rect.y + 15, board_rect.bottom - 15, 22):
        pygame.draw.line(surf, (140, 82, 36), (board_rect.x + 15, y), (board_rect.right - 15, y), 2)

    pygame.draw.rect(surf, (105, 60, 25), board_rect, 8, border_radius=28)

    inner_rect = pygame.Rect(55, 138, WIDTH - 110, HEIGHT - 180)
    pygame.draw.rect(surf, (125, 75, 32), inner_rect, border_radius=20)
    pygame.draw.rect(surf, (90, 50, 20), inner_rect, 4, border_radius=20)
    return surf


MENU_BG = create_menu_bg()
GAME_BG = create_game_bg()


class IconSpriteButton:

    def __init__(self, x, y, size, icon_type, bg_color):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.icon_type = icon_type
        self.bg_color = bg_color
        self.badge_count = None
        self.image = self.build_surface(False)
        self.hover_image = self.build_surface(True)

    def build_surface(self, hover):
        s = self.size
        surf = pygame.Surface((s, s + 6), pygame.SRCALPHA)
        cx, cy = s // 2, s // 2 + (0 if hover else 2)

        pygame.draw.circle(surf, (25, 40, 20, 140), (s // 2, s // 2 + 5), s // 2 - 2)
        col = tuple(min(255, c + 30) for c in self.bg_color) if hover else self.bg_color
        pygame.draw.circle(surf, col, (cx, cy), s // 2 - 2)
        pygame.draw.circle(surf, (255, 240, 190), (cx, cy), s // 2 - 2, 3)

        r = int(s * 0.28)
        if self.icon_type == "home":
            pts = [(cx, cy - r), (cx - r, cy - 2), (cx + r, cy - 2)]
            pygame.draw.polygon(surf, (255, 255, 255), pts)
            pygame.draw.rect(surf, (255, 255, 255), (cx - r + 4, cy - 2, (r - 4) * 2, r + 2), border_radius=2)
            pygame.draw.rect(surf, col, (cx - 4, cy + 3, 8, r - 3))
        elif self.icon_type == "reload":
            pygame.draw.arc(surf, (255, 255, 255), (cx - r, cy - r, r * 2, r * 2), 0.6, math.pi * 1.85, 4)
            pts = [(cx + r - 2, cy - 6), (cx + r + 5, cy + 3), (cx + r - 8, cy + 3)]
            pygame.draw.polygon(surf, (255, 255, 255), pts)
        elif self.icon_type == "eye":
            pygame.draw.ellipse(surf, (255, 255, 255), (cx - r - 2, cy - r // 1.4, (r + 2) * 2, int(r * 1.4)), 3)
            pygame.draw.circle(surf, (255, 255, 255), (cx, cy), r // 2)
        elif self.icon_type == "bulb":
            pygame.draw.circle(surf, (255, 245, 130), (cx, cy - 3), int(r * 0.75))
            pygame.draw.rect(surf, (220, 220, 220), (cx - r // 2, cy + r // 2 - 1, r, 6), border_radius=2)
        elif self.icon_type == "clock":
            pygame.draw.circle(surf, (255, 255, 255), (cx, cy), r, 3)
            pygame.draw.line(surf, (255, 255, 255), (cx, cy), (cx, cy - r // 2), 3)
            pygame.draw.line(surf, (255, 255, 255), (cx, cy), (cx + r // 2, cy), 3)
        return surf

    def draw(self, surface, font):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        surface.blit(self.hover_image if hover else self.image, self.rect.topleft)
        if self.badge_count is not None:
            bx, by = self.rect.right - 10, self.rect.bottom - 10
            pygame.draw.circle(surface, (220, 40, 50), (bx, by), 11)
            pygame.draw.circle(surface, (255, 255, 255), (bx, by), 11, 2)
            txt = font.render(str(self.badge_count), True, (255, 255, 255))
            surface.blit(txt, (bx - txt.get_width() // 2, by - txt.get_height() // 2))


class LevelCardButton:

    def __init__(self, x, y, w, h, grid_size, fruit_icon):
        self.rect = pygame.Rect(x, y, w, h)
        self.grid_size = grid_size
        self.fruit_icon = fruit_icon
        self.image = self.build_card(w, h, False)
        self.hover_image = self.build_card(w, h, True)

    def build_card(self, w, h, hover):
        surf = pygame.Surface((w, h + 8), pygame.SRCALPHA)
        y_off = 0 if hover else 3

        pygame.draw.rect(surf, (25, 50, 20, 150), (4, 8, w - 8, h - 4), border_radius=22)
        bg_col = (255, 248, 225) if hover else (245, 232, 195)
        border_col = (210, 135, 45) if hover else (175, 105, 35)

        body = pygame.Rect(0, y_off, w, h - 4)
        pygame.draw.rect(surf, bg_col, body, border_radius=22)
        pygame.draw.rect(surf, border_col, body, 5, border_radius=22)

        preview_size = 76
        px, py = 24, y_off + (h - 4 - preview_size) // 2
        pygame.draw.rect(surf, (185, 120, 55), (px - 4, py - 4, preview_size + 8, preview_size + 8), border_radius=10)
        cell = preview_size // self.grid_size
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                col = (255, 220, 130) if (r + c) % 2 == 0 else (230, 185, 95)
                pygame.draw.rect(surf, col, (px + c * cell + 1, py + r * cell + 1, cell - 2, cell - 2), border_radius=2)

        draw_fruit_graphic(surf, self.fruit_icon, w - 48, y_off + 40, 22)

        font_big = pygame.font.SysFont("arial", 28, bold=True)
        txt = font_big.render(f"{self.grid_size} x {self.grid_size}", True, (110, 60, 15))
        surf.blit(txt, (116, y_off + 16))
        return surf

    def draw(self, surface, font, stars, best_score):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        y_off = 0 if hover else 3
        surface.blit(self.hover_image if hover else self.image, self.rect.topleft)

        t_limit = TIME_LIMITS[self.grid_size]
        sc_txt = font.render(f"Time: {t_limit}s  |  Best: {best_score}", True, (150, 90, 30))
        surface.blit(sc_txt, (self.rect.x + 116, self.rect.y + y_off + 54))

        for i in range(3):
            scol = (255, 205, 0) if i < stars else (200, 185, 155)
            draw_star(surface, self.rect.x + 130 + i * 30, self.rect.y + y_off + 98, 12, scol)


class FloatingText:

    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 55
        self.font = pygame.font.SysFont("arial", 24, bold=True)

    def update(self):
        self.y -= 1.4
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = min(255, int((self.life / 55) * 255))
            txt = self.font.render(self.text, True, self.color)
            shd = self.font.render(self.text, True, (40, 20, 5))
            txt.set_alpha(alpha)
            shd.set_alpha(alpha)
            surface.blit(shd, (int(self.x - txt.get_width() // 2 + 2), int(self.y + 2)))
            surface.blit(txt, (int(self.x - txt.get_width() // 2), int(self.y)))


class Particle:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(2, 8)
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.life = random.randint(25, 50)
        self.size = random.randint(4, 9)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18
        self.life -= 1
        self.size = max(0, self.size - 0.15)

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))


class Card:

    def __init__(self, x, y, size, fruit):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.fruit = fruit
        self.revealed = False
        self.matched = False
        self.hint_timer = 0
        self.flip_progress = 0.0
        self.hover_offset = 0.0

    def update(self, mouse_pos, force_reveal=False):
        show = self.revealed or self.matched or force_reveal
        target_flip = 1.0 if show else 0.0
        self.flip_progress += (target_flip - self.flip_progress) * 0.24

        if self.hint_timer > 0:
            self.hint_timer -= 1

        is_hover = self.rect.collidepoint(mouse_pos) and not show
        target_hover = 4.0 if is_hover else 0.0
        self.hover_offset += (target_hover - self.hover_offset) * 0.25

    def draw(self, surface):
        scale_x = abs(math.cos(self.flip_progress * math.pi))
        w = max(4, int(self.size * scale_x))
        draw_x = self.x + (self.size - w) // 2
        draw_y = int(self.y - self.hover_offset)
        radius = max(5, self.size // 7)

        shadow_y = int(self.y + 5 + self.hover_offset * 0.5)
        shadow_surf = pygame.Surface((w, self.size), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (40, 20, 5, 120), (0, 0, w, self.size), border_radius=radius)
        surface.blit(shadow_surf, (draw_x, shadow_y))

        card_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        if self.flip_progress < 0.5:
            pygame.draw.rect(card_surf, (215, 140, 55), (0, 0, self.size, self.size), border_radius=radius)
            pygame.draw.rect(card_surf, (235, 170, 80), (4, 4, self.size - 8, self.size - 8), border_radius=max(2, radius - 2))
            c = self.size // 2
            r = self.size // 4
            pygame.draw.circle(card_surf, (195, 115, 40), (c, c), r)
            pygame.draw.circle(card_surf, (255, 220, 140), (c, c), r, max(2, self.size // 28))
            border_col = (255, 240, 0) if self.hint_timer > 0 else (140, 80, 25)
            border_w = max(3, self.size // 11) if self.hint_timer > 0 else max(2, self.size // 22)
            pygame.draw.rect(card_surf, border_col, (0, 0, self.size, self.size), border_w, border_radius=radius)
        else:
            pygame.draw.rect(card_surf, (255, 250, 240), (0, 0, self.size, self.size), border_radius=radius)
            pygame.draw.circle(card_surf, (245, 235, 215), (self.size // 2, self.size // 2), int(self.size * 0.36))
            draw_fruit_graphic(card_surf, self.fruit, self.size // 2, self.size // 2, max(6, int(self.size * 0.31)))
            border_col = (46, 204, 113) if self.matched else (195, 165, 130)
            border_w = max(3, self.size // 13) if self.matched else max(2, self.size // 22)
            pygame.draw.rect(card_surf, border_col, (0, 0, self.size, self.size), border_w, border_radius=radius)

        scaled = pygame.transform.smoothscale(card_surf, (w, self.size))
        surface.blit(scaled, (draw_x, draw_y))


class Game:

    def __init__(self):
        self.font = pygame.font.SysFont("arial", 18, bold=True)
        self.med_font = pygame.font.SysFont("arial", 26, bold=True)
        self.big_font = pygame.font.SysFont("arial", 48, bold=True)
        self.state = "menu"
        self.grid_size = 4
        self.best_scores = {4: 0, 6: 0, 8: 0, 10: 0}
        self.best_stars = {4: 0, 6: 0, 8: 0, 10: 0}
        self.level_cards = []
        self.particles = []
        self.float_texts = []
        self.clouds = [[random.randint(0, WIDTH), random.randint(30, 220), random.uniform(0.2, 0.6), random.randint(45, 75)] for _ in range(5)]
        self.setup_menu()

    def setup_menu(self):
        configs = [
            (4, "apple", WIDTH // 2 - 340, 290),
            (6, "watermelon", WIDTH // 2 + 20, 290),
            (8, "strawberry", WIDTH // 2 - 340, 460),
            (10, "pineapple", WIDTH // 2 + 20, 460),
        ]
        self.level_cards.clear()
        for sz, fr, x, y in configs:
            self.level_cards.append(LevelCardButton(x, y, 320, 135, sz, fr))

    def start_game(self, size):
        play_snd(SND_CLICK)
        self.grid_size = size
        self.state = "playing"
        self.cards = []
        self.selected = []
        self.particles.clear()
        self.float_texts.clear()
        self.moves = 0
        self.score = 0
        self.combo = 0
        self.peeks_left = 2
        self.hints_left = 3
        self.time_boosts = 2
        self.wait_time = 0

        self.max_time = float(TIME_LIMITS[size])
        self.time_left = self.max_time
        self.last_tick_sec = 999
        self.last_frame_tick = pygame.time.get_ticks()
        self.preview_until = self.last_frame_tick + 1800
        self.won = False
        self.lost = False

        self.btn_time = IconSpriteButton(WIDTH - 342, 12, 54, "clock", (40, 165, 135))
        self.btn_time.badge_count = self.time_boosts
        self.btn_peek = IconSpriteButton(WIDTH - 276, 12, 54, "eye", (145, 75, 190))
        self.btn_peek.badge_count = self.peeks_left
        self.btn_hint = IconSpriteButton(WIDTH - 210, 12, 54, "bulb", (230, 145, 25))
        self.btn_hint.badge_count = self.hints_left
        self.btn_restart = IconSpriteButton(WIDTH - 144, 12, 54, "reload", (55, 145, 205))
        self.btn_menu = IconSpriteButton(WIDTH - 78, 12, 54, "home", (215, 70, 65))

        self.btn_modal_again = IconSpriteButton(WIDTH // 2 - 80, HEIGHT // 2 + 95, 68, "reload", (46, 180, 95))
        self.btn_modal_menu = IconSpriteButton(WIDTH // 2 + 12, HEIGHT // 2 + 95, 68, "home", (215, 70, 65))

        pairs_needed = (size * size) // 2
        shuffled_fruits = FRUITS[:]
        random.shuffle(shuffled_fruits)
        chosen_fruits = [shuffled_fruits[i % len(shuffled_fruits)] for i in range(pairs_needed)]
        deck = chosen_fruits * 2
        random.shuffle(deck)

        gap = max(5, 16 - size)
        board_size = 715
        card_size = (board_size - (size - 1) * gap) // size
        start_x = (WIDTH - (size * card_size + (size - 1) * gap)) // 2
        start_y = 148 + (board_size - (size * card_size + (size - 1) * gap)) // 2

        for r in range(size):
            for c in range(size):
                x = start_x + c * (card_size + gap)
                y = start_y + r * (card_size + gap)
                fruit = deck.pop()
                self.cards.append(Card(x, y, card_size, fruit))

    def spawn_burst(self, card):
        cols = [(255, 215, 0), (46, 204, 113), (255, 100, 120), (255, 180, 50)]
        for _ in range(28):
            self.particles.append(Particle(card.rect.centerx, card.rect.centery, random.choice(cols)))

    def use_time_boost(self):
        if self.time_boosts > 0 and pygame.time.get_ticks() > self.preview_until:
            play_snd(SND_MATCH)
            self.time_boosts -= 1
            self.btn_time.badge_count = self.time_boosts
            self.time_left = min(self.max_time, self.time_left + 15.0)
            self.float_texts.append(FloatingText(WIDTH // 2, 95, "+15s TIME!", (80, 255, 140)))

    def use_peek(self):
        if self.peeks_left > 0 and pygame.time.get_ticks() > self.preview_until:
            play_snd(SND_CLICK)
            self.peeks_left -= 1
            self.btn_peek.badge_count = self.peeks_left
            self.preview_until = pygame.time.get_ticks() + 1400

    def use_hint(self):
        if self.hints_left > 0 and pygame.time.get_ticks() > self.preview_until:
            unmatched = [c for c in self.cards if not c.matched and not c.revealed]
            if len(unmatched) >= 2:
                play_snd(SND_CLICK)
                self.hints_left -= 1
                self.btn_hint.badge_count = self.hints_left
                target = unmatched[0]
                for c in unmatched[1:]:
                    if c.fruit == target.fruit:
                        target.hint_timer = 95
                        c.hint_timer = 95
                        break

    def calc_stars(self):
        ratio = self.time_left / self.max_time
        if ratio >= 0.45:
            return 3
        if ratio >= 0.20:
            return 2
        return 1

    def click(self, pos):
        if self.state == "menu":
            for lc in self.level_cards:
                if lc.rect.collidepoint(pos):
                    self.start_game(lc.grid_size)
                    break
        elif self.state == "playing":
            if self.won or self.lost:
                if self.btn_modal_again.rect.collidepoint(pos):
                    self.start_game(self.grid_size)
                elif self.btn_modal_menu.rect.collidepoint(pos):
                    play_snd(SND_CLICK)
                    self.state = "menu"
                return

            if self.btn_restart.rect.collidepoint(pos):
                self.start_game(self.grid_size)
                return
            if self.btn_menu.rect.collidepoint(pos):
                play_snd(SND_CLICK)
                self.state = "menu"
                return
            if self.btn_time.rect.collidepoint(pos):
                self.use_time_boost()
                return
            if self.btn_peek.rect.collidepoint(pos):
                self.use_peek()
                return
            if self.btn_hint.rect.collidepoint(pos):
                self.use_hint()
                return

            now = pygame.time.get_ticks()
            if now < self.preview_until:
                return

            if self.wait_time > 0:
                for c in self.selected:
                    c.revealed = False
                self.selected.clear()
                self.wait_time = 0

            if len(self.selected) >= 2:
                return

            for card in self.cards:
                if card.rect.collidepoint(pos) and not card.revealed and not card.matched:
                    play_snd(SND_FLIP)
                    card.revealed = True
                    card.hint_timer = 0
                    self.selected.append(card)
                    if len(self.selected) == 2:
                        self.moves += 1
                        c1, c2 = self.selected
                        if c1.fruit == c2.fruit:
                            c1.matched = True
                            c2.matched = True
                            self.combo += 1
                            pts = 100 * self.combo
                            self.score += pts
                            play_snd(SND_MATCH)
                            self.spawn_burst(c1)
                            self.spawn_burst(c2)
                            mid_x = (c1.rect.centerx + c2.rect.centerx) // 2
                            mid_y = (c1.rect.centery + c2.rect.centery) // 2

                            if self.combo > 1:
                                self.time_left = min(self.max_time, self.time_left + 2.0)
                                label = f"+{pts}  COMBO x{self.combo} (+2s!)"
                            else:
                                label = f"+{pts}"
                            self.float_texts.append(FloatingText(mid_x, mid_y, label, (255, 235, 60)))
                            self.selected.clear()

                            if all(c.matched for c in self.cards):
                                self.won = True
                                time_bonus = int(self.time_left) * 15
                                self.score += time_bonus
                                play_snd(SND_WIN)
                                stars = self.calc_stars()
                                if self.score > self.best_scores[self.grid_size]:
                                    self.best_scores[self.grid_size] = self.score
                                if stars > self.best_stars[self.grid_size]:
                                    self.best_stars[self.grid_size] = stars
                        else:
                            self.combo = 0
                            play_snd(SND_MISS)
                            self.wait_time = pygame.time.get_ticks()
                    break

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()
        dt = (now - getattr(self, "last_frame_tick", now)) / 1000.0
        self.last_frame_tick = now

        for cl in self.clouds:
            cl[0] += cl[2]
            if cl[0] > WIDTH + 100:
                cl[0] = -120

        if self.state == "playing":
            force_show = (now < self.preview_until) or self.lost

            if not self.won and not self.lost and now >= self.preview_until:
                self.time_left -= dt
                sec_int = int(math.ceil(self.time_left))
                if 0 < sec_int <= 10 and sec_int != self.last_tick_sec:
                    self.last_tick_sec = sec_int
                    play_snd(SND_TICK)

                if self.time_left <= 0:
                    self.time_left = 0
                    self.lost = True
                    play_snd(SND_LOSE)

            for card in self.cards:
                card.update(mouse_pos, force_show)

            for p in self.particles[:]:
                p.update()
                if p.life <= 0:
                    self.particles.remove(p)

            for ft in self.float_texts[:]:
                ft.update()
                if ft.life <= 0:
                    self.float_texts.remove(ft)

            if self.wait_time > 0 and now - self.wait_time > 650:
                for card in self.selected:
                    card.revealed = False
                self.selected.clear()
                self.wait_time = 0

    def draw_timer_bar(self, surface):
        bar_x, bar_y, bar_w, bar_h = 65, 80, WIDTH - 130, 26
        pygame.draw.rect(surface, (85, 48, 18), (bar_x - 4, bar_y - 4, bar_w + 8, bar_h + 8), border_radius=14)
        pygame.draw.rect(surface, (45, 25, 10), (bar_x, bar_y, bar_w, bar_h), border_radius=10)

        ratio = max(0.0, min(1.0, self.time_left / self.max_time))
        fill_w = int(bar_w * ratio)

        if ratio > 0.5:
            col = (55, 210, 85)
        elif ratio > 0.22:
            col = (245, 180, 30)
        else:
            flash = (pygame.time.get_ticks() // 180) % 2 == 0
            col = (245, 45, 45) if flash else (170, 25, 25)

        if fill_w > 6:
            pygame.draw.rect(surface, col, (bar_x, bar_y, fill_w, bar_h), border_radius=10)

        pygame.draw.circle(surface, (245, 200, 65), (bar_x + 8, bar_y + bar_h // 2), 18)
        pygame.draw.circle(surface, (120, 65, 15), (bar_x + 8, bar_y + bar_h // 2), 18, 3)
        pygame.draw.line(surface, (120, 65, 15), (bar_x + 8, bar_y + bar_h // 2), (bar_x + 8, bar_y + bar_h // 2 - 9), 3)
        pygame.draw.line(surface, (120, 65, 15), (bar_x + 8, bar_y + bar_h // 2), (bar_x + 15, bar_y + bar_h // 2), 3)

        t_str = f"{int(math.ceil(self.time_left))}s"
        txt = self.font.render(t_str, True, (255, 255, 255))
        surface.blit(txt, (bar_x + bar_w // 2 - txt.get_width() // 2, bar_y + 2))

    def draw(self, surface):
        if self.state == "menu":
            surface.blit(MENU_BG, (0, 0))
            for cx, cy, _, r in self.clouds:
                pygame.draw.circle(surface, (255, 255, 255), (int(cx), int(cy)), r)
                pygame.draw.circle(surface, (255, 255, 255), (int(cx - r * 0.6), int(cy + 8)), int(r * 0.75))
                pygame.draw.circle(surface, (255, 255, 255), (int(cx + r * 0.6), int(cy + 8)), int(r * 0.75))

            sign_rect = pygame.Rect(WIDTH // 2 - 280, 75, 560, 125)
            pygame.draw.rect(surface, (90, 50, 15), (sign_rect.x + 6, sign_rect.y + 8, sign_rect.w, sign_rect.h), border_radius=26)
            pygame.draw.rect(surface, (165, 100, 42), sign_rect, border_radius=26)
            pygame.draw.rect(surface, (110, 62, 22), sign_rect, 6, border_radius=26)

            shd = self.big_font.render("FRUIT MEMORY", True, (75, 40, 10))
            title = self.big_font.render("FRUIT MEMORY", True, (255, 235, 95))
            surface.blit(shd, (WIDTH // 2 - title.get_width() // 2 + 3, 110))
            surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 107))

            for lc in self.level_cards:
                sz = lc.grid_size
                lc.draw(surface, self.font, self.best_stars[sz], self.best_scores[sz])

        elif self.state == "playing":
            surface.blit(GAME_BG, (0, 0))

            hud_rect = pygame.Rect(35, 12, 535, 56)
            pygame.draw.rect(surface, (130, 75, 30), hud_rect, border_radius=16)
            pygame.draw.rect(surface, (245, 225, 185), (hud_rect.x + 4, hud_rect.y + 4, hud_rect.w - 8, hud_rect.h - 8), border_radius=12)

            stat = self.med_font.render(
                f"Score: {self.score}     Moves: {self.moves}     Combo: x{max(1, self.combo)}",
                True,
                (105, 55, 15),
            )
            surface.blit(stat, (hud_rect.x + 20, hud_rect.centery - stat.get_height() // 2))

            self.draw_timer_bar(surface)

            self.btn_time.draw(surface, self.font)
            self.btn_peek.draw(surface, self.font)
            self.btn_hint.draw(surface, self.font)
            self.btn_restart.draw(surface, self.font)
            self.btn_menu.draw(surface, self.font)

            for card in self.cards:
                card.draw(surface)

            for p in self.particles:
                p.draw(surface)

            for ft in self.float_texts:
                ft.draw(surface)

            if pygame.time.get_ticks() < self.preview_until and not self.won and not self.lost:
                banner = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 - 32, 340, 64)
                pygame.draw.rect(surface, (145, 85, 30), banner, border_radius=18)
                pygame.draw.rect(surface, (255, 225, 100), banner, 4, border_radius=18)
                m_txt = self.med_font.render("MEMORIZE CARDS!", True, (255, 245, 190))
                surface.blit(m_txt, (WIDTH // 2 - m_txt.get_width() // 2, HEIGHT // 2 - m_txt.get_height() // 2))

            if self.won or self.lost:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((20, 35, 15, 195))
                surface.blit(overlay, (0, 0))

                modal = pygame.Rect(WIDTH // 2 - 230, HEIGHT // 2 - 185, 460, 370)
                pygame.draw.rect(surface, (150, 90, 38), modal, border_radius=26)
                pygame.draw.rect(surface, (250, 238, 205), (modal.x + 10, modal.y + 10, modal.w - 20, modal.h - 20), border_radius=20)

                if self.won:
                    win = self.big_font.render("STAGE CLEAR!", True, (40, 165, 65))
                    surface.blit(win, (WIDTH // 2 - win.get_width() // 2, modal.y + 28))

                    stars = self.calc_stars()
                    for i in range(3):
                        scol = (255, 205, 0) if i < stars else (210, 195, 165)
                        draw_star(surface, WIDTH // 2 - 75 + i * 75, modal.y + 125, 28, scol)

                    s_txt = self.med_font.render(f"Final Score: {self.score}", True, (100, 55, 15))
                    m_txt = self.font.render(f"Moves: {self.moves}   |   Time Left: {int(self.time_left)}s", True, (130, 80, 35))
                else:
                    lose = self.big_font.render("TIME'S UP!", True, (215, 45, 45))
                    surface.blit(lose, (WIDTH // 2 - lose.get_width() // 2, modal.y + 32))

                    pygame.draw.circle(surface, (220, 65, 55), (WIDTH // 2, modal.y + 125), 34)
                    pygame.draw.circle(surface, (255, 255, 255), (WIDTH // 2, modal.y + 125), 34, 4)
                    pygame.draw.line(surface, (255, 255, 255), (WIDTH // 2, modal.y + 125), (WIDTH // 2, modal.y + 105), 4)
                    pygame.draw.line(surface, (255, 255, 255), (WIDTH // 2, modal.y + 125), (WIDTH // 2 + 14, modal.y + 125), 4)

                    s_txt = self.med_font.render(f"Score: {self.score}", True, (100, 55, 15))
                    m_txt = self.font.render("You ran out of time! Try again!", True, (165, 55, 40))

                surface.blit(s_txt, (WIDTH // 2 - s_txt.get_width() // 2, modal.y + 180))
                surface.blit(m_txt, (WIDTH // 2 - m_txt.get_width() // 2, modal.y + 225))

                self.btn_modal_again.draw(surface, self.font)
                self.btn_modal_menu.draw(surface, self.font)


def main():
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.state == "playing":
                    game.start_game(game.grid_size)
                elif event.key == pygame.K_m:
                    game.state = "menu"

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()