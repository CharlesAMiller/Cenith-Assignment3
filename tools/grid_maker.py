import argparse
import random

DEFAULT_DIM = 100

TILES = ['E', 'S', 'M', 'L']
DEFAULT_TILE_WEIGHTS = [65, 20, 10, 5] 

def generate_random_grid(dims, tile_probabilities=DEFAULT_TILE_WEIGHTS):
    rows, cols = dims
    start = random.randint(0, cols)
    end = random.randint(0, cols)

    grid = []
    for y in range(rows):
        row = '' 
        for x in range(cols):
            if x == 0 and y == start:
                row += 'A'
                continue
            elif x == cols - 1 and y == end:
                row += 'B'
                continue

            row += random.choices(TILES, tile_probabilities)[0]

        grid.append(row) 

    return grid

def write_grid(file_path, grid):
    with open(file_path, "w") as file:
        for i, row in enumerate(grid):
            file.write(row)
            if i < len(grid) - 1:
                file.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Assignment 3 - Grid Making Tool',
        description='Tool to generate random grids for our grid game')

    parser.add_argument('filename')
    parser.add_argument('-x', '--rows', 
                        dest='rows', default=DEFAULT_DIM, type=int)
    parser.add_argument('-y', '--cols', 
                        dest='cols', default=DEFAULT_DIM, type=int)

    args = parser.parse_args()

    grid = generate_random_grid((args.rows, args.cols))
    write_grid(args.filename, grid)
