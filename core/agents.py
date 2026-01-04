from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from core.grid import Grid
from core.path import Path

import heapq
import random
from collections import deque

@dataclass(slots=True)
class Agent:
    name: str

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        raise NotImplementedError


class ExampleAgent(Agent):

    def __init__(self):
        super().__init__("Example")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        nodes = [start]
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4(r, c)

            min_dist = min(grid.manhattan(t.pos, goal) for t in neighbors)
            best_tiles = [
                tile for tile in neighbors
                if grid.manhattan(tile.pos, goal) == min_dist
            ]
            best_tile = best_tiles[random.randint(0, len(best_tiles) - 1)]

            nodes.append(best_tile.pos)

        return Path(nodes)


class DFSAgent(Agent):

    def __init__(self):
        super().__init__("DFS")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        stack = [(start, [start])]  

        DIRECTION_PRIORITY = {
           (0, 1): 0,   
           (1, 0): 1,   
           (0, -1): 2, 
           (-1, 0): 3  
        }
        while stack:
            (r, c), path = stack.pop()

            if (r, c) == goal:
                return Path(path)

            neighbors = grid.neighbors4(r, c)

            neighbors.sort(
                key=lambda tile: (
                    tile.cost,
                    DIRECTION_PRIORITY[
                        (tile.pos[0] - r, tile.pos[1] - c)
                    ]
                ),
                reverse=True 
            )

            for tile in neighbors:
                if tile.pos not in path:
                    stack.append((tile.pos, path + [tile.pos]))

        return Path([])


class BranchAndBoundAgent(Agent):

    def __init__(self):
        super().__init__("BranchAndBound")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:

        heap = []
        tie_breaker = random.random()
        heapq.heappush(heap, (0, 1, tie_breaker, start, [start]))

        best_cost_to = {start: 0}

        while heap:
            g, l, _, current, path = heapq.heappop(heap)

            if current == goal:
                return Path(path)

            r, c = current

            for tile in grid.neighbors4(r, c):
                neighbor = tile.pos

                if neighbor in path:
                    continue 

                new_g = g + tile.cost
                new_l = l + 1

                if neighbor not in best_cost_to or new_g < best_cost_to[neighbor]:
                    best_cost_to[neighbor] = new_g
                    tie_breaker = random.random()
                    heapq.heappush(
                        heap,
                        (new_g, new_l, tie_breaker, neighbor, path + [neighbor])
                    )

        return Path([])



class AStar(Agent):

    def __init__(self):
        super().__init__("AStar")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:

            heap = []
            tie_breaker = random.random()
            heapq.heappush(heap, (grid.manhattan(start, goal), 1, tie_breaker, 0, start, [start]))

            best_cost_to = {start: 0}

            while heap:
                f, l, _, g, current, path = heapq.heappop(heap)

                if current == goal:
                    return Path(path)

                r, c = current

                for tile in grid.neighbors4(r, c):
                    neighbor = tile.pos

                    if neighbor in path:
                        continue 

                    new_g = f + tile.cost + grid.manhattan(tile.pos, goal)
                    new_l = l + 1

                    if neighbor not in best_cost_to or new_g < best_cost_to[neighbor]:
                        best_cost_to[neighbor] = new_g
                        tie_breaker = random.random()
                        heapq.heappush(
                            heap,
                            (new_g, new_l, tie_breaker, f + tile.cost, neighbor, path + [neighbor])
                        )

            return Path([])


class BFSAgent(Agent):

    def __init__(self):
        super().__init__("BFS")
        
    def average_neighbor_cost(self, grid: Grid, node:tuple[int, int]):

        self.rows = len(grid.tiles)
        self.cols = len(grid.tiles[0])

        total_cost = 0.0
        count = 0

        if node.row - 1 >= 0:
            total_cost += grid.tiles[node.row - 1][node.col].cost
            count += 1

        if node.col + 1 < self.cols:
            total_cost += grid.tiles[node.row][node.col + 1].cost
            count += 1

        if node.row + 1 < self.rows:
            total_cost += grid.tiles[node.row + 1][node.col].cost
            count += 1

        if node.col - 1 >= 0:
            total_cost += grid.tiles[node.row][node.col - 1].cost
            count += 1

        if count == 0:
            return float('inf')

        return total_cost / count    
    
    


    def find_path(self, grid, start, goal):
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            (r, c), path = queue.popleft()

            if (r, c) == goal:
                return Path(path)

            for tile in grid.neighbors4(r, c):
                pos = tile.pos
                if pos not in visited:
                    visited.add(pos)
                    queue.append((pos, path + [pos]))

        return Path([])




class BestFirstSearchAgent(Agent):

    def __init__(self):
        super().__init__("BestFirstSearch")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
 
            heap = []
            tie_breaker = random.random()
            heapq.heappush(heap, (grid.manhattan(start, goal), 1, tie_breaker, start, [start]))

            while heap:
                g, l, _, current, path = heapq.heappop(heap)

                if current == goal:
                    return Path(path)

                r, c = current

                for tile in grid.neighbors4(r, c):
                    neighbor = tile.pos

                    if neighbor not in path:
                        new_g = grid.manhattan(tile.pos, goal)
                        new_l = l + 1
                        tie_breaker = random.random()
                        heapq.heappush(
                            heap,
                            (new_g, new_l, tie_breaker, neighbor, path + [neighbor])
                        )
                       

            return Path([])



AGENTS: dict[str, Callable[[], Agent]] = {
    "Example": ExampleAgent,
    "DFS": DFSAgent,
    "BranchAndBound": BranchAndBoundAgent,
    "AStar": AStar,
    "BFS": BFSAgent,
    "BestFirstSearch": BestFirstSearchAgent
}


def create_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise ValueError(f"Unknown agent '{name}'. Available: {', '.join(AGENTS.keys())}")
    return AGENTS[name]()
