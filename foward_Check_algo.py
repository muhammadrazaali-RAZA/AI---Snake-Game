from game_run import Player
from Apple import Apple
from long_path_algo import LongestPath
from BFS_algo import BFS
from snake_info import Snake

class Fowardcheck(Player):
    longgest_path_cache = []
    
    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple, **kwargs)
        self.kwargs = kwargs

    def run_forwardcheck(self):
        bfs = BFS(snake=self.snake, apple=self.apple, **self.kwargs)

        path = bfs.run_bfs()

        print("trying BFS")

        if path is None:
            snake_tail = Apple()
            snake_tail.location = self.snake.body[0]
            snake = Snake(body=self.snake.body[1:])
            longest_path = LongestPath(snake=snake, apple=snake_tail, **self.kwargs).run_longest()
            next_node = longest_path[0]
            # print("BFS not reachable, trying head to tail")
            # print(next_node)
            return next_node

        length = len(self.snake.body)
        virtual_snake_body = (self.snake.body + path[1:])[-length:]
        virtual_snake_tail = Apple()
        virtual_snake_tail.location = (self.snake.body + path[1:])[-length - 1]
        virtual_snake = Snake(body=virtual_snake_body)
        virtual_snake_longest = LongestPath(snake=virtual_snake, apple=virtual_snake_tail, **self.kwargs)
        virtual_snake_longest_path = virtual_snake_longest.run_longest()
        if virtual_snake_longest_path is None:
            snake_tail = Apple()
            snake_tail.location = self.snake.body[0]
            snake = Snake(body=self.snake.body[1:])
            longest_path = LongestPath(snake=snake, apple=snake_tail, **self.kwargs).run_longest()
            next_node = longest_path[0]
            # print("virtual snake not reachable, trying head to tail")
            # print(next_node)
            return next_node
        else:
            # print("BFS accepted")
            return path[1]