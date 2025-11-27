import psycopg2
import json

conn = psycopg2.connect(
    dbname="phonebook",     # или другая твоя база
    user="postgres",
    password="moiponos228",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
def get_or_create_user(username: str):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]          # user_id

    cursor.execute(
        "INSERT INTO users (username) VALUES (%s) RETURNING id",
        (username,)
    )
    user_id = cursor.fetchone()[0]
    return user_id
def get_current_level_and_score(user_id: int):
    cursor.execute(
        """
        SELECT level, score
        FROM user_score
        WHERE user_id = %s
        ORDER BY level DESC
        LIMIT 1
        """,
        (user_id,)
    )
    row = cursor.fetchone()
    if row:
        level, score = row
        return level, score
    else:
        return 1, 0
def save_game_state(user_id: int, level: int, score: int, state: dict):
    state_json = json.dumps(state)

    # Если запись для этого уровня уже есть — обновляем, иначе создаём
    cursor.execute(
        """
        INSERT INTO user_score (user_id, level, score, game_state)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id, level)
        DO UPDATE
        SET score = EXCLUDED.score,
            game_state = EXCLUDED.game_state,
            updated_at = NOW()
        """,
        (user_id, level, score, state_json)
    )
def login_screen():
    username = input("Enter your username: ")
    user_id = get_or_create_user(username)

    level, score = get_current_level_and_score(user_id)
    print(f"Welcome, {username}!")
    print(f"Your current level: {level}, last score: {score}")

    return user_id, level, score

import pygame
from pygame.locals import *

def run_game():
    user_id, level, start_score = login_screen()

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    score = start_score
    running = True
    paused = False

    # Пример состояния игры (ты заполняешь из своего кода)
    game_state = {
        "snake": [(10, 10), (10, 11), (10, 12)],
        "direction": "RIGHT",
        "food": (15, 15),
        "speed": 10 + 2 * (level - 1)   # разные скорости по уровням
    }

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            # Пример: P — пауза и сохранение
            if event.type == KEYDOWN:
                if event.key == K_p:
                    paused = not paused
                    if paused:
                        # Сохранение при постановке на паузу
                        save_game_state(user_id, level, score, game_state)
                        print("Game paused and state saved")

                # здесь меняешь направление змейки и т.п.

        if paused:
            clock.tick(5)
            continue

        # ===== твоя логика змейки =====
        # 1) двигаем змейку
        # 2) проверяем столкновения со стенами (зависят от level)
        # 3) если съели еду → score += 10, возможно level += 1
        # 4) обновляем game_state (координаты змейки, еды и т.д.)
        # ===============================

        screen.fill((0, 0, 0))
        # рисуешь змейку, стены, еду и т.д.
        pygame.display.flip()
        clock.tick(game_state["speed"])

    pygame.quit()
    cursor.close()
    conn.close()
