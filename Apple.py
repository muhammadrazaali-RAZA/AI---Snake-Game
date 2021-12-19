import random
from display import display_base
from itertools import product

class Apple(display_base):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.location = None

    def refresh(self, snake):
        """
        Generate a new apple
        """
        available_positions = set(product(range(self.cell_width - 1), range(self.cell_height - 1))) - set(snake.body)

        # If there's no available node for new apple, it reaches the perfect solution. Don't draw the apple then.
        location = random.sample(available_positions, 1)[0] if available_positions else (-1, -1)

        self.location = location
        