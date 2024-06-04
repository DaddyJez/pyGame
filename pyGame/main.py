import sys
import pygame
import sqlite3
import random


class Person:
    def __init__(self, x=200, y=245, speed=5, jump_count=8):
        self.x = x
        self.y = y
        self.speed = speed
        self.jump_count = jump_count
        self.is_jump = False
        self.player_rect = None
        self.key_down = pygame.key.get_pressed()
        self.player_anim_count = 0
        self.clip = 5
        self.go_right = [
            pygame.image.load('images/person/right/playerRight1.png').convert_alpha(),
            pygame.image.load('images/person/right/playerRight4.png').convert_alpha(),
            pygame.image.load('images/person/right/playerRight3.png').convert_alpha(),
            pygame.image.load('images/person/right/playerRight2.png').convert_alpha()
        ]
        self.go_left = [
            pygame.image.load('images/person/left/playerLeft1.png').convert_alpha(),
            pygame.image.load('images/person/left/playerLeft2.png').convert_alpha(),
            pygame.image.load('images/person/left/playerLeft3.png').convert_alpha(),
            pygame.image.load('images/person/left/playerLeft4.png').convert_alpha()
        ]

    def move(self):
        if self.key_down[pygame.K_LEFT] and self.x > 20:
            self.x -= self.speed
        elif self.key_down[pygame.K_RIGHT] and self.x < 640:
            self.x += self.speed

        if not self.is_jump:
            if self.key_down[pygame.K_UP]:
                self.is_jump = True
        else:
            if self.jump_count >= -8:
                if self.jump_count > 0:
                    self.y -= (self.jump_count ** 2) / 2
                elif self.jump_count < 0:
                    self.y += (self.jump_count ** 2) / 2

                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 8

    def animate(self, screen):
        if self.player_anim_count == 3:
            self.player_anim_count = 0
        else:
            self.player_anim_count += 1

        if self.key_down[pygame.K_LEFT]:
            screen.blit(self.go_left[self.player_anim_count], (self.x, self.y))
        else:
            screen.blit(self.go_right[self.player_anim_count], (self.x, self.y))


