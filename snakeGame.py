import contextlib
import time
import sys

from display import display_base
from snake_info import Snake
from Apple import Apple
from mixed_algo import Mixed
from heapq import *

with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    
    
    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)

#@dataclass
class snakeGame(display_base):
    
    fps: int = 60

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = kwargs

        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('AI Snake Game')

    def launch(self):
        while True:
            self.game()
            # self.showGameOverScreen()
            self.pause_game()

    def game(self):
        snake = Snake(**self.kwargs)

        apple = Apple(**self.kwargs)
        apple.refresh(snake=snake)

        step_time = []


        while True:
            
            # AI Game Player
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.terminate()

            start_time = time.time()

            # BFS Solver
            # new_head = BFS(snake=snake, apple=apple, **self.kwargs).next_node()

            # Longest Path Solver
            # this solver is calculated per apple, not per move
            # if not longgest_path_cache:
            #     longgest_path_cache = LongestPath(snake=snake, apple=apple, **self.kwargs).run_longest()
            # new_head = longgest_path_cache.pop(0)

            # A star Solver
            # new_head = Astar(snake=snake, apple=apple, **self.kwargs).run_astar()

            # FORWARD CHECKING
            # new_head = Fowardcheck(snake=snake, apple=apple, **self.kwargs).run_forwardcheck()
            new_head = Mixed(snake=snake, apple=apple, **self.kwargs).run_mixed()
            print(new_head)

            end_time = time.time()
            move_time = end_time - start_time
            # print(move_time)
            step_time.append(move_time)

            snake.move(new_head=new_head, apple=apple)

            if snake.is_dead:
                print(snake.body)
                print("Dead")
                break
            elif snake.eaten:
                apple.refresh(snake=snake)

            if snake.score + snake.initial_length >= self.cell_width * self.cell_height:
                break

            self.display.fill(BLACK)
            self.draw_panel()
            self.draw_snake(snake.body)

            self.draw_apple(apple.location)
            pygame.display.update()
            self.clock.tick(self.fps)

        print(f"Score: {snake.score}")
        print(f"Mean step time: {self.mean(step_time)}")

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def pause_game(self):
        while True:
            time.sleep(0.2)
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    self.terminate()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    else:
                        return

    def draw_snake(self, snake_body):
        for snake_block_x, snake_block_y in snake_body:
            x = snake_block_x * self.cell_size
            y = snake_block_y * self.cell_size
            snake_block = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(self.display, WHITE, snake_block)

        # Draw snake's head
        x = snake_body[-1][0] * self.cell_size
        y = snake_body[-1][1] * self.cell_size
        snake_block = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
        pygame.draw.rect(self.display, GREEN, snake_block)

        # Draw snake's tail
        x = snake_body[0][0] * self.cell_size
        y = snake_body[0][1] * self.cell_size
        snake_block = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)
        pygame.draw.rect(self.display, BLUE, snake_block)

    def draw_apple(self, apple_location):
        apple_x, apple_y = apple_location
        apple_block = pygame.Rect(apple_x * self.cell_size, apple_y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.display, RED, apple_block)

    def draw_panel(self):
        for x in range(0, self.window_width, self.cell_size):  # draw vertical lines
            pygame.draw.line(self.display, DARKGRAY, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_size):  # draw horizontal lines
            pygame.draw.line(self.display, DARKGRAY, (0, y), (self.window_width, y))
