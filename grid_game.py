""" Grid Game
This script contains the logic for finding the optimal path through our grid game.
"""
import heapq
import math

from utils import add_tuples, manhattan_dist


class InvalidGridException(Exception):
    "Invalid grid - grid must have starting place (A) and goal (B)"
    pass


"""The cost (health, moves) associated to navigating to a special tile"""
COSTS = {'S': (-5, 0),
         'L': (-50, -10),
         'M': (-10, -5)
         }

"""The directions in which the 'player' can move - only cardinal"""
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

DEFAULT_DIM = 100
DEFAULT_HEALTH = 200
DEFAULT_MOVES = 450


def determine_start_and_goal(grid: list[list[str]]) -> tuple[tuple[int, int]]:
    """Locates the positions of the starting ('A') and ending characters ('B')"""
    start = end = None
    for x, row in enumerate(grid):
        for y, tile in enumerate(row):
            if tile == 'A':
                start = (x, y)
            elif tile == 'B':
                end = (x, y)

    return start, end


def is_in_bounds(loc: tuple[int, int], grid: list[list[str]]) -> bool:
    """Determines if the given coords of loc are within the dimensions of the given grid"""
    if loc[0] < 0 or loc[0] >= len(grid) or loc[1] < 0 or loc[1] >= len(grid[loc[0]]):
        return False
    return True


def get_cost(grid, loc):
    """Identify the type of tile at the given location and return its associated cost"""
    tile = grid[loc[0]][loc[1]]
    # By default, we assume that any non special tile is empty
    return COSTS[tile] if tile in COSTS else (0, -1)


def invert_path(came_from, end):
    """Inverts the steps in the given came_from list to return the actual path taken"""
    inverted_path = []
    loc = end

    while loc in came_from:
        inverted_path.insert(0, loc)
        loc = came_from[loc]
    inverted_path.insert(0, loc)

    return inverted_path


def calculate_relative_cost(stats, would_be_stats):
    """
    would_be_stats is what our health and moves would look like if we navigated to a particular tile.
    Because both health and moves have separate totals that can be depleted, we can never purely make decisions that 
    optimize for one or the other. Therefore, we find what percentage of each stat would be expended and scale them.
    We then take summation of these scaled values.

    Parameters
    ------------
        stats: 
            The current health and moves values
        would_be_stats: 
            What health and moves will be, if we navigate to a particular tile
    """
    health_relative_cost = math.floor(
        (1 - (would_be_stats[0] / max(1, stats[0]))) * 100)
    moves_relative_cost = math.floor(
        (1 - (would_be_stats[1] / max(1, stats[1]))) * 100)
    return (health_relative_cost + moves_relative_cost)


def find_path(grid, health=DEFAULT_HEALTH, moves=DEFAULT_MOVES) -> tuple[list[tuple[int, int]], tuple[int, int]] | None:
    """
    A* implementation that tries to minimize the loss of our health and moves.

    The heapq module and its methods are used to ensure that the most promising (i.e. the one with the lowest f-score) tile
    is always explored first. 

    Parameters
    ------------
        health: int
            The initial health, prior to beginning pathfinding
        moves: int
            The initial number of moves, prior to beginning pathfinding
    Return
    -----------
        best_path: 
            The list of coordinates in order from A to B, that represent the optimal path.
        final_stats: 
            A tuple of the final health and moves, as a consequence of taking the returned 'best_path'

    """
    start, end = determine_start_and_goal(grid)

    if start is None or end is None:
        raise InvalidGridException

    came_from = {}
    queue = [(0, start, (health, moves))]
    g_scores = {start: 0}

    while queue:
        _, loc, stats = heapq.heappop(queue)

        # The end has been reached and the optimal path is returned, along with final stats
        if loc == end:
            return invert_path(came_from, loc), stats

        for dir in DIRS:
            neighbor_loc = add_tuples(loc, dir)
            if not is_in_bounds(neighbor_loc, grid):
                continue

            neighbor_stats = get_cost(grid, neighbor_loc)
            n_health, n_moves = add_tuples(stats, neighbor_stats)

            # Navigating to the neighbor from the current path would result in failure. Therefore don't consider.
            if n_health <= 0 or n_moves < 0:
                continue

            cur_neighbor_g_score = g_scores[loc] + \
                calculate_relative_cost(stats, (n_health, n_moves))

            if neighbor_loc not in g_scores or cur_neighbor_g_score < g_scores[neighbor_loc]:
                came_from[neighbor_loc] = loc
                g_scores[neighbor_loc] = cur_neighbor_g_score
                if neighbor_loc not in queue:
                    f_score = cur_neighbor_g_score + \
                        manhattan_dist(loc, neighbor_loc)
                    heapq.heappush(
                        queue, (f_score, neighbor_loc, (n_health, n_moves)))

    # No valid path available
    return None
