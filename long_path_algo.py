from Apple import Apple
from snake_info import Snake
from BFS_algo import BFS

class LongestPath(BFS):
    """
    Given shortest path, change it to the longest path
    """

    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple, **kwargs)
        self.kwargs = kwargs

    def run_longest(self):
        """
        For every move, check if it could be replace with three equivalent moves.
        For example, for snake moving one step left, check if moving up, left, and down is valid. If yes, replace the
        move with equivalent longer move. Start this over until no move can be replaced.
        """
        path = self.run_bfs()

        # print(f'longest path initial result: {path}')

        if path is None:
            # print(f"Has no Longest path")
            return

        i = 0
        while True:
            try:
                direction = self.node_sub(path[i], path[i + 1])
            except IndexError:
                break

            # Build a dummy snake with body and longest path for checking if node replacement is valid
            snake_path = Snake(body=self.snake.body + path[1:], **self.kwargs)

            # up -> left, up, right
            # down -> right, down, left
            # left -> up, left, down
            # right -> down, right, up
            for neibhour in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if direction == neibhour:
                    x, y = neibhour
                    diff = (y, x) if x != 0 else (-y, x)

                    extra_node_1 = self.node_add(path[i], diff)
                    extra_node_2 = self.node_add(path[i + 1], diff)

                    if snake_path.dead_checking(head=extra_node_1) or snake_path.dead_checking(head=extra_node_2):
                        i += 1
                    else:
                        # Add replacement nodes
                        path[i + 1:i + 1] = [extra_node_1, extra_node_2]
                    break

        # Exclude the first node, which is same to snake's head
        return path[1:]