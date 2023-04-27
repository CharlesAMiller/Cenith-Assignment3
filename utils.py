def add_tuples(tup1: tuple[int, int], tup2: tuple[int, int]) -> tuple[int, int]:
    """ Returns a tuple whose ith elements is the sum of the given tuples ith elements """
    return tuple(map(lambda x, y: x + y, tup1, tup2))


def manhattan_dist(tup1: tuple[int, int], tup2: tuple[int, int]) -> int:
    """Given two coordinates, calculate the sum of the x and y distance between them"""
    return abs(tup1[0] - tup2[0]) + abs(tup1[1] - tup2[1])


def print_grid(grid: list[list[str]]):
    """Helper that prints contents of the grid by row then column"""
    for row in grid:
        for tile in row:
            print(tile, end='')
        print()


def make_pretty_path(grid: list[list[str]], path: list[tuple[int, int]]) -> list[list[str]]:
    """Given a grid and a path through it, return a grid depicting said path with nice arrow characters"""
    grid_path = grid.copy()
    if len(path) < 2:
        return grid

    direction = ''
    for i, loc in enumerate(path, 0):
        if i == len(path) - 1:
            break

        nxt = path[i + 1]

        if nxt[0] > loc[0]:
            direction = '↓'
        elif nxt[0] < loc[0]:
            direction = '↑'
        elif nxt[1] > loc[1]:
            direction = '→'
        else:
            direction = '←'
        grid_path[loc[0]][loc[1]] = direction

    return grid_path
