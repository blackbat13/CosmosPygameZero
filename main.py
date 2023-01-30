import math
import random

import pgzrun

"""CONFIGURATION"""

WIDTH = 1200
HEIGHT = 1200
MARGIN = 20

"""VARIABLES"""

player = Actor("player")
player.x = WIDTH / 2
player.y = HEIGHT - 60
player.v = 2
player.va = 2
player.ac = 0.2
player.maxv = 8
player.angle = 0
player.lifes = 3
player.time = 0

asteroids_list = []
player_lasers_list = []
enemy_lasers_list = []
enemies_list = []

"""DRAW"""


def draw():
    screen.fill("black")

    draw_list(asteroids_list)
    draw_list(player_lasers_list)
    draw_list(enemy_lasers_list)
    draw_list(enemies_list)

    player.draw()

    draw_lifes()

    if player.lifes <= 0:
        screen.draw.text("GAME OVER", center=(
            WIDTH / 2, HEIGHT / 2), fontsize=100, color="red")

    screen.draw.text(str(player.time), center=(
        WIDTH / 2, 40), fontsize=80, color="yellow")


def draw_list(list):
    for element in list:
        element.draw()


def draw_lifes():
    for life_id in range(1, player.lifes + 1):
        life = Actor("life")
        life.x = life_id * life.width
        life.y = life.height / 2
        life.draw()


"""UPDATE"""


def update():
    if player.lifes <= 0:
        return

    update_player()
    update_asteroids()
    update_player_lasers()
    update_enemies()
    update_enemy_lasers()
    update_collisions()


def update_player():
    player.x += math.sin(math.radians(player.angle - 180)) * player.v
    player.y += math.cos(math.radians(player.angle - 180)) * player.v

    if keyboard.A:
        player.angle += player.va

    if keyboard.D:
        player.angle -= player.va

    if keyboard.W:
        player.v += player.ac
        if player.v > player.maxv:
            player.v = player.maxv

    if keyboard.S:
        player.v -= player.ac
        if player.v < 0:
            player.v = 0

    if player.x > WIDTH + MARGIN:
        player.x = -MARGIN

    if player.x < -MARGIN:
        player.x = WIDTH + MARGIN

    if player.y < -MARGIN:
        player.y = HEIGHT + MARGIN

    if player.y > HEIGHT + MARGIN:
        player.y = -MARGIN


def update_asteroids():
    if random.random() < 0.008:
        add_asteroid()

    for asteroid in asteroids_list:
        asteroid.x += math.sin(math.radians(asteroid.angle - 180)) * asteroid.v
        asteroid.y += math.cos(math.radians(asteroid.angle - 180)) * asteroid.v

        if asteroid.x > WIDTH + MARGIN:
            asteroid.x = -MARGIN

        if asteroid.x < -MARGIN:
            asteroid.x = WIDTH + MARGIN

        if asteroid.y < -MARGIN:
            asteroid.y = HEIGHT + MARGIN

        if asteroid.y > HEIGHT + MARGIN:
            asteroid.y = -MARGIN


def update_player_lasers():
    for las in player_lasers_list[:]:
        las.x += math.sin(math.radians(las.angle - 180)) * las.v
        las.y += math.cos(math.radians(las.angle - 180)) * las.v

        if las.x > WIDTH + MARGIN or las.x < -MARGIN:
            player_lasers_list.remove(las)
        elif las.y > HEIGHT + MARGIN or las.y < -MARGIN:
            player_lasers_list.remove(las)


def update_enemies():
    if random.random() < 0.01:
        add_enemy()

    for enemy in enemies_list:
        enemy.angle = enemy.angle_to(player.pos) - 90
        enemy.x += math.sin(math.radians(enemy.angle - 180)) * enemy.v
        enemy.y += math.cos(math.radians(enemy.angle - 180)) * enemy.v

        if random.random() < 0.005:
            las = Actor("laser2")
            las.angle = enemy.angle
            las.x = enemy.x
            las.y = enemy.y
            las.v = random.randint(5, 10)
            enemy_lasers_list.append(las)
            sounds.laser2.play()


def update_enemy_lasers():
    for las in enemy_lasers_list[:]:
        las.x += math.sin(math.radians(las.angle - 180)) * las.v
        las.y += math.cos(math.radians(las.angle - 180)) * las.v

        if las.x > WIDTH + MARGIN or las.x < -MARGIN:
            enemy_lasers_list.remove(las)
        elif las.y > HEIGHT + MARGIN or las.y < -MARGIN:
            enemy_lasers_list.remove(las)


def update_collisions():
    for las in player_lasers_list[:]:
        for met in asteroids_list[:]:
            if met.colliderect(las):
                asteroids_list.remove(met)
                player_lasers_list.remove(las)

    for las in enemy_lasers_list[:]:
        for met in asteroids_list[:]:
            if met.colliderect(las):
                asteroids_list.remove(met)
                enemy_lasers_list.remove(las)

    for las in player_lasers_list[:]:
        for enemy in enemies_list[:]:
            if enemy.colliderect(las):
                enemies_list.remove(enemy)
                player_lasers_list.remove(las)

    for las in enemy_lasers_list[:]:
        if player.collidepoint(las.pos):
            player.lifes -= 1
            if player.lifes == 0:
                sounds.game_over.play()
            enemy_lasers_list.remove(las)

    for enemy in enemies_list[:]:
        if player.collidepoint(enemy.pos):
            player.lifes -= 1
            if player.lifes == 0:
                sounds.game_over.play()
            enemies_list.remove(enemy)

    for ast in asteroids_list[:]:
        if player.collidepoint(ast.pos):
            player.lifes -= 1
            if player.lifes == 0:
                sounds.game_over.play()
            asteroids_list.remove(ast)


"""EVENTS"""


def on_key_down(key):
    if key == keys.SPACE:
        las = Actor("laser1")
        las.angle = player.angle
        las.x = player.x
        las.y = player.y
        las.v = 10
        player_lasers_list.append(las)
        sounds.laser1.play()


"""HELPERS"""


def add_asteroid():
    image_id = random.randint(1, 4)
    asteroid = Actor("asteroid" + str(image_id))
    asteroid.pos = choose_position()
    asteroid.v = random.randint(2, 10)
    asteroid.angle = random.randint(0, 359)
    asteroids_list.append(asteroid)


def add_enemy():
    enemy = Actor("enemy")
    enemy.pos = choose_position()
    enemy.v = random.randint(2, 5)
    enemies_list.append(enemy)


def choose_position():
    if random.randint(1, 2) == 1:
        x = random.choice([-MARGIN, WIDTH + MARGIN])
        y = random.randint(MARGIN, HEIGHT - MARGIN)
    else:
        x = random.randint(MARGIN, WIDTH - MARGIN)
        y = random.choice([-MARGIN, HEIGHT + MARGIN])

    return x, y


def addTime():
    if player.lifes > 0:
        player.time += 1


"""INITIALIZATION"""

clock.schedule_interval(addTime, 1)
pgzrun.go()
