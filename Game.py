import pygame, sys, random, time

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('./assets/music/tetris_theme.mp3') # Change these when compiling using pyinstaller
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
remove_line_music = pygame.mixer.Sound('./assets/sound_effects/clear_line.mp3') # Change these when compiling using pyinstaller
remove_line_music.set_volume(0.25)
land_music = pygame.mixer.Sound('./assets/sound_effects/land.mp3') # Change these when compiling using pyinstaller
land_music.set_volume(0.25)
info = pygame.display.Info()
HEIGHT = info.current_h - 200

# Set up the window
WIDTH = 601
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
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

keybinds = {
    'Left': [pygame.K_LEFT],
    'Right': [pygame.K_RIGHT],
    'Down': [pygame.K_DOWN],
    'Rotate': [pygame.K_z],
    'Store': [pygame.K_c],
    'Pause': [pygame.K_p],
    'Restart': [pygame.K_r],
    'Quit': [pygame.K_ESCAPE],
    'Drop': [pygame.K_SPACE]
}


previous_block = None # Store the name of the previous block

#Functions
def draw_grid():
    for i in range(0, 401, 40):
        pygame.draw.line(screen, WHITE, (i, 0), (i, HEIGHT + 1))
    for i in range(0, HEIGHT + 1, 40):
        pygame.draw.line(screen, WHITE, (0, i), (401, i))

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

def generate_new_block():
    new_block = Block(0, 0, [pygame.Rect(rect.x, rect.y, rect.width, rect.height) for rect in random.choice(list(shapes.values()))])
    while new_block.name == previous_block:
        new_block = Block(0, 0, [pygame.Rect(rect.x, rect.y, rect.width, rect.height) for rect in random.choice(list(shapes.values()))])
    return new_block

def draw_next_block():
    bounding_box = next_piece.shape[0].unionall(next_piece.shape[1:])
    offset_x = (160 - bounding_box.width) // 2 - bounding_box.x
    offset_y = (160 - bounding_box.height) // 2 - bounding_box.y + 175

    for rect in next_piece.shape:
        pygame.draw.rect(screen, next_piece.color, rect.move(WIDTH - 180 + offset_x, offset_y))

    next_piece_container = pygame.Rect(WIDTH - 180, 175, 160, 160)
    pygame.draw.rect(screen, WHITE, next_piece_container, 2)

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
            speed /= 1.01
            remove_line_music.play()
            break

def draw_stored_block():
    global stored_block
    if stored_block is not None:
        if stored_block == 'I' or stored_block == 'J' or stored_block == 'L':
            bounding_box = rotated_shapes[stored_block][0].unionall(rotated_shapes[stored_block][1:])
        else:
            bounding_box = shapes[stored_block][0].unionall(shapes[stored_block][1:])
        offset_x = (160 - bounding_box.width) // 2 - bounding_box.x
        offset_y = (160 - bounding_box.height) // 2 - bounding_box.y + 400

        for rect in rotated_shapes[stored_block] if stored_block in rotated_shapes else shapes[stored_block]:
            pygame.draw.rect(screen, choose_color(shapes[stored_block]), rect.move(WIDTH - 180 + offset_x, offset_y))

        stored_block_container = pygame.Rect(WIDTH - 180, 400, 160, 160)
        pygame.draw.rect(screen, WHITE, stored_block_container, 2)
        stored_block_text = font.render('Hold:', True, WHITE)
        stored_block_text_rect = stored_block_text.get_rect(center=(WIDTH - 100, 375))
        screen.blit(stored_block_text, stored_block_text_rect)

