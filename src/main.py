#!/usr/bin/env python3
import pygame
import argparse
from pygame.locals import *
from pong import Pong
from constants import *


def check_colourscheme(colourscheme_name_lowercase):
    if colourscheme_name_lowercase in COLOURSCHEMES.keys():
        return COLOURSCHEMES[colourscheme_name_lowercase]
    else:
        print(f"{TERMINAL_RED}Colourscheme '{colourscheme_name_lowercase}' not found: continuing with default{TERMINAL_NC}")
        return COLOURSCHEMES["default"]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Classic game of Pong with a few comfy additions")

    # TODO: add flag to choose between lan/wifi, ai & local (gamemode-argument in main)
    parser.add_argument("-g", default=0, metavar="mode", help="Select a gamemode")
    parser.add_argument("-c", default="default", metavar="name", help="Select a colourscheme")

    args = parser.parse_args()

    return int(args.g), check_colourscheme(args.c.lower())


def main(gamemode, colourscheme):
    pygame.init()
    pygame.display.set_caption("deus-pong")
    clock = pygame.time.Clock()

    font_regular = pygame.font.Font("font/Hack-Regular.ttf", 40)
    font_bold = pygame.font.Font("font/Hack-Bold.ttf", 60)

    pong = Pong(colourscheme, font_regular, font_bold, gamemode)

    done = 0
    while not done:
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = 1
            elif e.type == pygame.MOUSEBUTTONDOWN and pong.pause_col_rect.collidepoint(mouse):
                if pong.handle_pause():
                    done = 1
                    return

        pong.update(keys)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    gamemode, colourscheme = parse_arguments()
    main(gamemode, colourscheme)
