from Apple import Apple
from BFS_algo import BFS
from snake_info import Snake
from game_run import Player


class Mixed(Player):
    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple, **kwargs)
        self.kwargs = kwargs

    def escape(self):
        head = self.snake.get_head()
        largest_neibhour_apple_distance = 0
        newhead = None
        for diff in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            neibhour = self.node_add(head, diff)

            if self.snake.dead_checking(head=neibhour, check=True):
                continue

            neibhour_apple_distance = (
                abs(neibhour[0] - self.apple.location[0]) + abs(neibhour[1] - self.apple.location[1])
            )
            # Find the neibhour which has greatest Manhattan distance to apple and has path to tail
            if largest_neibhour_apple_distance < neibhour_apple_distance:
                snake_tail = Apple()
                snake_tail.location = self.snake.body[1]
                # Create a virtual snake with a neibhour as head, to see if it has a way to its tail,
                # thus remove two nodes from body: one for moving one step forward, one for avoiding dead checking
                snake = Snake(body=self.snake.body[2:] + [neibhour])
                bfs = BFS(snake=snake, apple=snake_tail, **self.kwargs)
                path = bfs.run_bfs()
                if path is None:
                    continue
                largest_neibhour_apple_distance = neibhour_apple_distance
                newhead = neibhour
        return newhead

    def run_mixed(self):
        """
        Mixed strategy
        """
        bfs = BFS(snake=self.snake, apple=self.apple, **self.kwargs)

        path = bfs.run_bfs()

        # If the snake does not have the path to apple, try to follow its tail to escape
        if path is None:
            return self.escape()

        # Send a virtual snake to see when it reaches the apple, does it still have a path to its own tail, to keep it
        # alive
        length = len(self.snake.body)
        virtual_snake_body = (self.snake.body + path[1:])[-length:]
        virtual_snake_tail = Apple()
        virtual_snake_tail.location = (self.snake.body + path[1:])[-length - 1]
        virtual_snake = Snake(body=virtual_snake_body)
        virtual_snake_longest = BFS(snake=virtual_snake, apple=virtual_snake_tail, **self.kwargs)
        virtual_snake_longest_path = virtual_snake_longest.run_bfs()
        if virtual_snake_longest_path is None:
            return self.escape()
        else:
            return path[1]