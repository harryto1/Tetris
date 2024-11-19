import pygame, sys, random, time

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 401, 900
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
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)



#Functions
def draw_grid():
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, WHITE, (i, 100), (i, HEIGHT))
    for i in range(100, HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (0, i), (WIDTH, i))

def get_name(shape):
    for key, value in shapes.items():
        if value == shape:
            return key

def choose_color(shape):
    for key, value in shapes.items():
        if shape == value:
            if key == 'I':
                return CYAN
            if key == 'J':
                return BLUE
            if key == 'L':
                return ORANGE
            if key == 'O':
                return YELLOW
            if key == 'S':
                return GREEN
            if key == 'T':
                return PURPLE
            if key == 'Z':
                return RED


def place_blocks(placed_blocks):
    for block in placed_blocks:
        for rect in block.shape:
            pygame.draw.rect(screen, block.color, rect)

def check_collision(current_block):
    for rect in current_block.shape:
        if rect.y >= HEIGHT:
            return True
        for block in placed_blocks:
            if any(rect.colliderect(placed_rect) for placed_rect in block.shape):
                return True
    return False

def remove_line():
    for y in range(HEIGHT - 40, 0, -40):
        count = 0
        blocks_to_remove = []
        for block in placed_blocks:
            for rect in block.shape:
                if rect.y == y:
                    count += 1
                    blocks_to_remove.append(rect)
        if count == 10:
            for block in blocks_to_remove:
                for i in range(len(placed_blocks)):
                    if block in placed_blocks[i].shape:
                        placed_blocks[i].shape.remove(block)
            for block in placed_blocks:
                for rect in block.shape:
                    if rect.y < y:
                        rect.y += 40
            global score, speed
            score += 10
            speed /= 1.1
            break

def draw_stored_block():
    global stored_block
    if stored_block is not None:
        if stored_block == 'I' or stored_block == 'J' or stored_block == 'L':
            shape_rect = rotated_shapes[stored_block][0].unionall(rotated_shapes[stored_block][1:])
        else:
            shape_rect = shapes[stored_block][0].unionall(shapes[stored_block][1:])
        pygame.draw.rect(screen, BLACK, shape_rect.inflate(10, 10).move(240, -90))
        if stored_block == 'I' or stored_block == 'J' or stored_block == 'L':
            for rect in rotated_shapes[stored_block]:
                pygame.draw.rect(screen, choose_color(shapes[stored_block]), rect.move(240, -90))
        else:
            for rect in shapes[stored_block]:
                pygame.draw.rect(screen, choose_color(shapes[stored_block]), rect.move(240, -90))

def check_lose():
    for block in placed_blocks:
        for rect in block.shape:
            if rect.y <= 100:
                return True
    return False

# Set up the fonts
font = pygame.font.Font('freesansbold.ttf', 32)

# Define all Tetris shapes
shapes = {
    'I': [pygame.Rect(0, 100, 38, 38), pygame.Rect(0, 140, 38, 38), pygame.Rect(0, 180, 38, 38),
          pygame.Rect(0, 220, 38, 38)],
    'J': [pygame.Rect(0, 100, 38, 38), pygame.Rect(0, 140, 38, 38), pygame.Rect(0, 180, 38, 38),
          pygame.Rect(40, 180, 38, 38)],
    'L': [pygame.Rect(40, 100, 38, 38), pygame.Rect(40, 140, 38, 38), pygame.Rect(40, 180, 38, 38),
          pygame.Rect(0, 180, 38, 38)],
    'O': [pygame.Rect(0, 100, 38, 38), pygame.Rect(40, 100, 38, 38), pygame.Rect(0, 140, 38, 38),
          pygame.Rect(40, 140, 38, 38)],
    'S': [pygame.Rect(0, 140, 38, 38), pygame.Rect(40, 140, 38, 38), pygame.Rect(40, 100, 38, 38),
          pygame.Rect(80, 100, 38, 38)],
    'T': [pygame.Rect(0, 100, 38, 38), pygame.Rect(40, 100, 38, 38), pygame.Rect(80, 100, 38, 38),
          pygame.Rect(40, 140, 38, 38)],
    'Z': [pygame.Rect(0, 100, 38, 38), pygame.Rect(40, 100, 38, 38), pygame.Rect(40, 140, 38, 38),
          pygame.Rect(80, 140, 38, 38)]
}

rotated_shapes = {
    'I': [pygame.Rect(0, 100, 38, 38), pygame.Rect(40, 100, 38, 38), pygame.Rect(80, 100, 38, 38), pygame.Rect(120, 100, 38, 38)],
    'J': [pygame.Rect(0, 100, 38, 38), pygame.Rect(40, 100, 38, 38), pygame.Rect(80, 100, 38, 38), pygame.Rect(80, 140, 38, 38)],
    'L': [pygame.Rect(0, 100, 38, 38), pygame.Rect(40, 100, 38, 38), pygame.Rect(80, 100, 38, 38), pygame.Rect(0, 140, 38, 38)]
}

