#!/usr/bin/env python3
import pygame
from pygame import gfxdraw
from pygame.locals import *
from elements import *
from artificial import *
from math import sin, cos


class Pong:

    def __init__(self, colourscheme, font_regular, font_bold, gamemode):
        self.colourscheme = colourscheme
        self.font_regular = font_regular
        self.font_bold = font_bold
        self.gamemode = gamemode
        self.window_size = [800, 600]
        self.screen = pygame.display.set_mode(self.window_size)
        self.border_margin = 10
        self.win_score = 8
        self.paddle_w, self.paddle_h = 20, 100
        self.paddle_max_vel = 5
        self.ball_radius = 7
        self.ball_max_vel = 10
        self.paddle1 = Paddle(self.screen, (0, self.window_size[1] // 2 - self.paddle_h // 2), self.paddle_max_vel,
                              (self.paddle_w, self.paddle_h), self.colourscheme[1])
        self.paddle2 = Paddle(self.screen, (self.window_size[0] - self.paddle_w, self.window_size[1] // 2 - self.paddle_h // 2),
                              self.paddle_max_vel, (self.paddle_w, self.paddle_h), self.colourscheme[1])
        self.ball = Ball(self.screen, (self.window_size[0] // 2, self.window_size[1] // 2), self.ball_radius,
                         self.ball_max_vel, self.colourscheme[2])
        self.scoreboard = Scoreboard(self.screen, self.window_size, self.colourscheme, self.font_bold)
        self.pause_menu = PauseMenu(self.screen, self.window_size, (self.window_size[0] // 2, self.window_size[1] // 2),
                                    self.colourscheme, self.font_regular)
        self.pause_col_rect = Rect(self.window_size[0] // 2 - 55, self.window_size[1] - self.border_margin - 30, 25, 20)
        self.continue_col_rect = Rect(self.window_size[0] // 2 + 30, self.window_size[1] - self.border_margin - 30, 25, 20)
        self.pause_button_rect1 = (self.window_size[0] // 2 - 55, self.window_size[1] - self.border_margin - 30, 10, 20)
        self.pause_button_rect2 = (self.window_size[0] // 2 - 40, self.window_size[1] - self.border_margin - 30, 10, 20)
        self.continue_trigon_poings = ((self.window_size[0] // 2 + 30, self.window_size[1] - self.border_margin - 30),
                                       (self.window_size[0] // 2 + 30, self.window_size[1] - self.border_margin - 10),
                                       (self.window_size[0] // 2 + 55, self.window_size[1] - self.border_margin - 20))

        def set_ai():
            if self.gamemode == 1:
                self.ai = EasyOpponent(self.paddle2.y, self.paddle2.height, self.paddle2.max_vel)
            else:
                self.ai = None

        set_ai()

    def handle_pause(self):
        clock = pygame.time.Clock()
        pause = 1

        while pause:
            mouse = pygame.mouse.get_pos()
            self.pause_menu.draw("GAME PAUSED")

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif e.type == MOUSEBUTTONDOWN and self.continue_col_rect.collidepoint(mouse):
                    pause = 0

            clock.tick(60)
            pygame.display.update()

        return False

    def update(self, keys):

        def render_elements():
            self.screen.fill(self.colourscheme[0])

            for p in [self.paddle1, self.paddle2]:
                p.draw()

            self.ball.draw()
            self.scoreboard.draw()

            y = 0
            while y < self.window_size[1]:
                pygame.draw.rect(self.screen, self.colourscheme[3], (self.window_size[0] // 2 - 5, y, 5, 13))
                y += 25

            # stop & start visuals
            pygame.draw.rect(self.screen, self.colourscheme[3], self.pause_button_rect1)
            pygame.draw.rect(self.screen, self.colourscheme[3], self.pause_button_rect2)
            pygame.gfxdraw.filled_trigon(self.screen, self.continue_trigon_poings[0][0], self.continue_trigon_poings[0][1], self.continue_trigon_poings[1][0],
                                         self.continue_trigon_poings[1][1], self.continue_trigon_poings[2][0], self.continue_trigon_poings[2][1], self.colourscheme[3])

        def end_and_reset(winner):
            clock = pygame.time.Clock()
            end = 1

            while end:
                mouse = pygame.mouse.get_pos()

                if self.gamemode == 0:
                    self.pause_menu.draw(f"{winner} WON")
                else:
                    self.pause_menu.draw(f"{'P' if winner == '1' else 'AI'} WON")
                    self.ai.reset()

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        return True
                    elif e.type == MOUSEBUTTONDOWN and self.continue_col_rect.collidepoint(mouse):
                        end = 0

                clock.tick(60)
                pygame.display.update()

            self.scoreboard.reset()
            self.paddle1.reset()
            self.paddle2.reset()
            self.ball.reset()

        def check_ball_collision():
            left_y_middle = self.paddle1.y + self.paddle1.height // 2
            right_y_middle = self.paddle2.y + self.paddle2.height // 2
            paddle_height = self.paddle1.height

            is_left_x_collision = self.ball.x - self.ball.radius - self.ball.max_vel <= self.paddle1.x + self.paddle1.width and self.ball.x_vel < 0
            is_right_x_collision = self.ball.x + self.ball.radius + self.ball.max_vel >= self.paddle2.x and self.ball.x_vel > 0

            is_left_y_collision = self.paddle1.y - self.ball.radius * 1.5 < self.ball.y < self.paddle1.y + paddle_height + self.ball.radius * 1.5
            is_right_y_collision = self.paddle2.y - self.ball.radius * 1.5 < self.ball.y < self.paddle2.y + paddle_height + self.ball.radius * 1.5

            is_left_edge = self.ball.x < self.paddle1.x + self.paddle1.width
            is_right_edge = self.ball.x > self.paddle2.x

            # wall-collision
            if self.ball.y - self.ball.radius <= 0 and self.ball.y_vel < 0:
                self.ball.y_vel *= -1
            elif self.ball.y + self.ball.radius >= self.window_size[1] and self.ball.y_vel > 0:
                self.ball.y_vel *= -1

            # paddle-collision
            if is_left_x_collision and is_left_y_collision:
                if is_left_edge:
                    self.ball.y_vel *= -1
                else:
                    self.ball.y_vel = ((self.ball.y - left_y_middle) / paddle_height) * self.ball.max_vel
                    self.ball.x_vel = self.ball.max_vel - abs(self.ball.y_vel) * 0.5
            elif is_right_x_collision and is_right_y_collision:
                if is_right_edge:
                    self.ball.y_vel *= -1
                else:
                    self.ball.y_vel = ((self.ball.y - right_y_middle) / paddle_height) * self.ball.max_vel
                    self.ball.x_vel = -self.ball.max_vel + abs(self.ball.y_vel) * 0.5

        def check_goal():
            if self.ball.x <= 0:
                self.scoreboard.update(0)
            elif self.ball.x >= self.window_size[0]:
                self.scoreboard.update(1)
            else:
                return

            if self.scoreboard.score1 == self.win_score:
                end_and_reset("1")
            elif self.scoreboard.score2 == self.win_score:
                end_and_reset("2")
            else:
                self.ball.reset()

        def check_paddle_movement():
            if keys[K_f] and self.paddle1.y + self.paddle1.max_vel < self.window_size[1] - self.paddle1.height:
                self.paddle1.move(dir=2)

            if keys[K_d] and self.paddle1.y + self.paddle1.max_vel > 0:
                self.paddle1.move(dir=1)

            if keys[K_j] and self.paddle2.y + self.paddle2.max_vel < self.window_size[1] - self.paddle2.height and self.gamemode == 0:
                self.paddle2.move(dir=2)

            if keys[K_k] and self.paddle2.y + self.paddle2.max_vel > 0 and self.gamemode == 0:
                self.paddle2.move(dir=1)

        def check_ai_movement():
            move = self.ai.check_required_move(self.ball.y)

            if move:
                self.paddle2.move(move)

        check_paddle_movement()
        if self.ai:
            check_ai_movement()
        self.ball.move()
        check_ball_collision()
        check_goal()
        render_elements()
