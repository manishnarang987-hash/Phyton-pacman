# Mini Pac-Man (Python + Pygame)

A small Pac-Man-inspired maze game built with Python and Pygame. This is a student-level project suitable for demonstrating basic Python programming, object-oriented programming, game loops, collision detection, and a simple pathfinding algorithm.

## Features

- Maze with walls, dots, and power pellets
- Player movement using arrow keys or WASD
- Four ghosts that follow the player through the maze
- Breadth-First Search (BFS) for ghost pathfinding
- Power pellets that let the player eat ghosts temporarily
- Score, lives, pause, restart, win, and game-over screens
- Graphics are drawn with Pygame shapes, so no external image files are required

## Requirements

- Python 3.9 or newer
- Pygame

## Run the game

1. Download or clone this project.
2. Open a terminal in the project folder.
3. Install the required package:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the game:

   ```bash
   python main.py
   ```

## Controls

| Key | Action |
|---|---|
| Arrow keys / WASD | Move |
| P | Pause or resume |
| R | Restart |
| Space / Enter | Start or play again |
| Esc | Quit |

## Project structure

```text
mini_pacman_bca/
├── main.py
├── requirements.txt
├── PROJECT_REPORT.md
├── README.md
└── .gitignore
```

## Main Python concepts used

- Variables, conditions, loops, and functions
- Lists, tuples, sets, and dictionaries
- Classes and objects
- Pygame event handling and drawing
- Collision detection
- Breadth-First Search (BFS) using a queue

## Upload it to GitHub

1. Create a free account at [GitHub](https://github.com/) if you do not already have one.
2. Create a new **public** repository named `mini-pacman-python`.
3. Upload `main.py`, `requirements.txt`, `README.md`, `PROJECT_REPORT.md`, and `.gitignore`.
4. Add a short repository description, for example:

   `A Pac-Man-inspired maze game developed using Python and Pygame as a BCA mini project.`

5. Share the repository link with your company.

GitHub will show the source code and project documentation. It does not automatically run a Pygame desktop game in the browser, so a reviewer can clone the repository and run it using the instructions above.

## Before showing it to a company

- Run the game yourself and test every control.
- Be ready to explain how the player moves, how dots are collected, how lives work, and how BFS helps ghosts find the player.
- Add your own name, course, college, and screenshots to the project report if your college or company requires them.
- Do not claim features or programming knowledge you cannot explain.
