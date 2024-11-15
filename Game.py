import pygame, sys, random, time

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
screen.fill((255, 255, 255))
pygame.display.flip()

# Set up the clock
clock = pygame.time.Clock()

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)



#Functions
def draw_grid():
    for i in range(0, WIDTH, 80):
        pygame.draw.line(screen, WHITE, (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT, 80):
        pygame.draw.line(screen, WHITE, (0, i), (WIDTH, i))


def place_blocks(placed_blocks):
    for i in range(len(placed_blocks)):
        pygame.draw.rect(screen, BLUE, placed_blocks[i])

def check_collision(current_block):
    for i in range(len(current_block.shape)):
        if current_block.shape[i].y >= 720:
            return True
        for j in range(len(placed_blocks)):
            if current_block.shape[i].x == placed_blocks[j].x and current_block.shape[i].y + 80 == placed_blocks[j].y:
                return True
    return False

# Set up the fonts
font = pygame.font.Font('freesansbold.ttf', 32)

# Define all Tetris shapes
shapes = {
    'I': [pygame.Rect(0, 0, 80, 80), pygame.Rect(0, 80, 80, 80), pygame.Rect(0, 160, 80, 80), pygame.Rect(0, 240, 80, 80)],
    'J': [pygame.Rect(0, 0, 80, 80), pygame.Rect(0, 80, 80, 80), pygame.Rect(0, 160, 80, 80), pygame.Rect(80, 160, 80, 80)],
    'L': [pygame.Rect(0, 0, 80, 80), pygame.Rect(0, 80, 80, 80), pygame.Rect(0, 160, 80, 80), pygame.Rect(-80, 160, 80, 80)],
    'O': [pygame.Rect(0, 0, 80, 80), pygame.Rect(80, 0, 80, 80), pygame.Rect(0, 80, 80, 80), pygame.Rect(80, 80, 80, 80)],
    'S': [pygame.Rect(0, 80, 80, 80), pygame.Rect(80, 80, 80, 80), pygame.Rect(80, 0, 80, 80), pygame.Rect(160, 0, 80, 80)],
    'T': [pygame.Rect(0, 0, 80, 80), pygame.Rect(80, 0, 80, 80), pygame.Rect(160, 0, 80, 80), pygame.Rect(80, 80, 80, 80)],
    'Z': [pygame.Rect(0, 0, 80, 80), pygame.Rect(80, 0, 80, 80), pygame.Rect(80, 80, 80, 80), pygame.Rect(160, 80, 80, 80)]
}

placed_blocks = []

block_colors = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]


class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.spawned = False
        self.color = random.choice(block_colors)

    def draw(self):
        for i in range(len(self.shape)):
            pygame.draw.rect(screen, self.color, self.shape[i])

    def fall(self):
        for i in range(len(self.shape)):
            self.shape[i].y += 80

    def move(self, direction):
        for i in range(len(self.shape)):
            self.shape[i].x += direction
        for i in range(len(self.shape)):
            if self.shape[i].x < 0 or self.shape[i].x >= 800:
                for j in range(len(self.shape)):
                    self.shape[j].x -= direction
                return
            for j in range(len(placed_blocks)):
                if self.shape[i].x == placed_blocks[j].x and self.shape[i].y == placed_blocks[j].y:
                    for k in range(len(self.shape)):
                        self.shape[k].x -= direction
                    return

    def set_spawned(self, value):
        self.spawned = value


current_block = Block(0, 0, random.choice(list(shapes.values())))


speed_x = 80
speed_y = 80
initial_time = time.time()


# Score
score = 0

running = True
while running:
    screen.fill(BLACK)

    if not current_block.spawned:
        current_block = Block(0, 0, random.choice(list(shapes.values())))
        current_block.set_spawned(True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block.move(-80)
            if event.key == pygame.K_RIGHT:
                current_block.move(80)
            if event.key == pygame.K_DOWN:
                current_block.fall()
    if time.time() - initial_time > 1:
        current_block.fall()
        initial_time = time.time()

    if check_collision(current_block):
        current_block.set_spawned(False)
        placed_blocks.extend(current_block.shape)
        current_block = Block(0, 0, random.choice(list(shapes.values())))

    draw_grid()
    place_blocks(placed_blocks)
    current_block.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()