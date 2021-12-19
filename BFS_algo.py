from game_run import Player
from Apple import Apple
from snake_info import Snake


class BFS(Player):
    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple, **kwargs)

    def run_bfs(self):
        """
        Run BFS searching and return the full path of best way to apple from BFS searching
        """
        queue = [[self.snake.get_head()]]

        while queue:
            path = queue[0]
            future_head = path[-1]

            # If snake eats the apple, return the next move after snake's head
            if future_head == self.apple.location:
                return path

            for next_node in self.explore_neighbors(future_head):
                if (
                    self.is_invalid_move(node=next_node, snake=self.snake)
                    or self.is_node_in_queue(node=next_node, queue=queue)
                ):
                    continue
                new_path = list(path)
                new_path.append(next_node)
                queue.append(new_path)

            queue.pop(0)

    def next_node(self):
        """
        Run the BFS searching and return the next move in this path
        """
        path = self.run_bfs()
        return path[1]