#print('Hello World!')

import pygame, random, os
from pygame.constants import QUIT, K_UP, K_RIGHT, K_DOWN, K_LEFT
from pygame.mask import from_surface
pygame.init()

#display setup
HEIGHT = 800
WIDTH = 1200
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = pygame.time.Clock()
FONT = pygame.font.SysFont("Verdana", 20)
FONT_GAME_OVER = pygame.font.SysFont("Verdana", 80)
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

def show_game_over():
    text = FONT_GAME_OVER.render("GAME OVER", True, COLOR_RED)
    main_display.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))



#colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

#player setup
#player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_mask = from_surface(player)
#        pygame.Surface (player_size)
#player.fill(COLOR_WHITE)
player_rect = player.get_rect(topleft=(85, HEIGHT//3))
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

CHANGE_IMAGE = pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE, 200)
image_index = 0

# Enemies
def create_enemy():
    #enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    #       pygame.Surface(enemy_size)
    #enemy.fill(COLOR_RED)
    enemy_rect = pygame.Rect(WIDTH, random.randint(80, HEIGHT-80), enemy.get_width(), enemy.get_height())
#                                                                  *enemy_size)
    enemy_move = [random.randint(-9, -5), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

# Bonuses
def create_bonus():
    #bonus_size = (25, 25)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    #       pygame.Surface(bonus_size)
    #bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(185, WIDTH-185), -298, bonus.get_width(), bonus.get_height()) 
#                                                               *bonus_size)
    bonus_move = [0, random.randint(3, 5)]
    return [bonus, bonus_rect, bonus_move]

def get_bonus_box(bonus_rect):
    box_height = bonus_rect.height // 7
    box_y = bonus_rect.bottom - box_height
    return pygame.Rect(bonus_rect.x, box_y, bonus_rect.width, box_height)

score = 0

CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []

# Common
playing = True
game_over = False

while playing:
    FPS.tick(120)
        
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])).convert_alpha()
            player_mask = from_surface(player)

    if game_over:
        show_game_over()
        pygame.display.flip()
        pygame.time.wait(2000)
        playing = False
        break

    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    

    # player movements
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom <= HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right <= WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)


    for enemy in enemies:
        enemy_mask = from_surface(enemy[0])
        offset = (enemy[1].x - player_rect.x, enemy[1].y - player_rect.y)

        if player_mask.overlap(enemy_mask, offset):
            game_over = True

        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        # if player_rect.colliderect(enemy[1]):
        #     playing = False



    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        bonus_box = get_bonus_box(bonus[1])
        if player_rect.colliderect(bonus_box):
            score += 1
            bonuses.pop(bonuses.index(bonus))

        # if player_rect.colliderect(bonus[1]):
        #     score += 1
        #     bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)
    pygame.display.flip()
    #print(len(bonuses))

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top >= HEIGHT:
            bonuses.pop(bonuses.index(bonus))