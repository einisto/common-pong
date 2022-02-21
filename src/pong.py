#!/usr/bin/env python3
import pygame
import argparse
from pygame import gfxdraw
from pygame.locals import *
from constants import *
from elements import Paddle, Ball, Scoreboard


def draw_elements(screen, colourscheme, size, border_margin, paddles, ball, scoreboard):
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
    pass


def stop_pause():
    # TODO
    pass


def handle_collision():
    pass


def main(colourscheme, high_res, gamemode=None):
    pygame.init()

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

    act_rect = Rect(x_mid - 55, size[1] - border_margin - 30, 25, 20)
    act_trigon = Rect(x_mid + 30, size[1] - border_margin - 30, 25, 20)

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
                    start_pause()
                elif act_trigon.collidepoint(mouse) and pause:
                    stop_pause()

        if keys[K_f] and paddle1.y + paddle1.max_vel < size[1] - border_margin - paddle1.height:
            paddle1.move(down=True)

        if keys[K_d] and paddle1.y + paddle1.max_vel > border_margin + 5:
            paddle1.move(down=False)

        if keys[K_j] and paddle2.y + paddle2.max_vel < size[1] - border_margin - paddle2.height:
            paddle2.move(down=True)

        if keys[K_k] and paddle2.y + paddle2.max_vel > border_margin + 5:
            paddle2.move(down=False)

        draw_elements(screen, colourscheme, size, border_margin,
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