class DatabaseManager:
    def __init__(self, database):
        self.db = sqlite3.connect(database)
        self.logger = self.Logger()

    class Logger:
        def log(self, message):
            print(message)

    def write_score(self, nick, score_to_insert):
        cur = self.db.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS users
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nickname TEXT,
                        score INTEGER)''')

        cur.execute('SELECT score FROM users WHERE nickname = ?', (nick,))
        previous_score = cur.fetchone()

        if previous_score is None:
            cur.execute('INSERT INTO users (nickname, score) VALUES (?, ?)', (nick, score_to_insert))
        elif score_to_insert > previous_score[0]:
            cur.execute('UPDATE users SET score = ? WHERE nickname = ?', (score_to_insert, nick))

        self.db.commit()

    def get_top_players(self):
        cur = self.db.cursor()

        query = 'SELECT nickname, score FROM users ORDER BY score DESC LIMIT 5'

        cur.execute(query)
        top_players_list = cur.fetchall()

        self.logger.log("Retrieved top players from the database.")
        self.logger.log(top_players_list)

        self.db.commit()

        return top_players_list

    def close(self):
        self.db.commit()
        self.db.close()
        self.logger.log("Closed the database connection.")


clock = pygame.time.Clock()

key_down = None

pygame.init()
field = pygame.display.set_mode((680, 340))
pygame.display.set_caption("Brodilka")
icon = pygame.image.load('images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

background = pygame.image.load('images/bg1.png').convert()
menu_bg = pygame.image.load('images/bg_menu.png').convert()

game_font = pygame.font.Font('fonts/Jacquard12-Regular.ttf', 55)
name_font = pygame.font.Font('fonts/Kanit-Regular.ttf', 20)

start_label = game_font.render('Start', False, (168, 2, 2))
start_label_rect = start_label.get_rect(topleft=(140, 250))

lose_label = game_font.render('You lose :(', False, (168, 2, 2))
leads_label = game_font.render('Leaderboards:', False, (168, 2, 2))
restart_label = game_font.render('Restart', False, (168, 2, 2))
restart_label_rect = restart_label.get_rect(topleft=(140, 250))

db_manager = DatabaseManager('scores.db')
db_manager.write_score('vladik', 0)

leaderboard_labels = [
                            name_font.render(f"None", False, (168, 2, 2)),
                            name_font.render(f"None", False, (168, 2, 2)),
                            name_font.render(f"None", False, (168, 2, 2)),
                            name_font.render(f"None", False, (168, 2, 2)),
                            name_font.render(f"None", False, (168, 2, 2))
                        ]
top_players = db_manager.get_top_players()
for ranking, player in enumerate(top_players, start=1):
    leaderboard_labels[ranking - 1] = name_font.render(
        f'{ranking}.{player[0]}, Score: {player[1]}', False, (168, 2, 2))

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 3000)

shot = pygame.image.load('images/bullet.png').convert_alpha()
shots = []

enemy = pygame.image.load('images/enemy.png').convert_alpha()
enemy_list_in_game = []

background_x = 0

enemy_speed = 5

score_to_ins = 0
nickname = 'your nickname'
player = Person()
menu = 1
need_input = True
gameplay = False
running = True

while running:
    clock.tick(20)
    if menu == 0:
        field.blit(background, (background_x, 0))
        field.blit(background, (background_x + 680, 0))

        if gameplay:
            player.key_down = pygame.key.get_pressed()
            player.move()
            player.animate(field)
            player_rect = player.go_right[0].get_rect(topleft=(player.x, player.y))

            score_label = game_font.render(f"Your score: {player.score}", False, (168, 2, 2))
            field.blit(score_label, (200, 30))
            clip_label = name_font.render(f"Clip: {player.clip}", False, (168, 2, 2))
            field.blit(clip_label, (50, 50))
            name = name_font.render(f"{nickname}", False, (168, 2, 2))
            field.blit(name, (player.x - 20, player.y - 40))

            if enemy_list_in_game:
                for (i, el) in enumerate(enemy_list_in_game):
                    field.blit(enemy, el)
                    el.x -= enemy_speed

                    if el.x < -30:
                        enemy_list_in_game.pop(i)

                    if player_rect.colliderect(el):
                        db_manager.write_score(nickname, score_to_ins)
                        top_players = db_manager.get_top_players()
                        for ranking, player in enumerate(top_players, start=1):
                            leaderboard_labels[ranking-1] = name_font.render(
                                f'{ranking}.{player[0]}, Score: {player[1]}', False, (168, 2, 2))

                        gameplay = False

            key_down = pygame.key.get_pressed()

            background_x -= 2

            if background_x % 550 == 0 and player.clip < 5:
                player.clip += 1
            if background_x % 100 == 0:
                player.score += 1
                score_to_ins += 1
                if player.score >= 30:
                    gameplay = False
                    db_manager.write_score(nickname, score_to_ins)
                    menu = 2
                    top_players = db_manager.get_top_players()
                    for ranking, player in enumerate(top_players, start=1):
                        leaderboard_labels[ranking - 1] = name_font.render(
                            f'{ranking}.{player[0]}, Score: {player[1]}', False, (168, 2, 2))

            if background_x == -680:
                background_x = 0
                enemy_speed += 2

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
                                score_to_ins += 1
        else:
            description = name_font.render(f"your score is {score_to_ins}", False, (168, 2, 2))
            field.blit(menu_bg, (0, 0))
            field.blit(lose_label, (65, 35))
            field.blit(restart_label, restart_label_rect)
            field.blit(description, (155, 200))

            field.blit(leads_label, (385, 35))

            for i in range(5):
                field.blit(leaderboard_labels[i], (450, 100 + (i * 40)))

            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                player = Person()
                player.clip = 5
                player.x = 200
                player.y = 245
                player.score = 0
                score_to_ins = 0
                enemy_list_in_game.clear()
                shots.clear()
                enemy_speed = 5
                gameplay = True
    elif menu == 1:
        name = name_font.render(f"Enter nickname: {nickname}", False, (168, 2, 2))
        description = name_font.render("(ingame): get score 30 to win", False, (168, 2, 2))
        description2 = name_font.render("SPACE - shoot, ARROWS - go", False, (168, 2, 2))

        field.blit(menu_bg, (0, 0))
        field.blit(start_label, start_label_rect)
        field.blit(name, (65, 40))
        field.blit(description, (65, 80))
        field.blit(description2, (65, 200))

        field.blit(leads_label, (385, 35))

        for i in range(5):
            field.blit(leaderboard_labels[i], (450, 100 + (i * 40)))

        mouse = pygame.mouse.get_pos()
        if start_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            player = Person()
            player.clip = 5
            player.x = 200
            player.y = 245
            player.score = 0
            score_to_ins = 0
            enemy_list_in_game.clear()
            shots.clear()
            enemy_speed = 5
            gameplay = True
            menu = 0

    elif menu == 2:
        name = name_font.render(f"Great, {nickname}!", False, (168, 2, 2))
        description = name_font.render(f"your score is {score_to_ins}", False, (168, 2, 2))

        field.blit(menu_bg, (0, 0))
        field.blit(restart_label, restart_label_rect)
        field.blit(name, (65, 40))
        field.blit(description, (65, 80))

        field.blit(leads_label, (385, 35))

        for i in range(5):
            field.blit(leaderboard_labels[i], (450, 100 + (i * 40)))

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            player = Person()
            player.x = 200
            player.y = 245
            player.clip = 5
            player.score = 0
            score_to_ins = 0
            enemy_list_in_game.clear()
            shots.clear()
            enemy_speed = 5
            gameplay = True
            menu = 0

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if db_manager:
                db_manager.close()
            running = False
            pygame.quit()
            sys.exit()
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(random.randint(685, 1000), 235)))
            enemy_list_in_game.append(enemy.get_rect(topleft=(random.randint(1000, 1500), 175)))
        if gameplay and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.clip > 0:
            shots.append(shot.get_rect(topleft=(player.x + 20, player.y + 10)))
            player.clip -= 1
        if menu == 1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                nickname = nickname[0:-1]
            else:
                if len(nickname) <= 20:
                    nickname += event.unicode
