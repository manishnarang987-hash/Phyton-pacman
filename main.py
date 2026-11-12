"""
Mini Pac-Man
A small maze game made with Python and Pygame.

Controls:
    Arrow keys / WASD : Move
    P                 : Pause / Resume
    R                 : Restart
    Enter / Space     : Start or play again
    Esc               : Quit
"""

import asyncio
import math
import random
from collections import deque

import pygame


# ----------------------------- GAME SETTINGS -----------------------------

TILE_SIZE = 32
HUD_HEIGHT = 70
FPS = 60

SCREEN_WIDTH = 19 * TILE_SIZE
SCREEN_HEIGHT = 15 * TILE_SIZE + HUD_HEIGHT

PLAYER_START = (1, 1)

MAZE = [
    "###################",
    "#.................#",
    "#.###...###...###.#",
    "#o...............o#",
    "#...###...###.....#",
    "#.................#",
    "#.###...###...###.#",
    "#.................#",
    "#.....#.....#.....#",
    "#.................#",
    "#.###...###...###.#",
    "#o...............o#",
    "#...###...###.....#",
    "#.................#",
    "###################",
]

# Directions are stored as (change in x, change in y).
DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
}

# Colours
BACKGROUND = (8, 12, 32)
WALL_BLUE = (35, 75, 190)
WALL_HIGHLIGHT = (75, 130, 255)
PACMAN_YELLOW = (255, 220, 45)
PELLET_COLOUR = (255, 235, 190)
POWER_COLOUR = (255, 255, 255)
WHITE = (245, 245, 255)
MUTED_TEXT = (170, 185, 220)
GHOST_BLUE = (255, 80, 90)
GHOST_PINK = (255, 120, 210)
GHOST_GREEN = (70, 220, 160)
GHOST_ORANGE = (255, 165, 65)
SCARED_BLUE = (55, 95, 255)


# ------------------------------- GHOST CLASS -----------------------------

