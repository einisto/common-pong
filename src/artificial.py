#!/usr/bin/env python3


class EasyOpponent:

    def __init__(self, paddle_y_mid, paddle_max_vel, paddle_height, window_height):
        self.paddle_y_mid = self.paddle_y_mid_orig = paddle_y_mid
        self.paddle_max_vel = paddle_max_vel
        self.deadzone = paddle_height // 3
        self.half_height = paddle_height // 2
        self.window_height = window_height

    def check_required_move(self, ball_pos):
        if ball_pos[1] < self.paddle_y_mid - self.deadzone and self.paddle_y_mid - self.half_height > 0:
            # paddle up
            self.paddle_y_mid -= self.paddle_max_vel
            return 1
        elif ball_pos[1] > self.paddle_y_mid + self.deadzone and self.paddle_y_mid + self.half_height < self.window_height:
            # paddle down
            self.paddle_y_mid += self.paddle_max_vel
            return 2
        else:
            return 0

    def reset(self):
        self.paddle_y_mid = self.paddle_y_mid_orig
