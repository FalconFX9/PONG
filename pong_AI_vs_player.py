"""
Made pong in 23min04s680ms
"""
import pygame
import random
import neat

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
        self.score = 0

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
        self.collided = False
        self.scored = False
        self.count = 150

    def update(self):
        self.collided = False
        self.scored = False
        if (self.rect.top < 0) or self.rect.bottom >= 800:
            self.speed_y *= -1

        if self.rect.x <= 0 or self.rect.right >= 1000:
            if self.speed_x > 0:
                self.paddles.sprites()[0].score += 1
                self.scored = True
            else:
                self.paddles.sprites()[1].score += 1
            reset_ball(self)

        self.rect.x += self.speed_x
        collision = pygame.sprite.spritecollide(self, self.paddles, False)
        if collision and self.count < 0:
            self.speed_x *= -1
            self.count = 150
            if self.speed_x > 0:
                self.collided = True

        self.rect.y += self.speed_y
        self.count -= 1



def point(score_internal):
    font = pygame.font.SysFont('comicsansms', 35)
    score_text = font.render(str(score_internal[0]) + '-' + str(score_internal[1]), True, WHITE)
    display.blit(score_text, (1000//2, 0))


def reset_ball(ball):
    ball.rect.x = 500
    ball.rect.y = 400
    ball.speed_x = 3
    ball.speed_y = 3


def game(genomes, config):
    nets = []
    ge = []
    player1 = []
    balls = []

    player2 = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        player = Paddle()
        player.rect.x = 20
        player.rect.y = 300
        player1.append(player)
        g.fitness = 0
        ge.append(g)
        ball = Ball()
        paddle_group = pygame.sprite.Group()
        paddle_group.add(player)
        player = Paddle()
        player.rect.x = 960
        player.rect.y = 300
        player2.append(player)
        paddle_group.add(player)
        ball.paddles = paddle_group
        balls.append(ball)

    all_sprites = pygame.sprite.Group()
    for player in player1:
        all_sprites.add(player)

    for player in player2:
        all_sprites.add(player)

    for ball in balls:
        reset_ball(ball)
        all_sprites.add(ball)

    while True:
        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    for player in player2:
                        player.speed_y = -3
                elif event.key == pygame.K_DOWN:
                    for player in player2:
                        player.speed_y = 3
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    for player in player2:
                        player.speed_y = 0

        for x, player in enumerate(player1):
            output = nets[x].activate((balls[x].rect.x, balls[x].rect.y, balls[x].speed_x, balls[x].speed_y, player1[x].rect.y))

            if output[0] > 0.5:
                player1[x].speed_y = -3
            elif output[1] > 0.5:
                player1[x].speed_y = 3

            if balls[x].scored:
                ge[x].fitness += 2
            if balls[x].collided:
                ge[x].fitness += 1
            if player2[x].score > 0:
                ge[x].fitness -= 1
                all_sprites.remove((player1[x], balls[x], player2[x]))
                player1.pop(x)
                ge.pop(x)
                nets.pop(x)
                player2.pop(x)
                balls.pop(x)

        all_sprites.update()
        all_sprites.draw(display)

        pygame.display.flip()

        pygame.time.Clock().tick(120)

        if len(player1) <= 0:
            break


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(game, 50)


pygame.init()
run('config.txt')