class Ghost:
    """Stores the position, colour and movement speed of one ghost."""

    def __init__(self, x, y, colour, move_delay):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.colour = colour
        self.move_delay = move_delay
        self.move_timer = 0

    def reset(self):
        """Send the ghost back to its starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.move_timer = 0


# ------------------------------- GAME CLASS ------------------------------

class PacManGame:
    """Controls the maze, player, ghosts, score and game screens."""

    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("arial", 38, bold=True)
        self.large_font = pygame.font.SysFont("arial", 30, bold=True)
        self.font = pygame.font.SysFont("arial", 21, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)

        self.reset_game(start_screen=True)

    def reset_game(self, start_screen=False):
        """Start a fresh game and create all collectible dots."""
        self.player_x, self.player_y = PLAYER_START
        self.player_direction = (0, 0)
        self.queued_direction = (0, 0)
        self.player_move_timer = 0
        self.player_move_delay = 0.12

        self.ghosts = [
            Ghost(9, 7, GHOST_BLUE, 0.27),
            Ghost(9, 9, GHOST_PINK, 0.32),
            Ghost(17, 13, GHOST_GREEN, 0.36),
            Ghost(1, 13, GHOST_ORANGE, 0.40),
        ]

        self.pellets = set()
        self.power_pellets = set()

        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                if cell == ".":
                    self.pellets.add((x, y))
                elif cell == "o":
                    self.power_pellets.add((x, y))

        # The player should not have to collect a dot from the starting tile.
        self.pellets.discard(PLAYER_START)
        self.power_timer = 0
        self.score = 0
        self.lives = 3
        self.state = "menu" if start_screen else "playing"

    def reset_positions(self):
        """Reset positions after the player loses a life."""
        self.player_x, self.player_y = PLAYER_START
        self.player_direction = (0, 0)
        self.queued_direction = (0, 0)
        self.player_move_timer = 0
        self.power_timer = 0

        for ghost in self.ghosts:
            ghost.reset()

    def is_open(self, x, y):
        """Return True if a maze tile is not a wall."""
        if y < 0 or y >= len(MAZE):
            return False
        if x < 0 or x >= len(MAZE[y]):
            return False
        return MAZE[y][x] != "#"

    def get_neighbours(self, position):
        """Return all walkable tiles directly beside a position."""
        x, y = position
        neighbours = []

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_position = (x + dx, y + dy)
            if self.is_open(*next_position):
                neighbours.append(next_position)

        return neighbours

    def find_next_step(self, start, goal):
        """
        Find a short path through the maze using Breadth-First Search (BFS).
        The ghost only uses the first step of the path.
        """
        if start == goal:
            return start

        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            for neighbour in self.get_neighbours(current):
                if neighbour not in came_from:
                    came_from[neighbour] = current
                    queue.append(neighbour)

        if goal not in came_from:
            return start

        # Work backwards from the target until the first step is found.
        step = goal
        while came_from[step] != start:
            step = came_from[step]

        return step

    def move_player(self):
        """Move Pac-Man one tile in the current or queued direction."""
        next_x = self.player_x + self.queued_direction[0]
        next_y = self.player_y + self.queued_direction[1]

        # Turn as soon as the requested direction becomes available.
        if self.queued_direction != (0, 0) and self.is_open(next_x, next_y):
            self.player_direction = self.queued_direction

        dx, dy = self.player_direction
        next_x = self.player_x + dx
        next_y = self.player_y + dy

        if self.is_open(next_x, next_y):
            self.player_x = next_x
            self.player_y = next_y

        self.collect_items()

    def collect_items(self):
        """Add points when Pac-Man moves over dots or power pellets."""
        position = (self.player_x, self.player_y)

        if position in self.pellets:
            self.pellets.remove(position)
            self.score += 10

        if position in self.power_pellets:
            self.power_pellets.remove(position)
            self.score += 50
            self.power_timer = 8.0

        if not self.pellets and not self.power_pellets:
            self.state = "won"

    def move_ghost(self, ghost):
        """Move one ghost towards the player, or away while powered up."""
        ghost_position = (ghost.x, ghost.y)
        player_position = (self.player_x, self.player_y)
        neighbours = self.get_neighbours(ghost_position)

        if not neighbours:
            return

        if self.power_timer > 0:
            # When Pac-Man has a power pellet, ghosts try to move farther away.
            distances = [
                abs(x - self.player_x) + abs(y - self.player_y)
                for x, y in neighbours
            ]
            farthest_distance = max(distances)
            choices = [
                position for position, distance in zip(neighbours, distances)
                if distance == farthest_distance
            ]
            next_position = random.choice(choices)
        else:
            next_position = self.find_next_step(ghost_position, player_position)

        ghost.x, ghost.y = next_position

    def check_collisions(self):
        """Check whether a ghost has reached the player."""
        player_position = (self.player_x, self.player_y)

        for ghost in self.ghosts:
            if (ghost.x, ghost.y) == player_position:
                if self.power_timer > 0:
                    self.score += 200
                    ghost.reset()
                else:
                    self.lives -= 1

                    if self.lives <= 0:
                        self.state = "game_over"
                    else:
                        self.reset_positions()
                    return

    def update(self, delta_time):
        """Update movement and timers while the game is running."""
        if self.state != "playing":
            return

        if self.power_timer > 0:
            self.power_timer = max(0, self.power_timer - delta_time)

        self.player_move_timer += delta_time
        while self.player_move_timer >= self.player_move_delay:
            self.player_move_timer -= self.player_move_delay
            self.move_player()

        for ghost in self.ghosts:
            ghost.move_timer += delta_time

            while ghost.move_timer >= ghost.move_delay:
                ghost.move_timer -= ghost.move_delay
                self.move_ghost(ghost)

        self.check_collisions()

    # ------------------------------- DRAWING ------------------------------

    def draw_text(self, text, font, colour, x, y, centred=False):
        """Draw text at a position on the screen."""
        image = font.render(text, True, colour)
        rect = image.get_rect()

        if centred:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        self.screen.blit(image, rect)

    def draw_maze(self):
        """Draw walls, normal dots and power pellets."""
        for y, row in enumerate(MAZE):
            for x, cell in enumerate(row):
                screen_x = x * TILE_SIZE
                screen_y = HUD_HEIGHT + y * TILE_SIZE

                if cell == "#":
                    wall_rect = pygame.Rect(
                        screen_x + 2, screen_y + 2,
                        TILE_SIZE - 4, TILE_SIZE - 4
                    )
                    pygame.draw.rect(
                        self.screen, WALL_BLUE, wall_rect, border_radius=7
                    )
                    pygame.draw.rect(
                        self.screen, WALL_HIGHLIGHT, wall_rect,
                        width=1, border_radius=7
                    )

        for x, y in self.pellets:
            centre = (
                x * TILE_SIZE + TILE_SIZE // 2,
                HUD_HEIGHT + y * TILE_SIZE + TILE_SIZE // 2
            )
            pygame.draw.circle(self.screen, PELLET_COLOUR, centre, 3)

        # Make power pellets blink gently.
        pulse = 7 + int(2 * abs(math.sin(pygame.time.get_ticks() / 180)))

        for x, y in self.power_pellets:
            centre = (
                x * TILE_SIZE + TILE_SIZE // 2,
                HUD_HEIGHT + y * TILE_SIZE + TILE_SIZE // 2
            )
            pygame.draw.circle(self.screen, POWER_COLOUR, centre, pulse)

    def draw_player(self):
        """Draw Pac-Man as a yellow circle with a moving mouth."""
        centre_x = self.player_x * TILE_SIZE + TILE_SIZE // 2
        centre_y = HUD_HEIGHT + self.player_y * TILE_SIZE + TILE_SIZE // 2
        radius = 13

        pygame.draw.circle(
            self.screen, PACMAN_YELLOW, (centre_x, centre_y), radius
        )

        dx, dy = self.player_direction
        if (dx, dy) != (0, 0):
            angle = math.atan2(dy, dx)
            mouth_size = 0.38 + 0.12 * abs(
                math.sin(pygame.time.get_ticks() / 90)
            )

            point_one = (
                centre_x + radius * math.cos(angle - mouth_size),
                centre_y + radius * math.sin(angle - mouth_size)
            )
            point_two = (
                centre_x + radius * math.cos(angle + mouth_size),
                centre_y + radius * math.sin(angle + mouth_size)
            )

            pygame.draw.polygon(
                self.screen, BACKGROUND,
                [(centre_x, centre_y), point_one, point_two]
            )

    def draw_ghost(self, ghost):
        """Draw a simple ghost using circles and rectangles."""
        centre_x = ghost.x * TILE_SIZE + TILE_SIZE // 2
        centre_y = HUD_HEIGHT + ghost.y * TILE_SIZE + TILE_SIZE // 2

        colour = SCARED_BLUE if self.power_timer > 0 else ghost.colour

        # Head and body
        pygame.draw.circle(self.screen, colour, (centre_x, centre_y - 3), 12)
        body_rect = pygame.Rect(centre_x - 12, centre_y - 3, 24, 13)
        pygame.draw.rect(self.screen, colour, body_rect)

        # Small bumps make the bottom look like a ghost's tail.
        for offset in [-8, 0, 8]:
            pygame.draw.circle(
                self.screen, colour, (centre_x + offset, centre_y + 9), 4
            )

        # Eyes
        pygame.draw.circle(
            self.screen, WHITE, (centre_x - 5, centre_y - 4), 4
        )
        pygame.draw.circle(
            self.screen, WHITE, (centre_x + 5, centre_y - 4), 4
        )
        pygame.draw.circle(
            self.screen, (20, 35, 90), (centre_x - 4, centre_y - 4), 2
        )
        pygame.draw.circle(
            self.screen, (20, 35, 90), (centre_x + 6, centre_y - 4), 2
        )

    def draw_hud(self):
        """Draw the score, lives and game title above the maze."""
        self.draw_text("MINI PAC-MAN", self.font, PACMAN_YELLOW, 14, 22)
        self.draw_text(
            f"SCORE: {self.score}", self.small_font, WHITE, 250, 26
        )
        self.draw_text(
            f"LIVES: {self.lives}", self.small_font, WHITE, 465, 26
        )

    def draw_overlay(self, title, subtitle):
        """Draw a dark transparent panel over the game."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - HUD_HEIGHT))
        overlay.set_alpha(210)
        overlay.fill(BACKGROUND)
        self.screen.blit(overlay, (0, HUD_HEIGHT))

        centre_x = SCREEN_WIDTH // 2
        centre_y = HUD_HEIGHT + (SCREEN_HEIGHT - HUD_HEIGHT) // 2

        self.draw_text(
            title, self.title_font, PACMAN_YELLOW,
            centre_x, centre_y - 42, centred=True
        )
        self.draw_text(
            subtitle, self.font, WHITE,
            centre_x, centre_y + 8, centred=True
        )

    def draw(self):
        """Draw the complete game screen."""
        self.screen.fill(BACKGROUND)
        self.draw_hud()
        self.draw_maze()
        self.draw_player()

        for ghost in self.ghosts:
            self.draw_ghost(ghost)

        if self.state == "menu":
            self.draw_overlay(
                "MINI PAC-MAN",
                "Press SPACE or ENTER to start"
            )
            self.draw_text(
                "Collect every dot. Avoid the ghosts!",
                self.small_font, MUTED_TEXT,
                SCREEN_WIDTH // 2, SCREEN_HEIGHT - 65, centred=True
            )

        elif self.state == "paused":
            self.draw_overlay("PAUSED", "Press P to continue")

        elif self.state == "game_over":
            self.draw_overlay(
                "GAME OVER",
                f"Final score: {self.score}   |   Press SPACE to retry"
            )

        elif self.state == "won":
            self.draw_overlay(
                "YOU WIN!",
                f"Final score: {self.score}   |   Press SPACE to play again"
            )


# --------------------------------- MAIN -----------------------------------

async def main():
    """Run the game loop."""
    pygame.init()
    pygame.display.set_caption("Mini Pac-Man - Python BCA Project")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = PacManGame(screen)

    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key in DIRECTIONS and game.state == "playing":
                    game.queued_direction = DIRECTIONS[event.key]

                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if game.state in ("menu", "game_over", "won"):
                        game.reset_game()
                    elif game.state == "paused":
                        game.state = "playing"

                elif event.key == pygame.K_p:
                    if game.state == "playing":
                        game.state = "paused"
                    elif game.state == "paused":
                        game.state = "playing"

                elif event.key == pygame.K_r:
                    game.reset_game()

        game.update(delta_time)
        game.draw()
        pygame.display.flip()

        # This lets the game loop work with browser packaging tools too.
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
