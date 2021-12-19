from Apple import Apple
from snake_info import Snake
from display import display_base


class Player(display_base):
    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(**kwargs)
        self.snake = snake
        self.apple = apple
    
    def explore_neighbors(self, node):
        """
        fetch and yield the four neighbours of a node
        :param node: (node_x, node_y)
        """
        for diff in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            yield self.node_add(node, diff)

    @staticmethod
    def is_node_in_queue(node: tuple, queue: iter):
        """
        Check if element is in a nested list
        """
        return any(node in sublist for sublist in queue)

    def is_invalid_move(self, node: tuple, snake: Snake):
        """
        Similar to dead_checking, this method checks if a given node is a valid move
        :return: Boolean
        """
        x, y = node
        if not 0 <= x < self.cell_width or not 0 <= y < self.cell_height or node in snake.body:
            return True
        return False