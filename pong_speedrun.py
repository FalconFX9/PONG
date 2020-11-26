"""
Made pong in 23min04s680ms
"""
import pygame
import random

display = pygame.display.set_mode((1000, 800))
WHITE = (255, 255, 255)
start = [-4, 4]
score = [0, 0]


class Paddle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 100))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

        self.speed_y = 0

    def update(self):
        if (self.rect.y > 0 > self.speed_y) or (self.rect.bottom < 800 and self.speed_y > 0):
            self.rect.y += self.speed_y


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()

        self.speed_x = 0
        self.speed_y = 0

        self.paddles = None
        self.score = None

    def update(self):
        if (self.rect.top < 0) or self.rect.bottom >= 800:
            self.speed_y *= -1

        if self.rect.x <= 0 or self.rect.right >= 1000:
            if self.speed_x > 0:
                score[0] += 1
            else:
                score[1] += 1
            reset_ball(self)

        self.rect.x += self.speed_x
        collision = pygame.sprite.spritecollide(self, self.paddles, False)
        if collision:
            self.speed_x *= -1

        self.rect.y += self.speed_y


def point(score_internal):
    font = pygame.font.SysFont('comicsansms', 35)
    score_text = font.render(str(score_internal[0]) + '-' + str(score_internal[1]), True, WHITE)
    display.blit(score_text, (1000//2, 0))


def reset_ball(ball):
    ball.rect.x = 500
    ball.rect.y = 400
    ball.speed_x = random.choice(start)
    ball.speed_y = random.randint(2, 4)


def game():
    player1 = Paddle()
    player1.rect.x = 20
    player1.rect.y = 300
    player2 = Paddle()
    player2.rect.x = 960
    player2.rect.y = 300

    paddle_group = pygame.sprite.Group()
    paddle_group.add(player1)
    paddle_group.add(player2)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player1)
    all_sprites.add(player2)

    ball = Ball()
    ball.paddles = paddle_group

    reset_ball(ball)
    ball.score = score

    all_sprites.add(ball)

    while True:
        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.speed_y = -3
                elif event.key == pygame.K_s:
                    player1.speed_y = 3
                if event.key == pygame.K_UP:
                    player2.speed_y = -3
                elif event.key == pygame.K_DOWN:
                    player2.speed_y = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.speed_y = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2.speed_y = 0

        point(score)
        all_sprites.update()
        all_sprites.draw(display)

        pygame.display.flip()

        pygame.time.Clock().tick(120)


pygame.init()
game()