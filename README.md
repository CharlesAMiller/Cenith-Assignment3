# Assignment 3 - Grid Game (Solver)

![Tests](https://github.com/CharlesAMiller/Cenith-Assignment3/actions/workflows/python-app.yml/badge.svg)

This is an attempt of Assignment 3 - which has to do with finding the optimal path that 
minimizes the amount of health lost and moves expended through a 100x100 grid. Grids
have a variety of possible tiles, and navigating through them can incur different health
and movement penalties. 

### Project Overview
```
.
├── docs                    # Sphinx autogen doc files 
├── samples                 # Directory containing example input grids and their associated outputs
│   ├── *.in                # Example grid files
│   ├── *.out               # The result of running the associated .in file through assignment.py 
├── tools                   # Tools and utilities
│   ├── grid_maker          # Helper script that can be used to automatically generate grids for grid_game
├── assignment.py           # The entry point of the application. It handles ui / ux centric behavior
├── grid_game.py            # The file that contains the logic of the game/simulation. It's probably what you're most after
├── README.md               # You are here
├── requirements.txt        # App dependencies (ONLY USED WHEN GENERATING DOCS)
├── tests.py                # Unit tests for our game logic 
└── utils.py                # Misc functions that are used in the project, but do not necessarily apply directly to the game logic
```


### Project Details
The project implements the [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) algorithm to 
find the optimal path that minimizes damage and moves. The selected heuristic is the [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry), considering that only movement in the cardinal directions is permitted. 
The cost of an edge is determined by taking the sum of the relative change of each metric (health or moves) that would be incurred by taking said edge.
The motivation behind this was to balance the two different priorities/resources. For example, if were down to our last 2 or 3 moves, but still had an abundance of health, navigating to a Speeder tile might be more advantageous than an empty space. This dynamic is demonstrated in the test: 'test_take_speeder_if_would_exhaust_moves' within `tests.py`

### What's Next? Misc Thoughts
I still think there could be more testing surrounding "Speeders". I think so long as there's an associated health cost with them, I don't think there's a problem with the algorithm. The fact they incur no movement penalty is what gives me some pause, because if we only made decisions off of that, we would run into a situation wherein the heuristic could 
be over estimating our distance - which can lead to non optimal paths being selected. [Note](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html).

As for bells and whistles, I could probably add back in a linter step to the Github Actions workflow.
Additionally, I could also add a step in the workflow to generate coverage stats.

## Usage
This was primarily tested on Python 3.11, though I think 3.9 or 3.10 ought to work too. 

```
python3 assignment.py [-h] [--strict] [-e HEALTH] [-m MOVES] <filename> 
```

### Example 
Included within `samples/` are a number of sample input files ending in `.in`.

```
python3 assignment.py samples/2x2.in
```

Each sample input file has a corresponding output (`*.out`) file that displays the
final health and moves statistics, followed by a depiction of the path taken. 

```
200 448

→↓
EB
```

## Testing
```
python3 -m unittest tests.py
```

Optionally, if you're using VSCode, a `settings.json` file has been included in `.vscode/` to automatically
identify the `tests.py` with the appropriate testing framework (unittest).


### Testing with coverage

1. Install the [coverage](https://coverage.readthedocs.io/en/7.2.3/) tool.


``` 
python3 -m pip install coverage 
```
2. Re-run the unittests, but with the coverage tool.

```
coverage run -m unittest tests.py
```

3. Optionally, you can now create coverage report HTML page

```
coverage html 
```

The command will then output the viewable HTML document to /htmlcov/index.html

## Docs
1. In order to build the docs, install the requirements contained within `requirements.txt` using `pip install -r requirements.txt` , ideally from within a new venv.

2. Run `spinx-build -b html docs/ docs/_build`

Now you can view the docs from `docs/_build/index.html`

## Tools

### Grid Maker
You can use the script `grid_maker.py` within the tools directory to generate grids of 100x100
with weighted distributions of tiles. All created grids ensure that the starting point always starts
on the left most columns of the grid and that the ending point is located on the far right column (per doc requirements).