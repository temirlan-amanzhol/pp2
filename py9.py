import sys
import random
import pygame

pygame.init()

# --------- GLOBAL SETTINGS ---------
W, H = 640, 800
FPS = 60

SCREEN = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont(None, 24)
FONT_BIG = pygame.font.SysFont(None, 40, bold=True)

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (120, 120, 120)
RED    = (220, 60,  60)
GREEN  = (60,  200, 60)
BLUE   = (60,  120, 220)
YELLOW = (240, 200, 0)


# --------- BASE SCENE ---------
class Scene:
    def handle(self, events): ...
    def update(self): ...
    def draw(self, surface): ...


def quit_game():
    pygame.quit()
    sys.exit()


def draw_button(surface, rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = WHITE if rect.collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=10)
    label = FONT_BIG.render(text, True, BLACK)
    surface.blit(label, label.get_rect(center=rect.center))



# --------- MENU ---------
class Menu(Scene):
    def __init__(self, switch_scene):
        self.switch_scene = switch_scene
        x = W // 2 - 160
        self.buttons = {
            "Racer": pygame.Rect(x, 280, 320, 70),
            "Snake": pygame.Rect(x, 370, 320, 70),
            "Paint": pygame.Rect(x, 460, 320, 70),
            "Quit":  pygame.Rect(x, 550, 320, 70),
        }

    def handle(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for name, rect in self.buttons.items():
                    if rect.collidepoint(e.pos):
                        if name == "Racer":
                            self.switch_scene(Racer(self.switch_scene))
                        elif name == "Snake":
                            self.switch_scene(Snake(self.switch_scene))
                        elif name == "Paint":
                            self.switch_scene(Paint(self.switch_scene))
                        elif name == "Quit":
                            quit_game()

    def draw(self, surface):
       

        # central panel
        panel = pygame.Rect(W // 2 - 230, 200, 460, 460)
        card = pygame.Surface(panel.size, pygame.SRCALPHA)
        pygame.draw.rect(card, (0, 0, 0, 160), card.get_rect(), border_radius=25)
        surface.blit(card, panel.topleft)

        title = FONT_BIG.render("Mini Game Hub", True, WHITE)
        surface.blit(title, title.get_rect(center=(W // 2, 240)))

        for name, rect in self.buttons.items():
            draw_button(surface, rect, name)

        # tips bottom bar
        tips_panel = pygame.Rect(0, H - 90, W, 90)
        tips_surf = pygame.Surface(tips_panel.size, pygame.SRCALPHA)
        pygame.draw.rect(tips_surf, (0, 0, 0, 150),
                         tips_surf.get_rect())
        surface.blit(tips_surf, tips_panel.topleft)

        tips = [
            "Racer: arrows",
            "Snake: arrows",
            "Paint: tools on the left, palette below",
            "ESC in game: back to menu",
        ]
        for i, text in enumerate(tips):
            surface.blit(FONT.render(text, True, WHITE),
                         (20, H - 80 + i * 20))


# --------- RACER ---------
class Racer(Scene):
    ROAD_WIDTH = 280
    PLAYER_SPEED = 7
    BASE_ENEMY_SPEED = 6
    COINS_FOR_SPEED_UP = 8
    ENEMY_SIZE = (40, 70)
    PLAYER_SIZE = (40, 70)
    COIN_SIZE = 16
    COIN_VALUES = (1, 2, 5)

    def __init__(self, switch_scene):
        self.switch_scene = switch_scene

        self.road_rect = pygame.Rect(
            W // 2 - self.ROAD_WIDTH // 2, 0, self.ROAD_WIDTH, H
        )
        self.player_rect = pygame.Rect(
            W // 2 - self.PLAYER_SIZE[0] // 2,
            H - 120,
            *self.PLAYER_SIZE,
        )

        self.enemy_speed = self.BASE_ENEMY_SPEED
        self.score = 0
        self.dead = False

        self.enemies = [self._new_enemy(-random.randint(50, 500)) for _ in range(4)]
        self.coins = [self._new_coin(-random.randint(60, 600)) for _ in range(4)]

    def _new_enemy(self, start_y):
        x = random.randrange(self.road_rect.left,
                             self.road_rect.right - self.ENEMY_SIZE[0], 50)
        return pygame.Rect(x, start_y, *self.ENEMY_SIZE)

    def _new_coin(self, start_y):
        x = random.randint(self.road_rect.left + 15,
                           self.road_rect.right - 15)
        rect = pygame.Rect(x, start_y, self.COIN_SIZE, self.COIN_SIZE)
        value = random.choice(self.COIN_VALUES)
        return [rect, value]

    def handle(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.switch_scene(Menu(self.switch_scene))

    def _move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_rect.x -= self.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player_rect.x += self.PLAYER_SPEED
        self.player_rect.clamp_ip(self.road_rect.inflate(-10, 0))

    def _update_enemies(self):
        for enemy in self.enemies:
            enemy.y += self.enemy_speed
            if enemy.y > H:
                enemy.y = -random.randint(80, 300)
                enemy.x = random.randrange(
                    self.road_rect.left,
                    self.road_rect.right - self.ENEMY_SIZE[0],
                    50,
                )
            if enemy.colliderect(self.player_rect):
                self.dead = True

    def _update_coins(self):
        for coin in self.coins:
            rect, val = coin
            rect.y += self.enemy_speed
            if rect.y > H:
                coin[:] = self._new_coin(-random.randint(120, 400))
                rect, val = coin
            if rect.colliderect(self.player_rect):
                self.score += val
                coin[:] = self._new_coin(-random.randint(120, 400))

    def _update_speed(self):
        self.enemy_speed = self.BASE_ENEMY_SPEED + self.score // self.COINS_FOR_SPEED_UP

    def update(self):
        if self.dead:
            return
        self._move_player()
        self._update_enemies()
        self._update_coins()
        self._update_speed()

    def draw(self, surface):
        surface.fill((20, 140, 20))
        pygame.draw.rect(surface, (60, 60, 60), self.road_rect)

        for y in range(-30, H, 70):
            pygame.draw.rect(surface, WHITE,
                             (W // 2 - 5, y, 10, 40), border_radius=6)

        pygame.draw.rect(surface, BLUE, self.player_rect, border_radius=6)
        for e in self.enemies:
            pygame.draw.rect(surface, RED, e, border_radius=6)

        for rect, val in self.coins:
            if val == 1:
                col = (230, 230, 0)
            elif val == 2:
                col = (230, 160, 0)
            else:
                col = (230, 100, 0)
            pygame.draw.circle(surface, col, rect.center, 8)

        surface.blit(
            FONT_BIG.render(
                f"Coins: {self.score}  Speed: {self.enemy_speed}", True, WHITE
            ),
            (12, 12),
        )
        if self.dead:
            msg = FONT_BIG.render("CRASH! ESC for menu", True, WHITE)
            surface.blit(msg, (W // 2 - 160, H // 2))


# --------- SNAKE ---------
class Snake(Scene):
    GRID = 20
    BASE_SPEED = 6
    FOOD_LIFE_MS = 4000
    FOOD_WEIGHTS = (1, 2, 3)

    def __init__(self, switch_scene):
        self.switch_scene = switch_scene
        self.cols = W // self.GRID
        self.rows = (H - 60) // self.GRID
        self.reset()

    def reset(self):
        self.body = [(self.cols // 2, self.rows // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.level = 1

        self.food_pos = None
        self.food_weight = 1
        self.food_timer = 0

        self.time_acc = 0
        self._spawn_food()

    def _spawn_food(self):
        while True:
            pos = (random.randrange(self.cols), random.randrange(self.rows))
            if pos not in self.body:
                self.food_pos = pos
                self.food_weight = random.choice(self.FOOD_WEIGHTS)
                self.food_timer = self.FOOD_LIFE_MS
                return

    def handle(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.switch_scene(Menu(self.switch_scene))
                if e.key in (pygame.K_LEFT, pygame.K_a) and self.direction != (1, 0):
                    self.direction = (-1, 0)
                if e.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != (-1, 0):
                    self.direction = (1, 0)
                if e.key in (pygame.K_UP, pygame.K_w) and self.direction != (0, 1):
                    self.direction = (0, -1)
                if e.key in (pygame.K_DOWN, pygame.K_s) and self.direction != (0, -1):
                    self.direction = (0, 1)

    def update(self):
        dt = CLOCK.get_time()
        self.time_acc += dt
        self.food_timer -= dt
        if self.food_timer <= 0:
            self._spawn_food()

        step_ms = int(1000 / (self.BASE_SPEED + self.level * 2))
        if self.time_acc < step_ms:
            return
        self.time_acc = 0

        hx = self.body[0][0] + self.direction[0]
        hy = self.body[0][1] + self.direction[1]
        new_head = (hx, hy)

        if (
            not (0 <= hx < self.cols)
            or not (0 <= hy < self.rows)
            or new_head in self.body
        ):
            self.reset()
            return

        self.body.insert(0, new_head)

        if new_head == self.food_pos:
            self.score += self.food_weight
            if self.score % 4 == 0:
                self.level += 1
            self._spawn_food()
        else:
            self.body.pop()

    def draw(self, surface):
        surface.fill((18, 18, 22))
        pygame.draw.rect(surface, GRAY, (0, 0, W, 60), 2)

        info = f"Score:{self.score}  Lvl:{self.level}  Food:{self.food_weight}"
        surface.blit(FONT_BIG.render(info, True, WHITE), (12, 12))

        pygame.draw.rect(surface, (26, 26, 30), (0, 60, W, H - 60))

        fx, fy = self.food_pos
        if self.food_weight == 1:
            col = (80, 220, 80)
        elif self.food_weight == 2:
            col = (220, 220, 80)
        else:
            col = (220, 120, 80)
        pygame.draw.rect(
            surface,
            col,
            (fx * self.GRID + 2, 60 + fy * self.GRID + 2,
             self.GRID - 4, self.GRID - 4),
            border_radius=4,
        )

        for i, (x, y) in enumerate(self.body):
            c = (0, 200, 220) if i == 0 else (180, 240, 255)
            pygame.draw.rect(
                surface,
                c,
                (x * self.GRID + 2, 60 + y * self.GRID + 2,
                 self.GRID - 4, self.GRID - 4),
                border_radius=6,
            )


# --------- PAINT ---------
class Paint(Scene):
    BRUSH_MIN = 1
    BRUSH_MAX = 60
    TOP_BAR = 60
    SIDE_BAR = 90
    BOTTOM_BAR = 70

    def __init__(self, switch_scene):
        self.switch_scene = switch_scene

        canvas_w = W - self.SIDE_BAR - 20
        canvas_h = H - self.TOP_BAR - self.BOTTOM_BAR - 20
        self.canvas_pos = (self.SIDE_BAR + 10, self.TOP_BAR + 10)
        self.canvas = pygame.Surface((canvas_w, canvas_h))
        self.canvas.fill(WHITE)
        self.canvas_rect = pygame.Rect(self.canvas_pos, self.canvas.get_size())

        self.mode = "pen"
        self.color = BLACK
        self.brush = 5
        self.drawing = False
        self.start = None

        self.palette_colors = [
            BLACK, RED, GREEN, BLUE,
            YELLOW, (0, 200, 200),
            (200, 0, 200), (160, 160, 160)
        ]

        # tools on the left
        self.tool_defs = [
            ("pen", "Pen"),
            ("rect", "Rect"),
            ("circle", "Circ"),
            ("square", "Sq"),
            ("rt", "RT"),
            ("eq", "Eq"),
            ("rh", "Rh"),
            ("eraser", "Erase"),
        ]
        self.tool_buttons = []
        y = self.TOP_BAR + 10
        for mode, label in self.tool_defs:
            r = pygame.Rect(10, y, self.SIDE_BAR - 20, 40)
            self.tool_buttons.append((mode, label, r))
            y += 48

        # palette at bottom
        self.palette_buttons = []
        base_y = H - self.BOTTOM_BAR + 15
        x0 = self.SIDE_BAR + 20
        for i, c in enumerate(self.palette_colors):
            r = pygame.Rect(x0 + i * 40, base_y, 32, 32)
            self.palette_buttons.append((c, r))

    # ---- helpers ----
    def _to_canvas(self, pos):
        return pos[0] - self.canvas_rect.x, pos[1] - self.canvas_rect.y

    def _pick_tool(self, pos):
        for mode, label, rect in self.tool_buttons:
            if rect.collidepoint(pos):
                self.mode = mode
                return True
        return False

    def _pick_color(self, pos):
        for color, rect in self.palette_buttons:
            if rect.collidepoint(pos):
                self.color = color
                return True
        return False

    # ---- events ----
    def handle(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                quit_game()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.switch_scene(Menu(self.switch_scene))
                if e.key == pygame.K_c:
                    self.canvas.fill(WHITE)

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self._pick_tool(e.pos) or self._pick_color(e.pos):
                        continue
                    if self.canvas_rect.collidepoint(e.pos):
                        self.drawing = True
                        self.start = self._to_canvas(e.pos)
                elif e.button in (4, 5):
                    if e.button == 4:
                        self.brush = min(self.BRUSH_MAX, self.brush + 1)
                    else:
                        self.brush = max(self.BRUSH_MIN, self.brush - 1)

            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if self.drawing and self.canvas_rect.collidepoint(e.pos):
                    end = self._to_canvas(e.pos)
                    self._finish_shape(self.start, end)
                self.drawing = False

            if e.type == pygame.MOUSEMOTION and self.drawing:
                if self.mode in ("pen", "eraser") and self.canvas_rect.collidepoint(e.pos):
                    end = self._to_canvas(e.pos)
                    col = WHITE if self.mode == "eraser" else self.color
                    pygame.draw.line(self.canvas, col, self.start, end, self.brush)
                    self.start = end

    def _finish_shape(self, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]

        if self.mode == "rect":
            r = pygame.Rect(min(a[0], b[0]), min(a[1], b[1]), abs(dx), abs(dy))
            pygame.draw.rect(self.canvas, self.color, r, self.brush)

        elif self.mode == "circle":
            r = int((dx * dx + dy * dy) ** 0.5)
            pygame.draw.circle(self.canvas, self.color, a, r, self.brush)

        elif self.mode == "square":
            side = min(abs(dx), abs(dy))
            r = pygame.Rect(a[0], a[1],
                            side * (1 if dx >= 0 else -1),
                            side * (1 if dy >= 0 else -1))
            r.normalize()
            pygame.draw.rect(self.canvas, self.color, r, self.brush)

        elif self.mode == "rt":
            p1 = a
            p2 = (b[0], a[1])
            p3 = (a[0], b[1])
            pygame.draw.polygon(self.canvas, self.color, (p1, p2, p3), self.brush)

        elif self.mode == "eq":
            side = min(abs(dx), abs(dy))
            x, y = a
            h = int(side * 3 ** 0.5 / 2)
            p1 = (x, y + side)
            p2 = (x + side, y + side)
            p3 = (x + side // 2, y + side - h)
            pygame.draw.polygon(self.canvas, self.color, (p1, p2, p3), self.brush)

        elif self.mode == "rh":
            cx = (a[0] + b[0]) // 2
            cy = (a[1] + b[1]) // 2
            hx = abs(dx) // 2
            hy = abs(dy) // 2
            pts = ((cx, cy - hy), (cx + hx, cy),
                   (cx, cy + hy), (cx - hx, cy))
            pygame.draw.polygon(self.canvas, self.color, pts, self.brush)

    # ---- draw ----
    def draw(self, s):
        s.fill((25, 25, 32))

        # top bar
        pygame.draw.rect(s, (30, 30, 38), (0, 0, W, self.TOP_BAR))
        title = "Paint   ESC:Menu   C:Clear"
        s.blit(FONT_BIG.render(title, True, WHITE),
               (self.SIDE_BAR + 20, 15))

        # left tools
        pygame.draw.rect(s, (20, 20, 26),
                         (0, self.TOP_BAR, self.SIDE_BAR, H))
        for mode, label, rect in self.tool_buttons:
            active = (mode == self.mode)
            bg = (45, 45, 60) if active else (34, 34, 46)
            pygame.draw.rect(s, bg, rect, border_radius=8)
            border_col = (240, 200, 0) if active else (0, 0, 0)
            pygame.draw.rect(s, border_col, rect, 2, border_radius=8)
            txt = FONT.render(label, True, WHITE)
            s.blit(txt, txt.get_rect(center=rect.center))

        # bottom palette
        pygame.draw.rect(s, (20, 20, 26),
                         (0, H - self.BOTTOM_BAR, W, self.BOTTOM_BAR))
        for color, rect in self.palette_buttons:
            pygame.draw.rect(s, color, rect, border_radius=6)
            border_col = WHITE if color == self.color else BLACK
            pygame.draw.rect(s, border_col, rect, 2, border_radius=6)

        # brush preview
        bx = W - 120
        by = H - self.BOTTOM_BAR // 2
        pygame.draw.circle(s, self.color, (bx, by), max(3, self.brush // 2))
        s.blit(FONT.render(f"size: {self.brush}", True, WHITE),
               (bx + 20, by - 10))

        # canvas frame
        frame = self.canvas_rect.inflate(4, 4)
        pygame.draw.rect(s, (18, 18, 24), frame, border_radius=10)
        s.blit(self.canvas, self.canvas_pos)


# --------- MAIN LOOP ---------
def main():
    current = {"scene": None}

    def switch(scene):
        current["scene"] = scene

    switch(Menu(switch))

    while True:
        events = pygame.event.get()
        current["scene"].handle(events)
        if hasattr(current["scene"], "update"):
            current["scene"].update()
        current["scene"].draw(SCREEN)

        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
