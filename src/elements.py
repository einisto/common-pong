#!/usr/bin/env python3
import pygame
import random
from pygame.locals import *
from constants import *


class Paddle:

    def __init__(self, screen, pos, paddle_max_vel, paddle_size, colour):
        self.screen = screen
        self.x = self.original_x = pos[0]
        self.y = self.original_y = pos[1]
        self.max_vel = paddle_max_vel
        self.width = paddle_size[0]
        self.height = paddle_size[1]
        self.colour = colour

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))

    def move(self, dir):
        if dir == 2:
            self.y += self.max_vel
        elif dir == 1:
            self.y -= self.max_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:

    def __init__(self, screen, pos, ball_radius, ball_max_vel, colour):
        self.screen = screen
        self.x = self.original_x = pos[0]
        self.y = self.original_y = pos[1]
        self.radius = ball_radius
        self.max_vel = self.original_vel = ball_max_vel
        self.x_vel = ball_max_vel
        self.y_vel = 0
        self.colour = colour

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self, randomise):
        self.x = self.original_x
        self.y = self.original_y
        self.max_vel = self.original_vel
        self.y_vel = random.random() * self.max_vel * 0.2 if randomise else 0
        self.x_vel = self.original_vel if random.getrandbits(1) else -self.original_vel


class Scoreboard:

    def __init__(self, screen, window_size, colourscheme, font):
        self.screen = screen
        self.pos1 = (window_size[0] // 4, window_size[1] // 8)
        self.pos2 = (window_size[0] // 4 * 3, window_size[1] // 8)
        self.score1 = self.score2 = 0
        self.colourscheme = colourscheme
        self.font = font

    def update(self, is_scorer_1):
        if is_scorer_1:
            self.score1 += 1
        else:
            self.score2 += 1

    def draw(self):
        label1 = self.font.render(str(self.score1), 1, self.colourscheme[3])
        label2 = self.font.render(str(self.score2), 1, self.colourscheme[3])
        label1_rect = label1.get_rect(center=self.pos1)
        label2_rect = label2.get_rect(center=self.pos2)

        self.screen.blit(label1, label1_rect)
        self.screen.blit(label2, label2_rect)

    def reset(self):
        self.score1 = self.score2 = 0


class PauseMenu:

    def __init__(self, screen, window_size, bg_size, colourscheme, font):
        self.screen = screen
        self.bg_rect = pygame.Rect(0, 0, bg_size[0], bg_size[1])
        self.bg_rect.center = (window_size[0] // 2, window_size[1] // 2)
        self.colourscheme = colourscheme
        self.font = font

    def draw(self, display_text):
        pygame.draw.rect(self.screen, self.colourscheme[0], self.bg_rect)
        pygame.draw.rect(self.screen, self.colourscheme[2], self.bg_rect, 8)
        label = self.font.render(display_text, 1, self.colourscheme[1])
        label_rect = label.get_rect(center=self.bg_rect.center)
        self.screen.blit(label, label_rect)
