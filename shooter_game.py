#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
"""mixer.music.set_volum(0.5)"""
fire_sound = mixer.Sound('fire.ogg')

win_width = 1080
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Space RobotoShooter')  
background = transform.scale(image.load('1625176070_57-kartinkin-com-p-stalker-fon-krasivie-foni-65.jpg'), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullets_PNG.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.x += self.speed
        global lost
        if self.rect.x > 980:
            self.rect.y = randint(50,800)
            self.rect.x = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 980:
            self.rect.y = randint(50,800)
            self.rect.x = 0

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid('asteroid.png', 0, randint(50, 650), 80 , 50, randint(2,6))
    asteroids.add(asteroid)



monsters = sprite.Group()
for i in range(1,8):
    monster = Enemy('Raven-Flying-PNG-HD.png', 0, randint(50, 650), 80, 50, randint(3,5))
    monsters.add(monster)


font.init()
font1 = font.SysFont('Arial', 36)


lost = 0
score = 0
bullets = sprite.Group()

rel_time = False

num_fire = 0

life = 3


ship = Player('stalker_PNG10.png', 950, win_height - 100, 80, 100, 18)
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True

            
    if not finish:
        window.blit(background, (0,0))
        text = font1.render('Счет: ' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('Raven-Flying-PNG-HD.png', 0, randint(50, 650), 80, 50, randint(3,5))
            monsters.add(monster)
        if score >= 20:
            finish = True
            win = font1.render('YOU WIN!', True, (255, 255, 255))
            window.blit(win, (500, 300))
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('идет перезарядка', 1, (150, 0, 0))
                window.blit(reload, (500, 200))
            else:
                num_fire = 0
                rel_time = False
        if life == 0 or lost >= 3:
            finish = True
            lose = font1.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (500, 300))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (1000, 20))
        display.update()
    time.delay(20)