# main imports and setup
import os
import pygame
import json

from ball import Ball
from peg import Peg
from ui import draw_game_state, draw_text_center
from confetti import ConfettiManager
confetti = ConfettiManager()

# screen size
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280

# init pygame and main objects
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True  # main loop runs while true

# game state vars
balls = []
pegs = []
balls_left = 0
balls_in_goal = 0
balls_needed = 0
peg_inventory = {}
selected_peg = ""
selected_peg_indx = 0
current_level = 1
total_levels = None

# sizing
cell_size = 100
ball_radius = cell_size // 4
peg_radius = cell_size // 3

# dropper (ball launcher)
dropper_x = 0
dropper_y = cell_size // 3
dropper_size = cell_size // 2
dropper_speed = 2
dropper_dir = 1

# state flags
game_over = False
game_over_t = None
level_beat = False
level_beat_t = None
pause_game_input = False
game_beat = False

# screen layout
padding = 40  # total horizontal padding
max_width = SCREEN_WIDTH - padding
min_cell_size = 20
max_cell_size = 100

# load level data and prep grid
def setup_level(data):
    global balls_needed, balls_left
    global selected_peg, peg_inventory, selected_peg_indx
    global cell_size, peg_radius, ball_radius

    sizeX, sizeY = data["sizeX"], data["sizeY"]
    balls_needed = data["balls_to_win"]
    balls_left = data["total_balls"]
    peg_inventory = data["total_pegs"]
    selected_peg = list(peg_inventory.keys())[0]
    selected_peg_indx = 0

    # make sure grid fits screen
    cell_size = max(min_cell_size, min(max_cell_size, max_width / sizeX))
    peg_radius = cell_size // 3
    ball_radius = cell_size // 4

    grid_w = sizeX * cell_size + (cell_size // 2)
    total_width = grid_w + padding
    offset_x = (SCREEN_WIDTH - total_width) // 2 + (padding // 2)
    offset_y = (SCREEN_HEIGHT - (sizeY * cell_size)) // 2

    pegs.clear()  # clear previous pegs

    # create pegs in grid
    for i, peg_type in enumerate(data["map"]):
        row = i // sizeX
        col = i % sizeX
        x = col * cell_size + cell_size // 2 + offset_x
        if row % 2 == 0:
            x += cell_size // 2
        y = row * cell_size + cell_size // 2 + offset_y
        pegs.append(Peg(x, y, peg_type, peg_radius, True if peg_type == "EMPTY" else False))

# draw all pegs
def draw_pegs(screen):
    for peg in pegs:
        peg.draw(screen)

# load level from file
def load_level(level):
    global game_beat, running
    if int(level) > level_count:
        game_beat = True
        pygame.display.flip()
        running = False
    else:
        with open(f'levels/{level}.json', 'r') as file:
            map_data = json.load(file)
            setup_level(map_data)

# draw game over blur + text
def draw_game_over(screen, progress):
    screen_copy = screen.copy()
    blur_factor = 0.01
    downscaled_size = (
        max(1, int(SCREEN_WIDTH * blur_factor)),
        max(1, int(SCREEN_HEIGHT * blur_factor))
    )
    blurred = pygame.transform.smoothscale(screen_copy, downscaled_size)
    blurred = pygame.transform.smoothscale(blurred, (SCREEN_WIDTH, SCREEN_HEIGHT))
    blurred.set_alpha(int(255 * progress))
    screen.blit(blurred, (0, 0))

    draw_text_center(screen, ":(", SCREEN_HEIGHT // 4)
    draw_text_center(screen, "out of balls", SCREEN_HEIGHT // 3)
    draw_text_center(screen, "press 'r' to restart", 3 * SCREEN_HEIGHT // 5)

# draw level complete blur + text
def draw_level_beat(screen):     
    screen_copy = screen.copy()
    blur_factor = 0.01
    downscaled_size = (
        max(1, int(SCREEN_WIDTH * blur_factor)),
        max(1, int(SCREEN_HEIGHT * blur_factor))
    )
    blurred = pygame.transform.smoothscale(screen_copy, downscaled_size)
    blurred = pygame.transform.smoothscale(blurred, (SCREEN_WIDTH, SCREEN_HEIGHT))
    blurred.set_alpha(255 * 0.5)
    screen.blit(blurred, (0, 0))

    draw_text_center(screen, ":)", SCREEN_HEIGHT // 4)
    draw_text_center(screen, "you did it", SCREEN_HEIGHT // 3)
    draw_text_center(screen, "press 'n' to continue", 3 * SCREEN_HEIGHT // 5)




# main menu screen
def main_menu():
    global level_count
    level_count = len([f for f in os.listdir("levels") if f.endswith(".json")])

    load_level(str(1))
    screen.fill("gray")
    draw_pegs(screen)
    confetti.update()
    confetti.draw(screen)
    pygame.display.flip()

    # draw blurred bg
    screen_copy = screen.copy()
    blur_factor = 0.0125
    downscaled_size = (
        max(1, int(SCREEN_WIDTH * blur_factor)),
        max(1, int(SCREEN_HEIGHT * blur_factor))
    )
    blurred = pygame.transform.smoothscale(screen_copy, downscaled_size)
    blurred = pygame.transform.smoothscale(blurred, (SCREEN_WIDTH, SCREEN_HEIGHT))
    blurred.set_alpha(255)
    screen.blit(blurred, (0, 0))

    # show title and start msg
    draw_text_center(screen, "O", SCREEN_HEIGHT // 4)
    draw_text_center(screen, "super ball fun", SCREEN_HEIGHT // 3)
    draw_text_center(screen, "press any key to start", 3 * SCREEN_HEIGHT // 5)
    pygame.display.flip()

    # wait for keypress
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# core loop
def game_loop():
    global running, current_level
    global game_over, pause_game_input, level_beat, level_beat_t
    global balls, balls_left, balls_in_goal, balls_needed 
    global pegs, peg_inventory, selected_peg, selected_peg_indx
    global cell_size, ball_radius, peg_radius
    global dropper_x, dropper_y, dropper_size, dropper_speed, dropper_dir


    load_level(str(current_level))

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            peg_clicked = False

            if event.type == pygame.QUIT:
                running = False

            # click to place/remove peg
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, peg in enumerate(pegs):
                    if not peg.editable or peg.type == "GOAL":
                        continue
                    if peg.type == "EMPTY" and event.button == 3:
                        continue
                    if peg.type != "EMPTY" and event.button == 1:
                        continue

                    x_dist = (peg.x - mouse_pos[0])
                    y_dist = (peg.y - mouse_pos[1])
                    sqdist = (x_dist*x_dist) + (y_dist*y_dist)

                    if (sqdist > (peg.radius*peg.radius)):
                        continue

                    # right click = remove
                    if event.button == 3:
                        peg_clicked = True
                        peg_inventory[peg.type] += 1
                        peg.switch("EMPTY")
                    # left click = place
                    elif peg_inventory[selected_peg] > 0:
                        peg_clicked = True
                        peg_inventory[selected_peg] -= 1
                        peg.switch(selected_peg)

            # key inputs
            if not pause_game_input and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and balls_left > 0 and not peg_clicked:
                    spawn_x = dropper_x + dropper_size // 2
                    spawn_y = dropper_y + dropper_size
                    balls.append(Ball(spawn_x, spawn_y, ball_radius))
                    balls_left -= 1
                if event.key == pygame.K_UP:
                    selected_peg_indx = (selected_peg_indx - 1) % len(peg_inventory)
                    selected_peg = list(peg_inventory.keys())[selected_peg_indx]
                if event.key == pygame.K_DOWN:
                    selected_peg_indx = (selected_peg_indx + 1) % len(peg_inventory)
                    selected_peg = list(peg_inventory.keys())[selected_peg_indx]

            # restart or next level
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_n:
                    if level_beat and event.key:
                        current_level += 1
                    # game state vars
                    game_over = False
                    pause_game_input = False
                    level_beat = False
                    balls.clear()
                    pegs.clear()
                    balls_left = 0
                    balls_in_goal = 0
                    balls_needed = 0
                    peg_inventory.clear()
                    selected_peg = ""
                    selected_peg_indx = 0

                    # sizing
                    cell_size = 100
                    ball_radius = cell_size // 4
                    peg_radius = cell_size // 3

                    # dropper (ball launcher)
                    dropper_x = 0
                    dropper_y = cell_size // 3
                    dropper_size = cell_size // 2
                    dropper_speed = 2
                    dropper_dir = 1
                    load_level(str(current_level))

        # hover effect
        if not game_over:
            for peg in pegs:
                x_dist = (peg.x - mouse_pos[0])
                y_dist = (peg.y - mouse_pos[1])
                sqdist = (x_dist*x_dist) + (y_dist*y_dist)
                peg.hovered = sqdist <= peg.radius * peg.radius

        screen.fill("gray")
        draw_pegs(screen)

        # move dropper
        dropper_x += dropper_dir * dropper_speed
        if dropper_x > SCREEN_WIDTH - dropper_size:
            dropper_dir = -1
        elif dropper_x < 0:
            dropper_dir = 1

        # draw dropper triangle
        mid_x = dropper_x + dropper_size // 2
        top_y = dropper_y
        bot_y = dropper_y + dropper_size
        left_x = dropper_x
        right_x = dropper_x + dropper_size
        pygame.draw.polygon(screen, (255, 255, 255), [(mid_x, bot_y), (left_x, top_y), (right_x, top_y)])

        # update all balls
        for ball in balls[:]:
            if ball.touching_goal:
                balls_in_goal += 1
                if ball:
                    balls.remove(ball)
            if ball.queue_delete:
                if ball:
                    balls.remove(ball)

            ball.update(pegs)

            # effects
            if ball.confetti:
                confetti.spawn(ball.x, ball.y, 50)
                ball.confetti = False

            if ball.split:
                ball.split = False
                balls.append(Ball(ball.x - 10, ball.y, ball_radius))
                balls[-1].vx = -abs(ball.vx or 1)
                balls.append(Ball(ball.x + 10, ball.y, ball_radius))
                balls[-1].vx = abs(ball.vx or 1)
                ball.queue_deletion = True

            if ball.explode:
                ball.explode = False
                for peg in pegs:
                    x_dist = (peg.x - ball.x)
                    y_dist = (peg.y - ball.y)
                    sqdist = (x_dist*x_dist) + (y_dist*y_dist)
                    if (sqdist < (peg.radius*peg.radius) * 17):
                        peg.queue_delete = True

            ball.draw(screen)

            # remove ball if off-screen
            if ball.y - ball.radius > SCREEN_HEIGHT or ball.y - ball.radius < (-1*SCREEN_HEIGHT):
                balls.remove(ball)
            if ball.x - ball.radius > (2*SCREEN_WIDTH) or ball.x - ball.radius < (-2*SCREEN_WIDTH):
                balls.remove(ball)

            for peg in pegs:
                ball.bounce_off_peg(peg)
                if peg.queue_delete:
                    peg.switch("EMPTY")

        # draw ui and fx
        draw_game_state(screen, balls_left, peg_inventory, selected_peg, balls_in_goal, balls_needed, current_level, level_count)
        confetti.update()
        confetti.draw(screen)

        # check win
        if balls_in_goal >= balls_needed:
            pause_game_input = True
            if not game_beat and not level_beat:
                level_beat = True
                level_beat_t = pygame.time.get_ticks()
            draw_level_beat(screen)

        # check game over
        if not game_beat and not game_over and len(balls) <= 0 and balls_left <= 0:
            pause_game_input = True
            game_over = True
            game_over_start = pygame.time.get_ticks()
        if game_over:
            elapsed = pygame.time.get_ticks() - game_over_start
            progress = min(elapsed / 1000, 1.0)
            draw_game_over(screen, progress)

        pygame.display.flip()
        clock.tick(60)

def win_screen(screen):
    screen.fill("gray")

    draw_text_center(screen, ":)", SCREEN_HEIGHT // 4)
    draw_text_center(screen, "you did it", SCREEN_HEIGHT // 3)
    draw_text_center(screen, "you beat the game", 3 * SCREEN_HEIGHT // 5)
    pygame.display.flip()

    # wait for keypress
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# run game
main_menu()
game_loop()
win_screen(screen)
pygame.quit()