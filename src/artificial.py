#!/usr/bin/env python3


class EasyOpponent:

    def __init__(self, y_pos, paddle_height, paddle_max_vel):
        self.paddle_max_vel = paddle_max_vel
        self.paddle_top = self.paddle_top_original = y_pos
        self.paddle_bottom = self.paddle_bottom_original = y_pos + paddle_height

    def check_required_move(self, ball_pos):
        if ball_pos[1] < self.paddle_top:
            # paddle up
            self.paddle_top -= self.paddle_max_vel
            self.paddle_bottom -= self.paddle_max_vel
            return 1
        elif ball_pos[1] > self.paddle_bottom:
            # paddle down
            self.paddle_top += self.paddle_max_vel
            self.paddle_bottom += self.paddle_max_vel
            return 2
        else:
            return 0

    def reset(self):
        self.paddle_top = self.paddle_top_original
        self.paddle_bottom = self.paddle_bottom_original
