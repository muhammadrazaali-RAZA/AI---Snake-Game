from game_run import Player
from Apple import Apple
from snake_info import Snake


def heuristic(start, goal):
    return (start[0] - goal[0])**2 + (start[1] - goal[1])**2

class Astar(Player):
    def __init__(self, snake: Snake, apple: Apple, **kwargs):
        """
        :param snake: Snake instance
        :param apple: Apple instance
        """
        super().__init__(snake=snake, apple=apple, **kwargs)
        self.kwargs = kwargs

    def run_astar(self):
        came_from = {}
        close_list = set()
        goal = self.apple.location
        start = self.snake.get_head()
        dummy_snake = Snake(body=self.snake.body)
        neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        gscore = {start: 0}
        fscore = {start: heuristic(start, goal)}
        open_list = [(fscore[start], start)]
        print(start, goal, open_list)
        while open_list:
            current = min(open_list, key=lambda x: x[0])[1]
            open_list.pop(0)
            print(current)
            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                    print(data)
                return data[-1]

            close_list.add(current)

            for neighbor in neighbors:
                neighbor_node = self.node_add(current, neighbor)

                if dummy_snake.dead_checking(head=neighbor_node) or neighbor_node in close_list:
                    continue
                if sum(map(abs, self.node_sub(current, neighbor_node))) == 2:
                    diff = self.node_sub(current, neighbor_node)
                    if dummy_snake.dead_checking(head=self.node_add(neighbor_node, (0, diff[1]))
                                                 ) or self.node_add(neighbor_node, (0, diff[1])) in close_list:
                        continue
                    elif dummy_snake.dead_checking(head=self.node_add(neighbor_node, (diff[0], 0))
                                                   ) or self.node_add(neighbor_node, (diff[0], 0)) in close_list:
                        continue
                tentative_gscore = gscore[current] + heuristic(current, neighbor_node)
                if tentative_gscore < gscore.get(neighbor_node, 0) or neighbor_node not in [i[1] for i in open_list]:
                    gscore[neighbor_node] = tentative_gscore
                    fscore[neighbor_node] = tentative_gscore + heuristic(neighbor_node, goal)
                    open_list.append((fscore[neighbor_node], neighbor_node))
                    came_from[neighbor_node] = current