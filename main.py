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
player.y = HEIGHT / 2
player.v = 2
player.va = 2
player.ac = 0.2
player.maxv = 8
player.lifes = 3
player.time = 0

player_lasers_list = []
enemy_lasers_list = []
enemies_list = []

"""DRAW"""


def draw():
    screen.fill("black")
    draw_list(player_lasers_list)
    draw_list(enemy_lasers_list)
    draw_list(enemies_list)
    player.draw()
    draw_lifes()
    screen.draw.text(str(player.time), center=(WIDTH / 2, 40), fontsize=80, color="yellow")
    if player.lifes <= 0:
        screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2), fontsize=100, color="red")


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


def update_player_lasers():
    for laser in player_lasers_list[:]:
        laser.x += math.sin(math.radians(laser.angle - 180)) * laser.v
        laser.y += math.cos(math.radians(laser.angle - 180)) * laser.v

        if laser.x > WIDTH + MARGIN or laser.x < -MARGIN or laser.y > HEIGHT + MARGIN or laser.y < -MARGIN:
            player_lasers_list.remove(laser)


def update_enemies():
    if random.random() < 0.01:
        add_enemy()

    for enemy in enemies_list:
        enemy.angle = enemy.angle_to(player.pos) - 90
        enemy.x += math.sin(math.radians(enemy.angle - 180)) * enemy.v
        enemy.y += math.cos(math.radians(enemy.angle - 180)) * enemy.v

        if random.random() < 0.005:
            laser = Actor("laser2")
            laser.pos = enemy.pos
            laser.angle = enemy.angle
            laser.v = random.randint(5, 10)
            enemy_lasers_list.append(laser)
            sounds.laser2.play()


def update_enemy_lasers():
    for laser in enemy_lasers_list[:]:
        laser.x += math.sin(math.radians(laser.angle - 180)) * laser.v
        laser.y += math.cos(math.radians(laser.angle - 180)) * laser.v

        if laser.x > WIDTH + MARGIN or laser.x < -MARGIN or laser.y > HEIGHT + MARGIN or laser.y < -MARGIN:
            enemy_lasers_list.remove(laser)


def update_collisions():
    for laser in player_lasers_list[:]:
        for enemy in enemies_list[:]:
            if enemy.colliderect(laser):
                enemies_list.remove(enemy)
                player_lasers_list.remove(laser)
                break

    for enemy in enemies_list[:]:
        if player.collidepoint(enemy.pos):
            enemies_list.remove(enemy)
            player.lifes -= 1
            if player.lifes == 0:
                sounds.game_over.play()

    for laser in enemy_lasers_list[:]:
        if player.collidepoint(laser.pos):
            enemy_lasers_list.remove(laser)
            player.lifes -= 1
            if player.lifes == 0:
                sounds.game_over.play()


"""EVENTS"""


def on_key_down(key):
    if key == keys.SPACE:
        laser = Actor("laser1")
        laser.pos = player.pos
        laser.angle = player.angle
        laser.v = 10
        player_lasers_list.append(laser)
        sounds.laser1.play()


"""HELPERS"""


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


def add_time():
    if player.lifes > 0:
        player.time += 1


"""INITIALIZATION"""

clock.schedule_interval(add_time, 1)
pgzrun.go()
