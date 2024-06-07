import pygame


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
        self.score = 0
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
