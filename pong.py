import pygame
import random

pygame.init()
pygame.mixer.init()

try:
    snd_bounce = pygame.mixer.Sound("bounce.wav")
    snd_score = pygame.mixer.Sound("score.wav")
except:
    snd_bounce = None
    snd_score = None

def play_sound(snd):
    if snd:
        snd.play()

def get_random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 500 - self.height:
            self.rect.y = 500 - self.height

    def change_color(self):
        color = get_random_color()
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [random.choice([-6, 6]), random.randint(-4, 4)]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = random.randint(-8, 8)
        self.change_color()

    def change_color(self):
        color = get_random_color()
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

carryOn = True
clock = pygame.time.Clock()

scoreA = 0
scoreB = 0
state = "MENU"
players = 1

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False
            if state == "MENU":
                if event.key == pygame.K_1:
                    players = 1
                    state = "PLAY"
                elif event.key == pygame.K_2:
                    players = 2
                    state = "PLAY"

    if state == "MENU":
        screen.fill(BLACK)
        title = font.render("PONG", True, WHITE)
        mode1 = small_font.render("Press 1 for 1 Player Mode (vs AI)", True, WHITE)
        mode2 = small_font.render("Press 2 for 2 Players Mode", True, WHITE)
        screen.blit(title, (270, 100))
        screen.blit(mode1, (150, 250))
        screen.blit(mode2, (150, 300))
        pygame.display.flip()
        clock.tick(60)
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
        
    if players == 2:
        if keys[pygame.K_UP]:
            paddleB.moveUp(5)
        if keys[pygame.K_DOWN]:
            paddleB.moveDown(5)
    else:
        if paddleB.rect.centery < ball.rect.centery and ball.velocity[0] > 0:
            paddleB.moveDown(5)
        elif paddleB.rect.centery > ball.rect.centery and ball.velocity[0] > 0:
            paddleB.moveUp(5)

    all_sprites_list.update()

    if ball.rect.x >= 690:
        scoreA += 1
        play_sound(snd_score)
        ball.rect.x = 345
        ball.rect.y = 195
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        scoreB += 1
        play_sound(snd_score)
        ball.rect.x = 345
        ball.rect.y = 195
        ball.velocity[0] = -ball.velocity[0]
        
    if ball.rect.y > 490:
        ball.velocity[1] = -abs(ball.velocity[1])
        play_sound(snd_bounce)
        ball.change_color()
    if ball.rect.y < 0:
        ball.velocity[1] = abs(ball.velocity[1])
        play_sound(snd_bounce)
        ball.change_color()

    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        play_sound(snd_bounce)
        ball.bounce()
        paddleA.change_color()
        paddleB.change_color()

    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    all_sprites_list.draw(screen)

    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()