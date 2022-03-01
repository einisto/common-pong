#!/usr/bin/env python3

COLOURSCHEMES = {
    #               bg          paddles           ball            ui
    "default": ((0, 0, 0), (255, 255, 255), (120, 120, 120), (50, 50, 50)),
    "solarized": ((7, 54, 66), (181, 137, 0), (203, 75, 22), (88, 110, 117)),
    "dracula": ((68, 71, 90), (189, 147, 249), (255, 121, 198), (248, 248, 242))
}

TERMINAL_RED = "\x1b[38;2;255;0;0m"
TERMINAL_NC = "\033[0m"
