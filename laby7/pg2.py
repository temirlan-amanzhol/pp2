import pygame
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Music Player")

img = pygame.image.load("C:/Users/ASUS/Downloads/bob/laby7/mainpage.png").convert_alpha()
img = pygame.transform.scale(img, (300, 200))

folder = r"C:\Users\ASUS\Downloads\bob\laby7"

tracks = [f for f in os.listdir(folder) if f.endswith(".mp3")]
if not tracks:
    print("No music found!")
    exit()

current = 0

def play():
    pygame.mixer.music.load(os.path.join(folder, tracks[current]))
    pygame.mixer.music.play()
    print(f"Playing: {tracks[current]}")

def stop():
    pygame.mixer.music.stop()
    print("Music stopped")

def next_track():
    global current
    current = (current + 1) % len(tracks)
    play()

def prev_track():
    global current
    current = (current - 1) % len(tracks)
    play()

play()

running = True
while running:
    screen.blit(img, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    print("Paused")
                else:
                    pygame.mixer.music.unpause()
                    print("Resumed")
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_d:
                next_track()
            elif event.key == pygame.K_a:
                prev_track()

pygame.quit()