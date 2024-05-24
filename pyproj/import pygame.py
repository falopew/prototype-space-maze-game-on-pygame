import pygame
import random
import sys

MAP_SIZE = 40
TILE_SIZE = 40
grass_texture = pygame.image.load('grass_texture.jpg')
grass_texture = pygame.transform.scale(grass_texture, (TILE_SIZE // 2, TILE_SIZE // 2))
rock_texture = pygame.image.load('rock_texture.jpg')
rock_texture = pygame.transform.scale(rock_texture, (TILE_SIZE // 2, TILE_SIZE // 2))
lava_texture = pygame.image.load('lava_texture.jpg')
lava_texture = pygame.transform.scale(lava_texture, (TILE_SIZE // 2, TILE_SIZE // 2))
swamp_texture = pygame.image.load('swamp_texture.jpg')
swamp_texture = pygame.transform.scale(swamp_texture, (TILE_SIZE // 2, TILE_SIZE // 2))
player_image = pygame.image.load('player_spaceship.png')
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
ore_image = pygame.image.load('ore_image.jpeg')
ore_image = pygame.transform.scale(ore_image, (TILE_SIZE // 2, TILE_SIZE // 2))
rare_artifact_image = pygame.image.load('rare_artifact_image.jpeg')
rare_artifact_image = pygame.transform.scale(rare_artifact_image, (TILE_SIZE // 2, TILE_SIZE // 2))
ship_parts_image = pygame.image.load('ship_parts_image.png')
ship_parts_image = pygame.transform.scale(ship_parts_image, (20, 20))
pygame.init()
screen = pygame.display.set_mode((MAP_SIZE * TILE_SIZE, MAP_SIZE * TILE_SIZE))
pygame.display.set_caption("Space Explorer")

map_data = [[random.choice(["grass", "rock", "lava", "swamp"]) for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

player_health = 100
player_position = [MAP_SIZE // 2, MAP_SIZE // 2]
resources = []
ship_parts = 0
upgrades = []

def draw_tile(tile_type, position):
    x, y = position
    if tile_type == "grass":
        screen.blit(grass_texture, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "rock":
        screen.blit(rock_texture, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "lava":
        screen.blit(lava_texture, (x * TILE_SIZE, y * TILE_SIZE))
    elif tile_type == "swamp":
        screen.blit(swamp_texture, (x * TILE_SIZE, y * TILE_SIZE))

def player_move(dx, dy):
    global player_position, player_health
    player_position[0] += dx
    player_position[1] += dy
    if map_data[player_position[1]][player_position[0]] == "swamp":
        player_health -= 5
    elif map_data[player_position[1]][player_position[0]] == "lava":
        player_health -= 10
    elif map_data[player_position[1]][player_position[0]] == "rock":
        resources.append("ore")

def update_resources():
    global resources, ship_parts
    if "rare artifact" in resources:
        global player_health
        player_health += 50
        resources.remove("rare artifact")
    if "ore" in resources:
        ship_parts += 1
        resources.remove("ore")

def update_health():
    global player_health
    if player_health > 100:
        player_health = 100
    elif player_health < 0:
        player_health = 0

def update_creatures():
    pass

def update_upgrades():
    global upgrades, player_health, resources
    if "shield" in upgrades:
        player_health += 50
        upgrades.remove("shield")
    if "laser" in upgrades:
        resources.append("rare artifact")
        upgrades.remove("laser")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_move(0, -1)
            elif event.key == pygame.K_DOWN:
                player_move(0, 1)
            elif event.key == pygame.K_LEFT:
                player_move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player_move(1, 0)

    update_resources()
    update_health()
    update_creatures()
    update_upgrades()

    screen.fill((0, 0, 0))  # Fill the screen with black

    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            draw_tile(map_data[i][j], (j, i))

    # Draw player
    screen.blit(player_image, (player_position[0] * TILE_SIZE, player_position[1] * TILE_SIZE))

    # Draw resources
    for i, resource in enumerate(resources):
        if resource == "ore":
            screen.blit(ore_image, (10 + i * 20, 10))
        elif resource == "rare artifact":
            screen.blit(rare_artifact_image, (10 + i * 20, 10))

    # Draw health bar
    pygame.draw.rect(screen, (255, 0, 0), (10, 30, player_health * 2, 20))
    pygame.draw.rect(screen, (0, 255, 0), (10, 30, 100 * 2, 20), 1)

    # Draw ship parts
    screen.blit(ship_parts_image, (10, 60))
    pygame.draw.rect(screen, (0, 255, 0), (10, 60, ship_parts * 20, 20), 1)

    pygame.display.flip()

pygame.quit()