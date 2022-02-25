#!/usr/bin/env python3
import pygame
import argparse
from pygame import gfxdraw
from pygame.locals import *
from constants import *

CHOSEN_COLOURSCHEME = COLOURSCHEMES["default"]


def set_custom_colourscheme(selection):
    CHOSEN_COLOURSCHEME = COLOURSCHEMES[selection]
    PADDLE1.colour = CHOSEN_COLOURSCHEME[1]
    PADDLE2.colour = CHOSEN_COLOURSCHEME[1]
    BALL.colour = CHOSEN_COLOURSCHEME[1]
    SCOREBOARD.colourscheme = CHOSEN_COLOURSCHEME
    PAUSE_MENU.colourscheme = CHOSEN_COLOURSCHEME


def render_elements():
    SCREEN.fill(CHOSEN_COLOURSCHEME[0])

    for p in [PADDLE1, PADDLE2]:
        p.draw()
    BALL.draw()
    SCOREBOARD.draw()

    y = 0
    while y < WINDOW_SIZE[1]:
        pygame.draw.rect(
            SCREEN, CHOSEN_COLOURSCHEME[1], (WINDOW_SIZE[0] // 2 - 5, y, 5, 13))
        y += 25

    # stop & start visuals
    pygame.draw.rect(SCREEN, CHOSEN_COLOURSCHEME[1], PAUSE_BUTTON_RECT1)
    pygame.draw.rect(SCREEN, CHOSEN_COLOURSCHEME[1], PAUSE_BUTTON_RECT2)
    pygame.gfxdraw.filled_trigon(SCREEN, CONTINUE_TRIGON_POINTS[0][0], CONTINUE_TRIGON_POINTS[0][1], CONTINUE_TRIGON_POINTS[1]
                                 [0], CONTINUE_TRIGON_POINTS[1][1], CONTINUE_TRIGON_POINTS[2][0], CONTINUE_TRIGON_POINTS[2][1], CHOSEN_COLOURSCHEME[1])


def handle_pause():
    clock = pygame.time.Clock()
    pause = 1

    while pause:
        mouse = pygame.mouse.get_pos()
        PAUSE_MENU.draw()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return True
            elif e.type == MOUSEBUTTONDOWN and CONTINUE_COL_RECT.collidepoint(mouse):
                pause = 0

        clock.tick(60)
        pygame.display.update()

    return False


def check_ball_collision():
    left_y_middle = PADDLE1.y + PADDLE1.height // 2
    right_y_middle = PADDLE2.y + PADDLE2.height // 2
    paddle_height = PADDLE1.height

    is_left_x_collision = BALL.x - BALL.radius <= PADDLE1.x + PADDLE1.width and BALL.x_vel < 0
    is_left_y_collision = PADDLE1.y - BALL.radius < BALL.y < PADDLE1.y + paddle_height + BALL.radius
    is_left_edge = BALL.x < PADDLE1.x + PADDLE1.width
    is_right_x_collision = BALL.x + BALL.radius >= PADDLE2.x and BALL.x_vel > 0
    is_right_y_collision = PADDLE2.y - BALL.radius < BALL.y < PADDLE2.y + paddle_height + BALL.radius
    is_right_edge = BALL.x > PADDLE2.x

    # wall-collision
    if BALL.y - BALL.radius <= 0:
        BALL.y_vel *= -1
    elif BALL.y + BALL.radius >= WINDOW_SIZE[1]:
        BALL.y_vel *= -1

    # paddle-collision
    if is_left_x_collision and is_left_y_collision:
        if is_left_edge:
            BALL.y_vel *= -1
        else:
            BALL.y_vel = ((BALL.y - left_y_middle) /
                          paddle_height) * BALL.max_vel
            BALL.x_vel = BALL.max_vel - abs(BALL.y_vel) * 0.5
    elif is_right_x_collision and is_right_y_collision:
        if is_right_edge:
            BALL.y_vel *= -1
        else:
            BALL.y_vel = ((BALL.y - right_y_middle) /
                          paddle_height) * BALL.max_vel
            BALL.x_vel = -BALL.max_vel + abs(BALL.y_vel) * 0.5


def check_paddle_movement(keys):
    if keys[K_f] and PADDLE1.y + PADDLE1.max_vel < WINDOW_SIZE[1] - PADDLE1.height:
        PADDLE1.move(is_down=True)

    if keys[K_d] and PADDLE1.y + PADDLE1.max_vel > 0:
        PADDLE1.move(is_down=False)

    if keys[K_j] and PADDLE2.y + PADDLE2.max_vel < WINDOW_SIZE[1] - PADDLE2.height:
        PADDLE2.move(is_down=True)

    if keys[K_k] and PADDLE2.y + PADDLE2.max_vel > 0:
        PADDLE2.move(is_down=False)


def check_goal():
    if BALL.x <= 0:
        SCOREBOARD.update(0)
        return True
    elif BALL.x >= WINDOW_SIZE[0]:
        SCOREBOARD.update(1)
        return True

    return False


def end_and_reset():
    # TODO display winner score
    pygame.time.wait(2000)

    SCOREBOARD.reset()
    PADDLE1.reset()
    PADDLE2.reset()
    BALL.reset()


def main(gamemode=None):
    pygame.init()
    pygame.display.set_caption(WINDOW_CAPTION)
    clock = pygame.time.Clock()

    SCOREBOARD.font = pygame.font.Font("font/Hack-Bold.ttf", 60)
    PAUSE_MENU.font = pygame.font.Font("font/Hack-Regular.ttf", 40)

    done = 0
    while not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = 1
            elif e.type == pygame.MOUSEBUTTONDOWN and PAUSE_COL_RECT.collidepoint(mouse):
                if handle_pause():
                    done = 1
                    return

        check_paddle_movement(keys)
        BALL.move()
        check_ball_collision()

        if check_goal():
            if SCOREBOARD.score1 == WIN_SCORE or SCOREBOARD.score2 == WIN_SCORE:
                end_and_reset()
            else:
                BALL.reset()

        render_elements()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Classic game of Pong with a few comfy additions")

    # TODO: add argument to choose between lan/wifi, ai & local (gamemode-argument in main)
    parser.add_argument("-c", default="default",
                        metavar="scheme", help="Select a colourscheme")

    args = parser.parse_args()

    if args.c not in COLOURSCHEMES.keys():
        print(f"{TERMINAL_RED}Colourscheme {args.c} not found: continuing with default option{TERMINAL_NC}")
    else:
        set_custom_colourscheme(args.c)

    main()
