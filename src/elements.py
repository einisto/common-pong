#!/usr/bin/env python3
import pygame
from pygame.locals import *
from constants import *


class Paddle:
    def __init__(self, screen, x, y, colour):
        self.screen = screen
        self.max_vel = PADDLE_MAX_VEL
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.colour = colour

    def draw(self):
        pygame.draw.rect(self.screen, self.colour,
                         (self.x, self.y, self.width, self.height))

    def move(self, down):
        if down:
            self.y += self.max_vel
        else:
            self.y -= self.max_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    def __init__(self, screen, x, y, colour):
        self.screen = screen
        self.radius = BALL_RADIUS
        self.max_vel = BALL_MAX_VEL
        self.x_vel = BALL_MAX_VEL
        self.y_vel = 0
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.colour = colour

    def draw(self):
        pygame.draw.circle(self.screen, self.colour,
                           (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


class Scoreboard:
    def __init__(self, screen, window_middle, x, y, colour, font):
        self.screen = screen
        self.font = font
        self.window_middle = window_middle
        self.x = x
        self.y = y
        self.colour = colour
        self.score1 = self.score2 = 0

    def update(self, scorer):
        if scorer:
            self.score1 += 1
        else:
            self.score2 += 1

    def game_end(self):
        return self.score1 == 8 or self.score2 == 8

    def draw(self):
        label1 = self.font.render(str(self.score1), 1, self.colour)
        label2 = self.font.render(str(self.score2), 1, self.colour)
        label1.set_alpha(100)
        label2.set_alpha(100)
        self.screen.blit(label1, (self.x, self.y))
        self.screen.blit(label2, (self.window_middle +
                         self.x - label1.get_width(), self.y))

    def highlight(self):
        # https://stackoverflow.com/questions/25714188/pygame-and-sleep-flashing-an-image-on-the-screen-and-going-back-to-the-initial
        pass

    def reset(self):
        self.score1 = self.score2 = 0
