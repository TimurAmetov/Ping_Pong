from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Racket(GameSprite):
    def __init__(self,player_image, player_x, player_y, player_speed,key_board):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.key_board = key_board

    def move(self):
        keys_pressed = key.get_pressed()

        if self.key_board == 1:
            if keys_pressed[K_UP] and  self.rect.y > 0:
                self.rect.y -= self.speed
            if keys_pressed[K_DOWN] and self.rect.y + self.rect.height < screen_height:
                self.rect.y += self.speed

        if self.key_board == 2:
            if keys_pressed[K_w] and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys_pressed[K_s] and self.rect.y + self.rect.height < screen_height:
                self.rect.y += self.speed

class Ball(GameSprite):
    def move(self):


font.init()
font1 = font.Font(None, 70)

window = display.set_mode((0, 0), FULLSCREEN)
display.set_caption('Пинг понг')

screen_width, screen_height = window.get_size()

background = transform.scale(
    image.load('assets\image[uEse9L].png'),
    (screen_width, screen_height)
)

ping = Racket('assets\pngimg.com - ping_pong_PNG10369.png', 0, screen_height/2,10,2)
pong = Racket('assets\pngimg.com - ping_pong_PNG10369.png',screen_width-100, screen_height/2,10,1)
ball = Ball('assets\pngimg.com - ping_pong_PNG10383.png',screen_width/2,screen_height/2,5)

clock = time.Clock()

FPS = 60

game = True

while game:
    window.blit(background, (0, 0))
    ping.reset()
    pong.reset()
    ball.reset()
    ping.move()
    pong.move()
    ball.move()

    ball.rect.x += speed_x
    ball.rect.y -= speed_y

    if ball.rect.y < 0:
        speed_y *= random.uniform(-1.05, -1)
    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= random.uniform(-1.05, -1)

    if ball.colliderect(platform.rect):
        speed_y *= random.uniform(-1.05, -1)

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)