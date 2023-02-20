import pygame
import random

# Constants
WIDTH = 512
HEIGHT = 400
CELL_SIZE = 5
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE
FPS = 120
SCALE_FACTOR = 0.25  # Used to scale up and down the cell size
BACKGROUND_TOP = (24, 18, 37)  # Dark color for top of the screen
BACKGROUND_BOTTOM = (33, 71, 97)  # Light color for bottom of the screen
CELL_COLORS = [(60, 173, 100), (52, 152, 219)]  # Colors for alive and dead cells

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background image
# background_image = pygame.image.load("background.png").convert()


def create_grid():
    """Create a new grid with random alive/dead cells."""
    return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]


def count_neighbors(grid, row, col):
    """Count the number of alive neighbors around a cell."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if row + i < 0 or row + i >= ROWS or col + j < 0 or col + j >= COLS:
                continue
            count += grid[row + i][col + j]
    return count


def get_cell_color(row):
    """Get the color for a cell based on the row number."""
    top_color = (60, 173, 100)  # Color for top of the wave
    bottom_color = (52, 152, 219)  # Color for bottom of the wave
    alpha = min(255, max(0, int(255 * (row / ROWS))))  # Opacity based on the row number
    color = (
        int((top_color[0] * alpha + bottom_color[0] * (255 - alpha)) / 255),
        int((top_color[1] * alpha + bottom_color[1] * (255 - alpha)) / 255),
        int((top_color[2] * alpha + bottom_color[2] * (255 - alpha)) / 255),
    )
    return color


def update_grid(grid):
    """Update the grid based on the rules of Conway's Game of Life."""
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = count_neighbors(grid, row, col)
            if grid[row][col] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row][col] = 0
            elif grid[row][col] == 0 and neighbors == 3:
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = grid[row][col]
    return new_grid


def draw_color_scheme(grid, scale_factor, last_grid):
    """Draw the grid on the screen as 3D cubes with a color gradient and a pulsating effect."""
    # Draw the background color gradient
    for y in range(HEIGHT):
        color = interpolate_colors(BACKGROUND_TOP, BACKGROUND_BOTTOM, y / HEIGHT)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # Draw the cells as 3D cubes with the wave pattern and pulsating effect
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != last_grid[row][col]:
                if grid[row][col] == 1:
                    color = get_cell_color(row)
                    size = int(CELL_SIZE + CELL_SIZE * scale_factor)
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE

                    # Draw the front face
                    pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

                    # Draw the back face
                    pygame.draw.rect(
                        screen,
                        interpolate_colors(color, (0, 0, 0), 0.5),
                        (x, y, CELL_SIZE, CELL_SIZE),
                        2,
                    )

                    # Draw the left face
                    pygame.draw.polygon(
                        screen,
                        interpolate_colors(color, (0, 0, 0), 0.2),
                        [
                            (x, y),
                            (x + CELL_SIZE // 2, y - CELL_SIZE // 2),
                            (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                            (x, y + CELL_SIZE),
                        ],
                        2,
                    )

                    # Draw the right face
                    pygame.draw.polygon(
                        screen,
                        interpolate_colors(color, (0, 0, 0), 0.2),
                        [
                            (x + CELL_SIZE, y),
                            (x + CELL_SIZE // 2, y - CELL_SIZE // 2),
                            (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                            (x + CELL_SIZE, y + CELL_SIZE),
                        ],
                        2,
                    )

                    # Draw the top face
                    pygame.draw.polygon(
                        screen,
                        interpolate_colors(color, (255, 255, 255), 0.5),
                        [
                            (x, y),
                            (x + CELL_SIZE, y),
                            (x + CELL_SIZE // 2, y - CELL_SIZE // 2),
                        ],
                        2,
                    )

                    # Draw the bottom face
                    pygame.draw.polygon(
                        screen,
                        interpolate_colors(color, (0, 0, 0), 0.5),
                        [
                            (x, y + CELL_SIZE),
                            (x + CELL_SIZE, y + CELL_SIZE),
                            (x + CELL_SIZE // 2, y + CELL_SIZE + CELL_SIZE // 2),
                        ],
                        2,
                    )

    pygame.display.update()


def interpolate_colors(color1, color2, t):
    """Interpolate between two colors."""
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    return (r, g, b)


def create_glider(grid, row, col):
    """Create a glider pattern at the specified row and column."""
    glider = [[0, 0, 1], [1, 0, 1], [0, 1, 1]]
    for i in range(3):
        for j in range(3):
            grid[row + i][col + j] = glider[i][j]
    return grid


def main():
    """Run the game."""
    grid = create_grid()
    last_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    running = True
    scale_factor = 0
    scale_direction = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid = create_grid()
                elif event.key == pygame.K_g:
                    row = random.randint(0, ROWS - 3)
                    col = random.randint(0, COLS - 3)
                    grid = create_glider(grid, row, col)
        last_grid = grid
        grid = update_grid(grid)
        draw_color_scheme(grid, scale_factor, last_grid)
        # Update the scale factor for the pulsating effect
        scale_factor += 0.025 * scale_direction
        if scale_factor > SCALE_FACTOR or scale_factor < 0:
            scale_direction *= -1
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()