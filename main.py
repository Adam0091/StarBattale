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

fire_width = 10
fire_height = 35

fps = pygame.time.Clock()
game = True


class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def change_y(self, value):
        self.y -= value


class HeroShip:
    def __init__(self, hero_x, hero_y):
        self.array_fires = []
        self.speed = 10
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.img_ship = pygame.image.load('./imgs/hero_ship.png')
        self.img_fire = pygame.image.load('./imgs/fire_hero.png')
        self.img_health = pygame.image.load('./imgs/icon.png')
        self.health = 5

    def minus_health_unit(self):
        self.health -= 1

    def get_hero_x(self):
        return self.hero_x

    def get_hero_y(self):
        return self.hero_y

    def draw_hero(self):
        display.blit(self.img_ship, (self.hero_x, self.hero_y))

    def move_left_hero(self):
        if self.hero_x > 0:
            self.hero_x -= self.speed

    def move_right_hero(self):
        if self.hero_x < display_width - hero_ship_width:
            self.hero_x += self.speed

    def move_up_hero(self):
        if self.hero_y > 0:
            self.hero_y -= self.speed

    def move_down_hero(self):
        if self.hero_y < display_height - hero_ship_height:
            self.hero_y += self.speed

    def fire(self):
        fire_x = self.hero_x + hero_ship_width // 2 - fire_width // 2
        fire_y = self.hero_y - fire_height
        fire = Pair(fire_x, fire_y)
        self.array_fires.append(fire)

    def draw_fires(self):
        for i in range(len(self.array_fires) - 1):
            if self.array_fires[i].get_y() <= 0:
                del self.array_fires[i]

        for i in range(len(self.array_fires) - 1):
            fire_x = self.array_fires[i].get_x()
            fire_y = self.array_fires[i].get_y()
            self.array_fires[i].change_y(10)
            display.blit(self.img_fire, (fire_x, fire_y))

    def check_collision_fire(self, enemy_ship, j, enemy_ships):
        enemy_ship_x = enemy_ship.get_enemy_x()
        enemy_ship_y = enemy_ship.get_enemy_y()

        for i in range(len(self.array_fires) - 1):
            fire_x = self.array_fires[i].get_x()
            fire_y = self.array_fires[i].get_y()
            if fire_x <= enemy_ship_x + enemy_ship_width and enemy_ship_x <= fire_x:
                if fire_y <= enemy_ship_y + enemy_ship_height and fire_y >= enemy_ship_y:
                    if enemy_ships[j].get_health() == 0:
                        enemy_ships.pop(j)
                    enemy_ships[j].minus_health_unit()
                    del self.array_fires[i]
                    self.draw_boom(enemy_ship_x, enemy_ship_y)

    def draw_boom(self, enemy_ship_x,  enemy_ship_y):
        image_counter = 0
        imgs_boom = [pygame.image.load('./imgs/hotpng(0).png'),
                     pygame.image.load('./imgs/hotpng(1).png'),
                     pygame.image.load('./imgs/hotpng(2).png'),
                     pygame.image.load('./imgs/hotpng(3).png'),
                     pygame.image.load('./imgs/hotpng(4).png'),
                     pygame.image.load('./imgs/hotpng(5).png')]
        time_ms = int(round(time.time() * 1000))
        while image_counter != 6:
            diff_time_ms = int(round(time.time() * 1000)) - time_ms
            if diff_time_ms >= 10:
                display.blit(imgs_boom[image_counter], (enemy_ship_x,  enemy_ship_y))
                time_ms = int(round(time.time() * 1000))
                pygame.display.update()
                image_counter += 1

    def draw_health(self):
        x = 20
        for i in range(self.health):
            display.blit(self.img_health, (x, 30))
            x += 40


