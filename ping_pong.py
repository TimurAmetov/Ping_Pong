from pygame import *
from random import randint


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

ping = Racket(player_image=r'assets\ping.png', size= (100,100), player_x=0, player_y=screen_height/2,player_speed=10,key_board=2)
pong = Racket(player_image='assets\pngimg.com - ping_pong_PNG10369.png', size= (100,100),player_x=screen_width-100, player_y=screen_height/2,player_speed=10,key_board=1)
ball = Ball(player_image='assets\pngimg.com - ping_pong_PNG10383.png',size=(50,50),player_x=100,player_y=screen_height/2,player_speed=5)
ping_ball = Racket(player_image=r'assets\ping_ball.png', size= (100,100), player_x=0, player_y=screen_height/2,player_speed=10,key_board=2)
pong_ball = Racket(player_image=r'assets\pong_ball.png', size= (100,100),player_x=screen_width-100, player_y=screen_height/2,player_speed=10,key_board=1)

clock = time.Clock()

mixer.init()
pas = mixer.Sound(r'assets\audiomass-output.mp3')

FPS = 60

speed_x = 1
speed_y = 0.1

score_one = 0
score_two = 0
roundes = 0

game_game = True
game_over = True
game = True
start = randint(1,2)

while game:
    window.blit(background, (0, 0))



    key_pressed = key.get_pressed()

    rounds = font1.render(
        'Раунд: ' + str(roundes), True, (255, 255, 255)
    )

    if game_over == True:
        window.blit(rounds, (x - 100, y))
        if start == 1:
            ping_ball.reset()
            ping_ball.move()
            pong.reset()
            pong.move()
        if start == 2:
            pong_ball.reset()
            pong_ball.move()
            ping.reset()
            ping.move()

        if game_game == True:
            if key_pressed[K_SPACE]:
                if start == 1:
                    ping.rect.y = ping_ball.rect.y
                    ball.rect.y = ping_ball.rect.y
                    ball.rect.x = ping_ball.rect.x + 50
                    ball.speed_x = abs(ball.speed_x)

                if start == 2:
                    pong.rect.y = pong_ball.rect.y
                    ball.rect.y = pong_ball.rect.y
                    ball.rect.x = pong_ball.rect.x - 50
                    ball.speed_x = -abs(ball.speed_x)

                game_over = False

    if game_over != True:
        pong.reset()
        pong.move()
        ping.reset()
        ping.move()
        ball.reset()

        if sprite.collide_rect(ball, ping) or sprite.collide_rect(ball, pong):
            ball.speed_x = -ball.speed_x
            if ball.rect.bottom >= ping.rect.top and ball.rect.bottom <= ping.rect.centery or ball.rect.bottom >= pong.rect.top and ball.rect.bottom <= pong.rect.centery:
                ball.speed_y = -abs(ball.speed_y)

            elif ball.rect.top <= ping.rect.bottom and ball.rect.top > ping.rect.centery or ball.rect.top <= pong.rect.bottom and ball.rect.top > pong.rect.centery:
                ball.speed_y = abs(ball.speed_y)
            pas.play()

        if ball.rect.y <= 0 or ((ball.rect.y + ball.rect.height) >= screen_height):
            ball.speed_y *= -1

        ball.move()

        if not game_over:
            if ball.speed_x > 0:
                while ball.rect.x <= 100:
                    ball.move()
            else:
                while ball.rect.x >= pong.rect.x-100:
                    ball.move()

    if ball.rect.x > screen_width:
        a = font1.render(
            'Игрок 1 победил', True, (255, 255, 255)
        )
        game_over = True
        start = 1
        score_one += 1
        ball.rect.y = screen_height/2
        ball.rect.x = screen_width/2
        roundes += 1

    if ball.rect.x < 0:
        b = font1.render(
            'Игрок 2 победил', True, (255, 255, 255)
        )
        game_over = True
        start = 2
        score_two += 1
        ball.rect.y = screen_height/2
        ball.rect.x = screen_width/2

        window.blit(rounds,(x-100, y))
        roundes += 1

    score_ping = font1.render(
        'Игрок 1: '+str(score_one), True, (255, 255, 255)
    )

    score_pong = font1.render(
        'Игрок 2: '+str(score_two), True, (255, 255, 255)
    )

    window.blit(score_ping, (0, 0))
    window.blit(score_pong, (screen_width - 250, 0))

    if roundes == 3:
        game_game = False
        if score_one == 2:
            window.blit(a, (x, y))
        if score_two == 2:
            window.blit(b,(x-100, y))

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)