placed_blocks = []

block_colors = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]


class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.name = get_name(shape)
        self.spawned = False
        self.color = choose_color(shape)
        self.already_stored = False

    def __str__(self):
        return f'Block at {self.x}, {self.y}'

    def draw(self):
        for i in range(len(self.shape)):
            pygame.draw.rect(screen, self.color, self.shape[i])

    def fall(self):
        for i in range(len(self.shape)):
            self.shape[i].y += 40

    def move(self, direction):
        for i in range(len(self.shape)):
            self.shape[i].x += direction
        for i in range(len(self.shape)):
            if self.shape[i].x < 0 or self.shape[i].x >= 400:
                for j in range(len(self.shape)):
                    self.shape[j].x -= direction
                return

        for block in placed_blocks:
            for rect in block.shape:
                for i in range(len(self.shape)):
                    if self.shape[i].colliderect(rect):
                        for j in range(len(self.shape)):
                            self.shape[j].x -= direction
                        return

    def set_spawned(self, value):
        self.spawned = value


    def rotate(self):
        pivot = self.shape[1]  # Use the second block as the pivot
        for rect in self.shape:
            # Translate block to origin
            x = rect.x - pivot.x
            y = rect.y - pivot.y
            # Rotate 90 degrees clockwise
            rect.x = pivot.x - y
            rect.y = pivot.y + x
            # Check boundaries
            if rect.x < 0 or rect.x >= WIDTH or rect.y < 0 or rect.y >= HEIGHT:
                return  # Invalid rotation, do nothing
            # Check collision with placed blocks
            for block in placed_blocks:
                if any(rect.colliderect(placed_rect) for placed_rect in block.shape):
                    return  # Invalid rotation, do nothing


current_block = Block(0, 100, [pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                             for rect in random.choice(list(shapes.values()))],)


speed = 1
stored_block = None
initial_time = time.time()


# Score
score = 0

running = True
while running:
    screen.fill(BLACK)


    if not current_block.spawned:
        current_block = Block(0, 100, [pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                                     for rect in random.choice(list(shapes.values()))])
        current_block.set_spawned(True)

    score_text = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(75, 50))
    screen.blit(score_text, score_rect)
    draw_grid()
    current_block.draw()
    remove_line()
    place_blocks(placed_blocks)
    draw_stored_block()
    if check_lose():
        screen.fill(BLACK)
        text = font.render('You Lose!', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block.move(-40)
            if event.key == pygame.K_RIGHT:
                current_block.move(40)
            if event.key == pygame.K_DOWN:
                current_block.fall()
                if check_collision(current_block):
                    for i in range(len(current_block.shape)):
                        current_block.shape[i].y -= 40
                    current_block.set_spawned(False)
                    placed_blocks.append(current_block)
                    current_block = Block(0, 100, [pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                                                 for rect in random.choice(list(shapes.values()))])
            if event.key == pygame.K_z or event.key == pygame.K_UP:
                if current_block.name == 'O':
                    break
                current_block.rotate()
            if event.key == pygame.K_SPACE:
                while not check_collision(current_block):
                    current_block.fall()
                for i in range(len(current_block.shape)):
                    current_block.shape[i].y -= 40
                current_block.set_spawned(False)
                placed_blocks.append(current_block)
                current_block = Block(0, 0, [pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                                             for rect in random.choice(list(shapes.values()))])
            if event.key == pygame.K_c:
                if current_block.already_stored:
                    break
                if stored_block is None:
                    stored_block = current_block.name
                    current_block.shape = [pygame.Rect(rect.x, rect.y, rect.width, rect.height) for rect in random.choice(list(shapes.values()))]
                    current_block.name = get_name(current_block.shape)
                    current_block.color = choose_color(current_block.shape)
                else:
                    temp = current_block.name
                    current_block.shape = [pygame.Rect(rect.x, rect.y, rect.width, rect.height) for rect in shapes[stored_block]]
                    current_block.name = stored_block
                    current_block.color = choose_color(current_block.shape)
                    stored_block = temp
                current_block.already_stored = True


    if check_collision(current_block):
        current_block.set_spawned(False)
        placed_blocks.append(current_block)
        current_block = Block(0, 0, [pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                                     for rect in random.choice(list(shapes.values()))])

    if time.time() - initial_time > speed:
        current_block.fall()
        if check_collision(current_block):
            for i in range(len(current_block.shape)):
                current_block.shape[i].y -= 40
            current_block.set_spawned(False)
            placed_blocks.append(current_block)
            current_block = Block(0, 0, [pygame.Rect(rect.x, rect.y, rect.width, rect.height)
                                         for rect in random.choice(list(shapes.values()))])
        initial_time = time.time()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()