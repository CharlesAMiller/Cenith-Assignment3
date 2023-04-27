""" Assignment 3 - Grid Game (Solver) 
This is the entry point of the program, and is responsible for:
    * Handling command line arguments
    * Calling path finding behavior
    * Outputting results
"""
import argparse

from grid_game import DEFAULT_DIM, DEFAULT_HEALTH, DEFAULT_MOVES, find_path 
from utils import make_pretty_path, print_grid


def read_grid_from_file(file_path: str) -> list[list[str]]:
    """ Give a file path, load the contents of the file to a 2D grid. """
    grid = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            line = line.replace('\n', '')
            grid.append(list(line))
    return grid


def enforceDefaultRequirements(grid: list[list[str]], health: int, moves: int):
    """ Is used to determine if a given grid adheres to the requirements specified by the provided doc. """
    if len(grid) != DEFAULT_DIM or any(map(lambda row: len(row) != DEFAULT_DIM, grid)):
        raise Exception()
    if health != DEFAULT_HEALTH or moves != DEFAULT_MOVES:
        raise Exception()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Assignment 3 - Path Finding Game',
        description='Attempts to find the optimal path from point A to B - avoiding the hazards that plague the grid')

    parser.add_argument('filename')
    parser.add_argument('--strict', action="store_true",
                        help="If raised, only accept grids of 100x100 and default health/moves values (200, 450)")
    parser.add_argument('-e', '--health',
                        dest='health', default=DEFAULT_HEALTH, type=int)
    parser.add_argument('-m', '--moves',
                        dest='moves', default=DEFAULT_MOVES, type=int)
    args = parser.parse_args()

    grid = read_grid_from_file(args.filename)
    if args.strict is True:
        enforceDefaultRequirements(grid, args.health, args.moves)

    # Attempt to find optimal path and final results as a consequence of taking said path
    path, health_and_weight = find_path(grid, args.health, args.moves)

    # Output results
    if path is not None:
        print(health_and_weight[0], health_and_weight[1], end=('\n\n'))
        prety_path = make_pretty_path(grid, path)
        print_grid(prety_path)
