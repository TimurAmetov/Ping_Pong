from pygame import *
import random


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, size, player_x, player_y, player_speed):
        super().__init__()
        self.size = size
        self.image = transform.scale(image.load(player_image), (size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed_x = 10
        self.speed_y = 1

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Racket(GameSprite):
    def __init__(self,player_image,size, player_x, player_y, player_speed,key_board):
        super().__init__(player_image, size, player_x, player_y, player_speed)
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
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

font.init()
font1 = font.Font(None, 70)

window = display.set_mode((0, 0), FULLSCREEN)
display.set_caption('Пинг понг')

screen_width, screen_height = window.get_size()

background = transform.scale(
    image.load(r'assets\Untitleddwa.png'),
    (screen_width, screen_height)
)

x = screen_width/2
y = screen_height/2

ping = Racket(player_image='assets\pngimg.com - ping_pong_PNG10369.png', size= (100,100), player_x=0, player_y=screen_height/2,player_speed=10,key_board=2)
pong = Racket(player_image='assets\pngimg.com - ping_pong_PNG10369.png', size= (100,100),player_x=screen_width-100, player_y=screen_height/2,player_speed=10,key_board=1)
ball = Ball(player_image='assets\pngimg.com - ping_pong_PNG10383.png',size=(50,50),player_x=100, player_y=screen_height/2,player_speed=5)

clock = time.Clock()

FPS = 60

speed_x = 1
speed_y = 0.1

game_over = False
game = True
pas = False

while game:
    if game_over == False:
        window.blit(background, (0, 0))
        ping.reset()
        pong.reset()
        ball.reset()
        ping.move()
        pong.move()

        if sprite.collide_rect(ball, ping) or sprite.collide_rect(ball, pong):
            ball.speed_x = -ball.speed_x
            if ball.rect.bottom >= ping.rect.top and ball.rect.bottom <= ping.rect.centery or ball.rect.bottom >= pong.rect.top and ball.rect.bottom <= pong.rect.centery:
                ball.speed_y = -abs(ball.speed_y)

            elif ball.rect.top <= ping.rect.bottom and ball.rect.top > ping.rect.centery or ball.rect.top <= pong.rect.bottom and ball.rect.top > pong.rect.centery:
                ball.speed_y = abs(ball.speed_y)

        if ball.rect.y <= 0 or ((ball.rect.y + ball.rect.height) >= screen_height):
            ball.speed_y *= -1

        ball.move()

        if ball.rect.x >= screen_width-5:
            a = font1.render(
                'Игрок 1 победил', True, (255, 255, 255)
            )
            game_over = True
            window.blit(a, (x, y))

        if ball.rect.x <= 5:
            b = font1.render(
                'Игрок 2 победил', True, (255, 255, 255)
            )
            game_over = True
            window.blit(b, (x, y))

        if not game_over:
            if ball.speed_x > 0:
                while ball.rect.x <= 100:
                    ball.move()
            else:
                while ball.rect.x >= pong.rect.x-100:
                    ball.move()

    key_pressed = key.get_pressed()

    if key_pressed[K_SPACE] and game_over:
        game_over = False
        ball.rect.x = screen_width / 2
        ball.rect.y = screen_height / 2
        ping.rect.x = 0
        pong.rect.x = screen_width-100


    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)