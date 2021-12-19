from game_run import Player
from Apple import Apple
from snake_info import Snake
import pygame
from heapq import *

class Human(Player):
    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple, **kwargs)

    def run(self):
        for event in pygame.event.get():  # event handling loop
            if event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and self.snake.last_direction != (1, 0):
                    diff = (-1, 0)  # left
                elif (event.key == K_RIGHT or event.key == K_d) and self.snake.last_direction != (-1, 0):
                    diff = (1, 0)  # right
                elif (event.key == K_UP or event.key == K_w) and self.snake.last_direction != (0, 1):
                    diff = (0, -1)  # up
                elif (event.key == K_DOWN or event.key == K_s) and self.snake.last_direction != (0, -1):
                    diff = (0, 1)  # down
                else:
                    break
                return self.node_add(self.snake.get_head(), diff)
        # If no button is pressed down, follow previou direction
        return self.node_add(self.snake.get_head(), self.snake.last_direction)