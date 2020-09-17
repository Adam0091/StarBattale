import pygame
import time

pygame.init()

display_width = 1280
display_height = 720
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Star Battle')


# icon 32*32
icon = pygame.image.load('./imgs/icon.png')
pygame.display.set_icon(icon)

pygame.mixer.music.load('./sound/fon_sound.mp3')
pygame.mixer.music.play()

hero_ship_width = 80
hero_ship_height = 79

enemy_ship_width = 80
enemy_ship_height = 110

fps = pygame.time.Clock()
game = True

class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def get_first(self):
        return self.first

    def get_second(self):
        return self.second

    def change_second(self, value):
        self.second -= value


class HeroShip:
    def __init__(self, hero_x, hero_y):
        img_ship = pygame.image.load('./imgs/hero_ship.png')
        img_fire = pygame.image.load('./imgs/fire_hero.png')
        self.array_fires = []
        self.speed = 5
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.hero_width = hero_ship_width
        self.hero_height = hero_ship_height
        self.img_ship = img_ship
        self.img_fire = img_fire
        self.boolean_hero_fire = False


    def get_hero_x(self):
        return self.hero_x

    def get_hero_y(self):
        return self.hero_y

    def draw_hero(self):
        display.blit(self.img_ship, (self.hero_x - self.hero_width,
                                     self.hero_y - self.hero_height))

    def move_left_hero(self):
        if self.hero_x > 80:
            self.hero_x -= self.speed

    def move_right_hero(self):
        if self.hero_x < display_width:
            self.hero_x += self.speed

    def move_up_hero(self):
        if self.hero_y > 79:
            self.hero_y -= self.speed

    def move_down_hero(self):
        if self.hero_y < display_height:
            self.hero_y += self.speed

    def hero_fire(self):
        fire_x = self.hero_x - self.hero_width // 2 - 5
        fire_y = self.hero_y - self.hero_height - 30
        self.array_fires.append(Pair(fire_x, fire_y))
        self.boolean_hero_fire = True

    def move_fires(self):
        for i in range(len(self.array_fires) - 1):
            if self.array_fires[i].get_second() <= 0:
                del self.array_fires[i]
        for fire in self.array_fires:
            fire_x = fire.get_first()
            fire_y = fire.get_second()
            fire.change_second(10)
            display.blit(self.img_fire, (fire_x, fire_y))
        if range(len(self.array_fires) - 1) == 0:
            self.boolean_hero_fire = False


    # def hero_destroy(self):


class EnemyShip:
    def __init__(self, enemy_x, enemy_y):
        img_ship = pygame.image.load('./imgs/enemy_ship.png')
        self.img_fire = pygame.image.load('./imgs/fire_enemy.png')
        self.speed = 6
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.enemy_width = enemy_ship_width
        self.enemy_height = enemy_ship_height
        self.img_ship = img_ship
        self.array_fires = []

    def get_img(self):
        return self.img_ship

    def get_enemy_x(self):
        return self.enemy_x

    def get_enemy_y(self):
        return self.enemy_y

    def draw_enemy(self):
        display.blit(self.img_ship, (self.enemy_x - self.enemy_width,
                                     self.enemy_y - self.enemy_height))

    def move_left_enemy(self):
        self.enemy_x -= self.speed

    def move_right_enemy(self):
        self.enemy_x += 1

    def move_up_enemy(self):
        self.enemy_y -= self.speed

    def move_down_enemy(self):
        self.enemy_y += self.speed

    def enemy_fire(self):
        fire_x = self.enemy_x - self.enemy_width // 2 + 80
        fire_y = self.enemy_y + self.enemy_height - 4
        self.array_fires.append(Pair(fire_x, fire_y))

    def move_fires(self, hero_x, hero_y):
        for i in range(len(self.array_fires) - 1):
            if self.array_fires[i].get_second() > 720:  # не трогать
                del self.array_fires[i]
        for fire in self.array_fires:
            fire_x = fire.get_first()
            fire_y = fire.get_second()
            fire.change_second(-5) # тоже не трогать
            if fire_x > hero_x and fire_x < hero_x + hero_ship_width:
                print_text('OK', 60, 150)
            else:
                print_text('Fail', 60, 100)
            display.blit(self.img_fire, (fire_x, fire_y))


    # def enemy_destroy(self):


def create_array_enemy():
    array_enemy_ships = []
    for i in range(7):
        array_enemy_ships.append(EnemyShip(0 - 200 * i, display_height - 610))
    return array_enemy_ships


def draw_enemy_ships(array_enemy_ships):
    for i in range(len(array_enemy_ships) - 1):
        display.blit(array_enemy_ships[i].get_img(),
                    (array_enemy_ships[i].get_enemy_x(), array_enemy_ships[i].get_enemy_y()))


def move_enemy_ships(array_enemy_ships):
    for i in range(len(array_enemy_ships) - 1):
        array_enemy_ships[i].move_right_enemy()


def print_text(message, x, y, font_size=50, font_color=(255, 255, 255), font_type='./font/font.ttf'):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            print_text('Paused. Press enter to continue', 150, 360)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                paused = False
            pygame.display.update()
            fps.tick(15)


def run_game():
    background = pygame.image.load('./imgs/background.jpg')

    hero_ship = HeroShip(display_width // 2, display_height - 20)
    array_enemy_ships = create_array_enemy()
    last_time_m = int(round(time.time() * 1000))
    last_time_ms = int(round(time.time() * 1000))
    while game:
        diff_time_ms2 = int(round(time.time() * 1000)) - last_time_m
        diff_time_ms = int(round(time.time() * 1000)) - last_time_ms
        display.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            hero_ship.move_left_hero()
        if keys[pygame.K_RIGHT]:
            hero_ship.move_right_hero()
        if keys[pygame.K_UP]:
            hero_ship.move_up_hero()
        if keys[pygame.K_DOWN]:
            hero_ship.move_down_hero()
        if diff_time_ms >= 200:
            if keys[pygame.K_SPACE]:
                hero_ship.hero_fire()
            last_time_ms = int(round(time.time() * 1000))

        if hero_ship.boolean_hero_fire:
            hero_ship.move_fires()

        hero_ship.draw_hero()
        draw_enemy_ships(array_enemy_ships)

        for i in range(len(array_enemy_ships) - 1):
            if array_enemy_ships[i].get_enemy_x() < 500 - i * enemy_ship_width:
                move_enemy_ships(array_enemy_ships)
            elif diff_time_ms2 >= 1000:
                array_enemy_ships[i].enemy_fire()
                last_time_m = int(round(time.time() * 1000))
            array_enemy_ships[i].move_fires(hero_ship.get_hero_x(), hero_ship.get_hero_y())

        if keys[pygame.K_ESCAPE]:
            pause()

        fps.tick(200)
        pygame.display.update()


run_game()