# Mini Pac-Man - Project Report

## 1. Project Title

**Mini Pac-Man: A Maze Game Using Python and Pygame**

## 2. Introduction

Mini Pac-Man is a simple maze-based game developed using the Python programming language and the Pygame library. The player controls a character inside a maze, collects dots, avoids ghosts, and tries to complete the maze while keeping their lives.

The project is intended to demonstrate basic programming and game-development concepts in a small, understandable application.

## 3. Objectives

- To understand how a game loop works.
- To use keyboard events to control a character.
- To draw shapes and text using Pygame.
- To use classes and objects to organise game elements.
- To implement score and life systems.
- To practise basic collision detection.
- To understand a simple pathfinding technique.

## 4. Software and Hardware Requirements

**Software**
- Python 3.9 or newer
- Pygame
- Any code editor, such as VS Code
- Windows, macOS, or Linux

**Hardware**
- A computer capable of running Python and Pygame
- Keyboard for game controls

## 5. Modules / Main Components

### Player movement
The player moves one maze tile at a time. Arrow keys or WASD keys are used to choose a direction. The game checks that the next tile is not a wall before moving.

### Maze and collectibles
The maze is stored as a list of strings. The `#` character represents a wall, `.` represents a normal dot, and `o` represents a power pellet.

### Ghost movement
Each ghost has a starting position, colour, and movement speed. Ghosts use Breadth-First Search (BFS) to find a path towards the player.

### Score and lives
Collecting a normal dot adds 10 points. A power pellet adds 50 points. Eating a ghost while powered up adds 200 points. The player starts with three lives.

### Game screens
The project includes a start screen, pause screen, win screen, and game-over screen.

## 6. Algorithm

1. Start the game and initialise the maze, player, ghosts, score, and lives.
2. Display the game window.
3. Read keyboard events.
4. Move the player when the next tile is open.
5. Check whether the player collected a dot or power pellet.
6. Move ghosts towards the player using BFS.
7. Check for collisions between the player and ghosts.
8. Update score, lives, and power-pellet time.
9. Display the win screen when all collectibles are collected.
10. Repeat until the player quits or the game ends.

## 7. Testing

| Test | Expected result |
|---|---|
| Press an arrow key or WASD | Player moves in that direction when the path is open |
| Move into a wall | Player does not pass through the wall |
| Collect a normal dot | Score increases by 10 |
| Collect a power pellet | Score increases by 50 and ghosts become vulnerable |
| Touch a ghost without power | Player loses one life |
| Touch a ghost with power | Ghost returns to its starting position and score increases |
| Press P | Game pauses or resumes |
| Press R | Game restarts |
| Collect every item | Win screen appears |

## 8. Conclusion

This project demonstrates how Python and Pygame can be used to create a small interactive game. It combines programming fundamentals, object-oriented programming, event handling, collision detection, and a basic pathfinding algorithm.

## 9. Future Scope

- Add multiple maze levels.
- Add sound effects and background music.
- Add a high-score saving system.
- Improve ghost behaviour with different difficulty levels.
- Add a settings screen and more visual effects.

## 10. Student Details

Fill in these details before submitting or sharing the report:

- **Student Name:** [Your Name]
- **Course:** Bachelor of Computer Applications (BCA)
- **Year:** Second Year
- **College:** [College Name]
- **Subject / Guide:** [Add if required]
