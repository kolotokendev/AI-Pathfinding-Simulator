# AI-Pathfinding-Simulator
This project is a Python-based graphical simulation that demonstrates the application of fundamental search algorithms in a grid-based environment. The goal is to navigate an agent from a starting point to a target goal while accounting for different terrain types and path costs.

# Implemented Algorithms
The core of this project is the implementation of various search strategies to find the most efficient path:

- Breadth-First Search (BFS): Explores all nodes at the current depth before moving to the next level, guaranteeing the shortest path in terms of the number of steps.
- Depth-First Search (DFS): Explores as far as possible along each branch before backtracking.
- Best-First Search: An informed search algorithm that uses a heuristic to decide which adjacent node is most promising.
- A* Search: A heuristic-based search that finds the least-cost path by combining the cost to reach a node and the estimated cost to reach the goal.
- Branch and Bound (B&B): Systematically explores branches to find the optimal solution by pruning paths that exceed the current best cost.