class EnemyShip:
    def __init__(self, enemy_x, enemy_y):
        self.img_ship = img_ship = pygame.image.load('./imgs/enemy_ship.png')
        self.img_fire = pygame.image.load('./imgs/fire_enemy.png')
        self.speed = 6
        self.array_fires = []
        self.enemy_x = enemy_x
        self.enemy_y = enemy_y
        self.health = 2

    def minus_health_unit(self):
        self.health -= 1

    def get_health(self):
        return self.health

    def get_img(self):
        return self.img_ship

    def get_enemy_x(self):
        return self.enemy_x

    def get_enemy_y(self):
        return self.enemy_y

    def move_left_enemy(self):
        self.enemy_x -= self.speed

    def move_right_enemy(self):
        self.enemy_x += self.speed

    def move_up_enemy(self):
        self.enemy_y -= self.speed

    def move_down_enemy(self):
        self.enemy_y += self.speed

    def draw_enemy(self):
        display.blit(self.img_ship, (self.enemy_x, self.enemy_y))

    def fire(self):
        fire_x = self.enemy_x + enemy_ship_width // 2 - fire_width // 2
        fire_y = self.enemy_y + enemy_ship_height + fire_height
        fire = Pair(fire_x, fire_y)
        self.array_fires.append(fire)

    def draw_fires(self):
        for i in range(len(self.array_fires) - 1):
            if self.array_fires[i].get_y() >= display_height:
                del self.array_fires[i]

        for i in range(len(self.array_fires) - 1):
            fire_x = self.array_fires[i].get_x()
            fire_y = self.array_fires[i].get_y()
            self.array_fires[i].change_y(-10)
            display.blit(self.img_fire, (fire_x, fire_y))

    def check_collision_for_enemy(self, hero_ship):
        hero_ship_x = hero_ship.get_hero_x()
        hero_ship_y = hero_ship.get_hero_y()

        for i in range(len(self.array_fires) - 1):
            fire_x = self.array_fires[i].get_x()
            fire_y = self.array_fires[i].get_y()
            if fire_x <= hero_ship_x + hero_ship_width and hero_ship_x <= fire_x:
                if fire_y <= hero_ship_y + hero_ship_height and fire_y >= hero_ship_y:
                    del self.array_fires[i]
                    hero_ship.minus_health_unit()


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


def create_array_enemy_ships(count):
    enemy_ships = []
    for i in range(count + 1):
        enemy_ships.append(EnemyShip(-100 - 200 * i, 100))
    return enemy_ships


def draw_enemy_ships(enemy_ships):
    for i in range(len(enemy_ships) - 1):
        enemy_ships[i].draw_enemy()


def move_enemy_ships(enemy_ships):
    for i in range(len(enemy_ships) - 1):
        if enemy_ships[i].get_enemy_x() <= (1100 - 200 * i):
            enemy_ships[i].move_right_enemy()


def fire_enemy_ships(enemy_ships):
    for i in range(len(enemy_ships) - 1):
        enemy_ships[i].fire()


def draw_fire_enemy_ships(enemy_ships):
    for i in range(len(enemy_ships) - 1):
        enemy_ships[i].draw_fires()


def check_collision_fire(enemy_ships, hero_ship):
    for i in range(len(enemy_ships) - 1):
        hero_ship.check_collision_fire(enemy_ships[i], i, enemy_ships)
        enemy_ships[i].check_collision_for_enemy(hero_ship)


def check_is_you_lose(hero_ship_health):
    show_text = True
    if hero_ship_health == 0:
        display.blit(pygame.image.load('./imgs/background.jpg'), (0, 0))
        while show_text:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            print_text('You lose. Press enter to start the game again', 150, display_height // 2 - 25, 35)
            pygame.display.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                show_text = False
                run_game()
            pygame.display.update()
            fps.tick(15)


def check_for_lvl_two(enemy_ships):
    if len(enemy_ships) - 1 == 0:
        return True



def run_game():
    background = pygame.image.load('./imgs/background.jpg')
    hero_ship = HeroShip(display_width // 2 - hero_ship_width // 2,
                         display_height // 2 + hero_ship_height)

    enemy_ships = create_array_enemy_ships(6)

    time_ms = int(round(time.time() * 1000))
    time2_ms = int(round(time.time() * 1000))

    while game:
        diff_time_ms = int(round(time.time() * 1000)) - time_ms
        diff_time2_ms = int(round(time.time() * 1000)) - time2_ms
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

        if diff_time_ms >= 300:
            if keys[pygame.K_SPACE]:
                hero_ship.fire()
            time_ms = int(round(time.time() * 1000))

        draw_enemy_ships(enemy_ships)
        move_enemy_ships(enemy_ships)
        if diff_time2_ms >= 600:
            fire_enemy_ships(enemy_ships)
            time2_ms = int(round(time.time() * 1000))
        draw_fire_enemy_ships(enemy_ships)

        hero_ship.draw_hero()
        hero_ship.draw_fires()
        hero_ship.draw_health()
        check_collision_fire(enemy_ships, hero_ship)
        check_is_you_lose(hero_ship.health)

        if keys[pygame.K_ESCAPE]:
            pause()

        if check_for_lvl_two(enemy_ships):
            enemy_ships = create_array_enemy_ships(6)

        fps.tick(200)
        pygame.display.update()


run_game()
