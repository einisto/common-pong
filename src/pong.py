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

    middle_y = 0
    while middle_y < size[1]:
        pygame.draw.rect(screen, colourscheme[1], (x_mid - 5, middle_y, 5, 13))
        middle_y += 25

    # stop
    pygame.draw.rect(
        screen, colourscheme[1], (x_mid - 55, size[1] - border_margin - 30, 10, 20))
    pygame.draw.rect(
        screen, colourscheme[1], (x_mid - 40, size[1] - border_margin - 30, 10, 20))

    # start
    pygame.gfxdraw.filled_trigon(screen, x_mid + 30, size[1] - border_margin - 30, x_mid + 30,
                                 size[1] - border_margin - 10, x_mid + 55, size[1] - border_margin - 20, colourscheme[1])


def start_pause():
    # TODO
    print("pause started")


def stop_pause():
    # TODO
    print("pause ended")


def handle_collision(window_height, left_paddle, right_paddle, ball):
    left_middle = left_paddle.y + left_paddle.height // 2
    right_middle = right_paddle.y + right_paddle.height // 2
    paddle_height = left_paddle.height

    # wall-ball-collision
    if ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    elif ball.y + ball.radius >= window_height:
        ball.y_vel *= -1

    # paddle-ball-collision
    if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
        if left_paddle.y < ball.y < left_paddle.y + paddle_height:
            ball.y_vel = ((ball.y - left_middle) /
                          paddle_height) * ball.max_vel
            ball.x_vel *= -1
            print(ball.y_vel)
    elif ball.x + ball.radius >= right_paddle.x:
        if right_paddle.y < ball.y < right_paddle.y + paddle_height:
            ball.y_vel = ((ball.y - right_middle) /
                          paddle_height) * ball.max_vel
            ball.x_vel *= -1
            print(ball.y_vel)


def handle_config(high_res, gamemode):
    if high_res:
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


def main(colourscheme, high_res, gamemode=None):
    pygame.init()

    size, font, border_margin = handle_config(high_res, gamemode)
    screen = pygame.display.set_mode([size[0], size[1]])
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()

    # visual elements
    paddle1 = Paddle(screen, border_margin,
                     size[1] // 2 - PADDLE_HEIGHT // 2, colourscheme[1])
    paddle2 = Paddle(screen, size[0] - border_margin - PADDLE_WIDTH,
                     size[1] // 2 - PADDLE_HEIGHT // 2, colourscheme[1])
    ball = Ball(screen, size[0] // 2, size[1] // 2, colourscheme[1])
    scoreboard = Scoreboard(
        screen, size[0] // 2, size[0] // 4, 3 * border_margin, colourscheme[1], font)

    act_rect = Rect(size[0] // 2 - 55, size[1] - border_margin - 30, 25, 20)
    act_trigon = Rect(size[0] // 2 + 30, size[1] - border_margin - 30, 25, 20)

    pause = 0
    done = 0
    while not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = 1
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if act_rect.collidepoint(mouse) and not pause:
                    pause = 1
                    start_pause()
                elif act_trigon.collidepoint(mouse) and pause:
                    pause = 0
                    stop_pause()

        check_paddle_movement(size[1], border_margin, keys, paddle1, paddle2)

        ball.move()
        handle_collision(size[1], paddle1, paddle2, ball)

        if check_goal(ball.x, size[0], scoreboard):
            if scoreboard.game_end():
                scoreboard.reset()
                paddle1.reset()
                paddle2.reset()
                ball.reset()
                # tmp solution
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