def check_lose():
    for block in placed_blocks:
        for rect in block.shape:
            if rect.y <= 100:
                return True
    return False

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_k:
                    new_keybinds = change_keybinds()
                    if new_keybinds is not None:
                        global keybinds
                        keybinds = new_keybinds
        background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 100))
        screen.blit(background, (0, 0))
        text = font.render('Paused', True, WHITE)
        text_2 = font.render('Press P to resume', True, WHITE)
        text_3 = font.render('Press ESC to quit', True, WHITE)
        text_4 = font.render('Press K to change keybinds', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        text_2_rect = text_2.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
        text_3_rect = text_3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        text_4_rect = text_4.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(text, text_rect)
        screen.blit(text_2, text_2_rect)
        screen.blit(text_3, text_3_rect)
        screen.blit(text_4, text_4_rect)
        pygame.mixer.music.pause()
        pygame.display.flip()
        clock.tick(60)
    pygame.mixer.music.unpause()
    return False

def change_keybinds():
    screen.fill(BLACK)
    title = font.render('Keybinds', True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    text_1 = font.render('Press the key you want to change', True, WHITE)
    text_1_rect = text_1.get_rect(center=(WIDTH // 2, 150))
    text_2 = font.render("Press 'A' to add a keybind", True, WHITE)
    text_2_rect = text_2.get_rect(center=(WIDTH // 2, 200))
    screen.blit(text_1, text_1_rect)
    screen.blit(text_2, text_2_rect)
    screen.blit(title, title_rect)
    for key in keybinds:
        text = font.render(f'{key}:', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 4, 300 + list(keybinds.keys()).index(key) * 50))
        screen.blit(text, text_rect)
        keybind_text = ' + '.join([pygame.key.name(k) for k in keybinds[key]])
        text = font.render(keybind_text, True, WHITE)
        text_rect = text.get_rect(center=(3 * WIDTH // 4, 300 + list(keybinds.keys()).index(key) * 50))
        screen.blit(text, text_rect)
    pygame.display.flip()
    changing = True
    while changing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return keybinds
                for key in keybinds:
                    if event.key == pygame.K_a:
                        screen.fill(BLACK)
                        text_3 = font.render('Press the key you want to bind', True, WHITE)
                        text_rect_3 = text_3.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text_3, text_rect_3)
                        pygame.display.flip()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    screen.fill(BLACK)
                                    new_key = event.key
                                    text_4 = font.render('What action do you want to bind this key to?', True, WHITE)
                                    text_rect_4 = text_4.get_rect(center=(WIDTH // 2, 150))
                                    screen.blit(text_4, text_rect_4)
                                    pygame.display.flip()
                                    for key in keybinds:
                                        text = font.render(f'{key}', True, WHITE)
                                        text_rect = text.get_rect(center=(WIDTH // 2, 300 + (list(keybinds.keys()).index(key) * 50) - 50))
                                        screen.blit(text, text_rect)
                                    selection_cursor = pygame.Rect(WIDTH // 2 - 100, 300 - 25, 200, 50)
                                    pygame.draw.rect(screen, WHITE, selection_cursor, 2)
                                    pygame.display.flip()
                                    selecting = True
                                    while selecting:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                return
                                            if event.type == pygame.KEYDOWN:
                                                if event.key == pygame.K_UP:
                                                    print(selection_cursor.y)
                                                    if selection_cursor.y > 250:
                                                        pygame.draw.rect(screen, BLACK, selection_cursor, 2)
                                                        selection_cursor.y -= 50
                                                    else:
                                                        pygame.draw.rect(screen, BLACK, selection_cursor, 2)
                                                if event.key == pygame.K_DOWN:
                                                    if selection_cursor.y > 300 + 50 * (len(keybinds) - 3):
                                                        pygame.draw.rect(screen, BLACK, selection_cursor, 2)
                                                    else:
                                                        pygame.draw.rect(screen, BLACK, selection_cursor, 2)
                                                        selection_cursor.y += 50
                                                if event.key == pygame.K_RETURN:
                                                    if isinstance(keybinds[list(keybinds.keys())[
                                                        selection_cursor.y // 50 - 4]], list):
                                                        keybinds[
                                                            list(keybinds.keys())[selection_cursor.y // 50 - 4]].append(
                                                            new_key)
                                                    else:
                                                        keybinds[
                                                            list(keybinds.keys())[selection_cursor.y // 50 - 4]] = [
                                                            keybinds[
                                                                list(keybinds.keys())[selection_cursor.y // 50 - 4]],
                                                            new_key]
                                                    selecting = False
                                                    print(keybinds)
                                                pygame.draw.rect(screen, WHITE, selection_cursor, 2)
                                                pygame.display.flip()
                                    return keybinds
                    if event.key in keybinds[key]:
                        screen.fill(BLACK)
                        text_3 = font.render('Press the key you want to bind', True, WHITE)
                        text_rect_3 = text_3.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text_3, text_rect_3)
                        pygame.display.flip()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    keybinds[key] = [event.key]
                                    return keybinds

    return keybinds

def restart():
    global placed_blocks, current_block, stored_block, score, speed
    screen.fill(BLACK)
    placed_blocks = []
    current_block = generate_new_block()
    stored_block = None
    pygame.mixer.music.rewind()
    pygame.mixer.music.play(-1)
    score = 0
    speed = 1

# Set up the fonts
font = pygame.font.Font('freesansbold.ttf', 32)

# Define all Tetris shapes
shapes = {
    'I': [pygame.Rect(0, 0, 38, 38), pygame.Rect(0, 40, 38, 38), pygame.Rect(0, 80, 38, 38),
          pygame.Rect(0, 120, 38, 38)],
    'J': [pygame.Rect(0, 0, 38, 38), pygame.Rect(0, 40, 38, 38), pygame.Rect(0, 80, 38, 38),
          pygame.Rect(40, 80, 38, 38)],
    'L': [pygame.Rect(40, 0, 38, 38), pygame.Rect(40, 40, 38, 38), pygame.Rect(40, 80, 38, 38),
          pygame.Rect(0, 80, 38, 38)],
    'O': [pygame.Rect(0, 0, 38, 38), pygame.Rect(40, 0, 38, 38), pygame.Rect(0, 40, 38, 38),
          pygame.Rect(40, 40, 38, 38)],
    'S': [pygame.Rect(0, 40, 38, 38), pygame.Rect(40, 40, 38, 38), pygame.Rect(40, 0, 38, 38),
          pygame.Rect(80, 0, 38, 38)],
    'T': [pygame.Rect(0, 0, 38, 38), pygame.Rect(40, 0, 38, 38), pygame.Rect(80, 0, 38, 38),
          pygame.Rect(40, 40, 38, 38)],
    'Z': [pygame.Rect(0, 0, 38, 38), pygame.Rect(40, 0, 38, 38), pygame.Rect(40, 40, 38, 38),
          pygame.Rect(80, 40, 38, 38)]
}

rotated_shapes = {
    'I': [pygame.Rect(0, 0, 38, 38), pygame.Rect(40, 0, 38, 38), pygame.Rect(80, 0, 38, 38),
          pygame.Rect(120, 0, 38, 38)],
    'J': [pygame.Rect(0, 0, 38, 38), pygame.Rect(40, 0, 38, 38), pygame.Rect(80, 0, 38, 38),
          pygame.Rect(80, 40, 38, 38)],
    'L': [pygame.Rect(0, 0, 38, 38), pygame.Rect(40, 0, 38, 38), pygame.Rect(80, 0, 38, 38), pygame.Rect(0, 40, 38, 38)]
}

placed_blocks = []

block_colors = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]


class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.name = get_name(shape)
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
        global initial_time
        pivot = self.shape[1]  # Use the second block as the pivot
        for rect in self.shape:
            # Translate block to origin
            x = rect.x - pivot.x
            y = rect.y - pivot.y
            # Rotate 90 degrees clockwise
            rect.x = pivot.x - y
            rect.y = pivot.y + x
            # Check collision with placed blocks
        for rect in self.shape:
            for block in placed_blocks:
                while any(rect.colliderect(placed_rect) for placed_rect in block.shape):
                    for rectangle in self.shape:
                        rectangle.y -= 40
                    initial_time = time.time() # Reset the timer
        for rect in self.shape:
            if rect.x < 0:
                self.move(40)
            if rect.x >= 400:
                self.move(-40)
            if rect.y >= HEIGHT:
                for rectangle in self.shape:
                    rectangle.y -= 40
                return
            if rect.y < 100:
                for rectangle in self.shape:
                    rectangle.y += 40
                return

    def rotate_back(self, pivot):
        for rect in self.shape:
            # Translate block to origin
            x = rect.x - pivot.x
            y = rect.y - pivot.y
            # Rotate 90 degrees counter-clockwise
            rect.x = pivot.x + y
            rect.y = pivot.y - x

    def predict_placement(self):
        copy_of_shape = Block(self.x, self.y, [pygame.Rect(rect.x, rect.y, rect.width, rect.height) for rect in self.shape])
        while not check_collision(copy_of_shape):
            copy_of_shape.fall()
        for i in range(len(copy_of_shape.shape)):
            copy_of_shape.shape[i].y -= 40
        for rect in copy_of_shape.shape:
            rect_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            rect_surf.fill((255, 255, 255, 16))
            pygame.draw.rect(rect_surf, self.color, rect_surf.get_rect(), 1)
            screen.blit(rect_surf, (rect.x, rect.y))


current_block = generate_new_block()
next_piece = generate_new_block()


speed = 1
stored_block = None
initial_time = time.time()


# Score
score = 0

running = True
while running:
    screen.fill(BLACK)

    score_text = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH - 100, 50))
    next_piece_text = font.render('Next:', True, WHITE)
    next_piece_rect = next_piece_text.get_rect(center=(WIDTH - 100, 150))
    screen.blit(score_text, score_rect)
    screen.blit(next_piece_text, next_piece_rect)
    draw_grid()
    current_block.predict_placement()
    current_block.draw()
    remove_line()
    place_blocks(placed_blocks)
    draw_stored_block()
    draw_next_block()
    if check_lose():
        screen.fill(BLACK)
        text = font.render('You Lose!', True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.mixer.music.pause()
        time.sleep(3)
        restart()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for key in keybinds:
                if event.key in keybinds[key]:
                    if key == 'Right':
                        current_block.move(40)
                    if key == 'Left':
                        current_block.move(-40)
                    if key == 'Down':
                        current_block.fall()
                        score += 1
                        if check_collision(current_block):
                            for i in range(len(current_block.shape)):
                                current_block.shape[i].y -= 40
                            placed_blocks.append(current_block)
                            land_music.play()
                            previous_block = current_block.name
                            current_block = next_piece
                            next_piece = generate_new_block()
                    if key == 'Rotate':
                        if current_block.name == 'O':
                            break
                        current_block.rotate()
                    if key == 'Store':
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
                    if key == 'Restart':
                        restart()
                    if key == 'Quit':
                        running = False
                    if key == 'Pause':
                        if pause():
                            running = False
                    if key == 'Drop':
                        while not check_collision(current_block):
                            current_block.fall()
                            score += 1
                        for i in range(len(current_block.shape)):
                            current_block.shape[i].y -= 40
                        placed_blocks.append(current_block)
                        land_music.play()
                        previous_block = current_block.name
                        current_block = next_piece
                        next_piece = generate_new_block()

            if event.key == pygame.K_m:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                if remove_line_music.get_volume() == 0.25:
                    remove_line_music.set_volume(0)
                    land_music.set_volume(0)
                else:
                    remove_line_music.set_volume(0.25)
                    land_music.set_volume(0.25)


    if check_collision(current_block):
        placed_blocks.append(current_block)
        land_music.play()
        previous_block = current_block.name
        current_block = next_piece
        next_piece = generate_new_block()

    if time.time() - initial_time > speed:
        current_block.fall()
        if check_collision(current_block):
            for i in range(len(current_block.shape)):
                current_block.shape[i].y -= 40
            placed_blocks.append(current_block)
            land_music.play()
            previous_block = current_block.name
            current_block = next_piece
            next_piece = generate_new_block()
        initial_time = time.time()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()