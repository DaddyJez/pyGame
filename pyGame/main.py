import sys
import pygame
import random

from definitions import show_leads, config_leads, menu_win, menu_start, menu_loss
import nums_constants
from person_class import Person
from database_class import DatabaseManager


def default_values():
    global player
    global menu
    player = Person()
    player.clip = 5
    player.x = nums_constants.DEFAULT_X
    player.y = nums_constants.DEFAULT_Y
    player.score = 0
    nums_constants.score_to_ins = 0
    enemy_list_in_game.clear()
    shots.clear()
    nums_constants.enemy_speed = 5
    menu = nums_constants.MENU_PLAY


clock = pygame.time.Clock()

key_down = None

pygame.init()
field = pygame.display.set_mode((680, 340))
pygame.display.set_caption("DONT DIE!!!")

ICON = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load('images/bg1.png').convert()
MENU_BG = pygame.image.load('images/bg_menu.png').convert()

GAME_FONT = pygame.font.Font('fonts/Jacquard12-Regular.ttf', 55)
NAME_FONT = pygame.font.Font('fonts/Kanit-Regular.ttf', 20)

START_LABEL = GAME_FONT.render('Start', False, (168, 2, 2))
START_LABEL_RECT = START_LABEL.get_rect(topleft=(140, 250))

lose_label = GAME_FONT.render('You lose :(', False, (168, 2, 2))
leads_label = GAME_FONT.render('Leaderboards:', False, (168, 2, 2))
RESTART_LABEL = GAME_FONT.render('Restart', False, (168, 2, 2))
RESTART_LABEL_RECT = RESTART_LABEL.get_rect(topleft=(140, 250))

db_manager = DatabaseManager('scores.db')
db_manager.write_score('vladik', 0)

leaderboard_labels = [
                            NAME_FONT.render(f"None", False, (168, 2, 2)),
                            NAME_FONT.render(f"None", False, (168, 2, 2)),
                            NAME_FONT.render(f"None", False, (168, 2, 2)),
                            NAME_FONT.render(f"None", False, (168, 2, 2)),
                            NAME_FONT.render(f"None", False, (168, 2, 2))
                        ]
config_leads(db_manager, nums_constants.nickname,
             nums_constants.score_to_ins, leaderboard_labels, NAME_FONT)

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 3000)

shot = pygame.image.load('images/bullet.png').convert_alpha()
shots = []

enemy = pygame.image.load('images/enemy.png').convert_alpha()
enemy_list_in_game = []

player = Person()
menu = nums_constants.MENU_MAIN

SCORE_TO_WIN = 30

while nums_constants.running:
    clock.tick(20)
    if menu == nums_constants.MENU_PLAY:
        field.blit(BACKGROUND, (nums_constants.background_x, 0))
        field.blit(BACKGROUND, (nums_constants.background_x + 680, 0))

        player.key_down = pygame.key.get_pressed()
        player.move()
        player.animate(field)
        player_rect = player.go_right[0].get_rect(topleft=(player.x, player.y))

        score_label = GAME_FONT.render(f"Your score: {player.score}", False, (168, 2, 2))
        field.blit(score_label, (200, 30))
        clip_label = NAME_FONT.render(f"Clip: {player.clip}", False, (168, 2, 2))
        field.blit(clip_label, (50, 50))
        name = NAME_FONT.render(f"{nums_constants.nickname}", False, (168, 2, 2))
        field.blit(name, (player.x - 20, player.y - 40))

        if enemy_list_in_game:
            for (i, el) in enumerate(enemy_list_in_game):
                field.blit(enemy, el)
                el.x -= nums_constants.enemy_speed

                if el.x < -30:
                    enemy_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    config_leads(db_manager, nums_constants.nickname,
                                 nums_constants.score_to_ins, leaderboard_labels, NAME_FONT)

                    menu = nums_constants.MENU_LOSE

        key_down = pygame.key.get_pressed()

        nums_constants.background_x -= 2

        if nums_constants.background_x == -500 or nums_constants.background_x == -200:
            print(f"Restored at {nums_constants.background_x}")
            if player.clip < 5:
                player.clip += 1
        if nums_constants.background_x % 100 == 0:
            player.score += 1
            nums_constants.score_to_ins += 1
            if player.score >= SCORE_TO_WIN:
                config_leads(db_manager, nums_constants.nickname,
                             nums_constants.score_to_ins, leaderboard_labels, NAME_FONT)

                menu = nums_constants.MENU_WIN

        if nums_constants.background_x == -680:
            nums_constants.background_x = 0
            nums_constants.enemy_speed += 2

        if shots:
            for (i, el) in enumerate(shots):
                field.blit(shot, (el.x, el.y))
                el.x += 25

                if el.x > 710:
                    shots.pop(i)

                if enemy_list_in_game:
                    for (j, element) in enumerate(enemy_list_in_game):
                        if el.colliderect(element):
                            enemy_list_in_game.pop(j)
                            shots.pop(i)
                            nums_constants.score_to_ins += 1

    elif menu == nums_constants.MENU_MAIN:
        name = NAME_FONT.render(f"Enter nickname: {nums_constants.nickname}", False, (168, 2, 2))
        description = NAME_FONT.render("(in game): get score 30 to win", False, (168, 2, 2))
        description2 = NAME_FONT.render("SPACE - shoot, ARROWS - go", False, (168, 2, 2))

        menu_start(field, MENU_BG, RESTART_LABEL, RESTART_LABEL_RECT, name, description, description2, leads_label)

        show_leads(field, leaderboard_labels)

        mouse = pygame.mouse.get_pos()
        if START_LABEL_RECT.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            default_values()

    elif menu == nums_constants.MENU_WIN:
        name = NAME_FONT.render(f"Great, {nums_constants.nickname}!", False, (168, 2, 2))
        description = NAME_FONT.render(f"your score is {nums_constants.score_to_ins}", False, (168, 2, 2))

        menu_win(field, MENU_BG, RESTART_LABEL, RESTART_LABEL_RECT, name, description, leads_label)

        show_leads(field, leaderboard_labels)

        mouse = pygame.mouse.get_pos()
        if RESTART_LABEL_RECT.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            default_values()
    elif menu == nums_constants.MENU_LOSE:
        description = NAME_FONT.render(f"your score is {nums_constants.score_to_ins}", False, (168, 2, 2))

        menu_loss(field, MENU_BG, RESTART_LABEL, RESTART_LABEL_RECT, description, lose_label, leads_label)

        show_leads(field, leaderboard_labels)

        mouse = pygame.mouse.get_pos()
        if RESTART_LABEL_RECT.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            default_values()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if db_manager:
                db_manager.close()
            nums_constants.running = False
            pygame.quit()
            sys.exit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(random.randint(685, 1000), 235)))
            enemy_list_in_game.append(enemy.get_rect(topleft=(random.randint(1000, 1500), 175)))
        if (menu == nums_constants.MENU_PLAY and event.type == pygame.KEYDOWN and
                event.key == pygame.K_SPACE and player.clip > 0):
            shots.append(shot.get_rect(topleft=(player.x + 20, player.y + 10)))
            player.clip -= 1
        if menu == nums_constants.MENU_MAIN and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                nums_constants.nickname = nums_constants.nickname[0:-1]
            else:
                if len(nums_constants.nickname) <= 20:
                    nums_constants.nickname += event.unicode
