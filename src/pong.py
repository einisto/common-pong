#!/usr/bin/env python3
import pygame
import argparse
from pygame import gfxdraw
from pygame.locals import *
from constants import *
from elements import Paddle, Ball, Scoreboard


def render_elements(screen, colourscheme, size, border_margin, paddles, ball, scoreboard):
    screen.fill(colourscheme[0])

    for p in paddles:
        p.draw()

    ball.draw()
    scoreboard.draw()

    # static elements

    x_mid = size[0] // 2

    middle_line_y = 0
    while middle_line_y < size[1]:
        pygame.draw.rect(screen, colourscheme[1], (x_mid - 5, middle_line_y, 5, 13))
        middle_line_y += 25

    # stop-button
    pygame.draw.rect(
        screen, colourscheme[1], (x_mid - 55, size[1] - border_margin - 30, 10, 20))
    pygame.draw.rect(
        screen, colourscheme[1], (x_mid - 40, size[1] - border_margin - 30, 10, 20))

    # start-button
    pygame.gfxdraw.filled_trigon(screen, x_mid + 30, size[1] - border_margin - 30, x_mid + 30,
                                 size[1] - border_margin - 10, x_mid + 55, size[1] - border_margin - 20, colourscheme[1])


def handle_pause(screen, continue_rect):
    pause = 1

    while pause:
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return True
            elif e.type == MOUSEBUTTONDOWN and continue_rect.collidepoint(mouse):
                pause = 0

    return False


def check_ball_collision(window_height, left_paddle, right_paddle, ball):
    left_y_middle = left_paddle.y + left_paddle.height // 2
    right_y_middle = right_paddle.y + right_paddle.height // 2
    paddle_height = left_paddle.height

    is_left_x_collision = ball.x - ball.radius <= left_paddle.x + \
        left_paddle.width and ball.x_vel < 0
    is_left_y_collision = left_paddle.y - \
        ball.radius < ball.y < left_paddle.y + paddle_height + ball.radius
    is_left_edge = ball.x < left_paddle.x + left_paddle.width
    is_right_x_collision = ball.x + ball.radius >= right_paddle.x and ball.x_vel > 0
    is_right_y_collision = right_paddle.y - \
        ball.radius < ball.y < right_paddle.y + paddle_height + ball.radius
    is_right_edge = ball.x > right_paddle.x

    # wall-ball-collision
    if ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    elif ball.y + ball.radius >= window_height:
        ball.y_vel *= -1

    # paddle-ball-collision
    if is_left_x_collision and is_left_y_collision:
        if is_left_edge:
            ball.y_vel *= -1
        else:
            ball.y_vel = ((ball.y - left_y_middle) /
                          paddle_height) * ball.max_vel
            ball.x_vel *= -1
    elif is_right_x_collision and is_right_y_collision:
        if is_right_edge:
            ball.y_vel *= -1
        else:
            ball.y_vel = ((ball.y - right_y_middle) /
                          paddle_height) * ball.max_vel
            ball.x_vel *= -1


def handle_config(is_high_res, gamemode):
    if is_high_res:
        size = (HR_WIDTH, HR_HEIGHT)
        font = pygame.font.SysFont(
            HR_FONT[0], HR_FONT[1], bold=True, italic=False)
        border_margin = 15
    else:
        size = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
        font = pygame.font.SysFont(
            DEFAULT_FONT[0], DEFAULT_FONT[1], bold=True, italic=False)
        border_margin = 10

    return size, font, border_margin


def check_paddle_movement(window_height, border_margin, keys, paddle1, paddle2):
    if keys[K_f] and paddle1.y + paddle1.max_vel < window_height - border_margin - paddle1.height:
        paddle1.move(down=True)

    if keys[K_d] and paddle1.y + paddle1.max_vel > border_margin + 5:
        paddle1.move(down=False)

    if keys[K_j] and paddle2.y + paddle2.max_vel < window_height - border_margin - paddle2.height:
        paddle2.move(down=True)

    if keys[K_k] and paddle2.y + paddle2.max_vel > border_margin + 5:
        paddle2.move(down=False)


def check_goal(ball_x, window_width, scoreboard):
    if ball_x <= 0:
        scoreboard.update(0)
        return True
    elif ball_x >= window_width:
        scoreboard.update(1)
        return True

    return False


def main(colourscheme, is_high_res, gamemode=None):
    pygame.init()

    size, font, border_margin = handle_config(is_high_res, gamemode)
    screen = pygame.display.set_mode([size[0], size[1]])
    pygame.display.set_caption("deus-pong")
    clock = pygame.time.Clock()

    # visual elements
    paddle1 = Paddle(screen, 0,
                     size[1] // 2 - PADDLE_HEIGHT // 2, colourscheme[1])
    paddle2 = Paddle(screen, size[0] - PADDLE_WIDTH,
                     size[1] // 2 - PADDLE_HEIGHT // 2, colourscheme[1])
    ball = Ball(screen, size[0] // 2, size[1] // 2, colourscheme[1])
    scoreboard = Scoreboard(
        screen, size[0] // 2, size[0] // 4, 3 * border_margin, colourscheme[1], font)

    pause_rect = Rect(size[0] // 2 - 55, size[1] - border_margin - 30, 25, 20)
    continue_rect = Rect(size[0] // 2 + 30, size[1] - border_margin - 30, 25, 20)

    done = 0
    while not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = 1
            elif e.type == pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(mouse):
                if handle_pause(screen, continue_rect):
                    done = 1
                    return

        check_paddle_movement(size[1], border_margin, keys, paddle1, paddle2)

        ball.move()
        check_ball_collision(size[1], paddle1, paddle2, ball)

        if check_goal(ball.x, size[0], scoreboard):
            if scoreboard.game_end():
                scoreboard.reset()
                paddle1.reset()
                paddle2.reset()
                ball.reset()
                # TODO: tmp solution
                pygame.time.wait(2000)
            else:
                ball.reset()

        render_elements(screen, colourscheme, size, border_margin,
                        (paddle1, paddle2), ball, scoreboard)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Classic game of Pong with a few comfy additions")

    # TODO: add argument to choose between lan/wifi, ai & local (gamemode-argument in main)
    parser.add_argument("-r", action="store_true",
                        help="Use higher resolution (1200x900)")
    parser.add_argument("-c", default="default",
                        metavar="scheme", help="Select a colourscheme")

    args = parser.parse_args()

    if args.c not in COLOURSCHEMES.keys():
        print(f"{TERMINAL_RED}Colourscheme {args.c} not found: continuing with default option{TERMINAL_NC}")
        args.c = "default"

    scheme = COLOURSCHEMES[args.c]

    main(scheme, args.r)
