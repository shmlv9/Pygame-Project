import pygame
import sys
from load_functions import load_image, load_level

# Инициализация Pygame
pygame.init()
base_width, base_height = 500, 500
current_width, current_height = base_width, base_height
is_fullscreen = False
screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
base_surface = pygame.Surface((base_width, base_height))
clock = pygame.time.Clock()

# Переменные для меню
characters = ["chill-guy.png", "dog_with_apple.png", "nuggets.png", "steve.png"]
current_character = 0
balance = 0


def start_screen():
    global current_width, current_height, is_fullscreen, screen
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор уровня", True, pygame.Color('white'))
    buttons = [font.render(f"Уровень {i + 1}", True, pygame.Color('white')) for i in range(5)]

    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not is_fullscreen:
                    current_width, current_height = event.w, event.h
                    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        current_width, current_height = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    return selected + 1

        # Отрисовка на базовой поверхности
        base_surface.fill((0, 0, 0))
        base_surface.blit(title, (base_width // 2 - title.get_width() // 2, 50))

        for i, button in enumerate(buttons):
            color = (255, 0, 0) if i == selected else (255, 255, 255)
            text = font.render(f"Уровень {i + 1}", True, color)
            base_surface.blit(text, (base_width // 2 - text.get_width() // 2, 150 + i * 60))

        # Масштабирование и вывод на экран
        scale = min(current_width / base_width, current_height / base_height)
        scaled_width = int(base_width * scale)
        scaled_height = int(base_height * scale)
        scaled_surface = pygame.transform.scale(base_surface, (scaled_width, scaled_height))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - scaled_width) // 2, (current_height - scaled_height) // 2))
        pygame.display.flip()
        clock.tick(60)


def character_selection():
    global current_character, current_width, current_height, is_fullscreen, screen
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор персонажа", True, pygame.Color('white'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not is_fullscreen:
                    current_width, current_height = event.w, event.h
                    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        current_width, current_height = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
                elif event.key == pygame.K_RIGHT:
                    current_character = (current_character + 1) % len(characters)
                elif event.key == pygame.K_LEFT:
                    current_character = (current_character - 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    return

        # Отрисовка на базовой поверхности
        base_surface.fill((0, 0, 0))
        base_surface.blit(title, (base_width // 2 - title.get_width() // 2, 50))

        character_image = load_image(characters[current_character])
        character_image = pygame.transform.scale(character_image, (200, 200))
        base_surface.blit(character_image, (base_width // 2 - 100, base_height // 2 - 100))

        # Масштабирование и вывод на экран
        scale = min(current_width / base_width, current_height / base_height)
        scaled_width = int(base_width * scale)
        scaled_height = int(base_height * scale)
        scaled_surface = pygame.transform.scale(base_surface, (scaled_width, scaled_height))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - scaled_width) // 2, (current_height - scaled_height) // 2))
        pygame.display.flip()
        clock.tick(60)


# Основной игровой процесс
def game_loop(level):
    global balance, current_width, current_height, is_fullscreen, screen

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('floor.png')
    }
    player_image = load_image(characters[current_character])
    player_image = pygame.transform.scale(player_image, (40, 40))

    tile_width = tile_height = 50

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.pos_x = pos_x
            self.pos_y = pos_y

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
            self.pos_x = pos_x
            self.pos_y = pos_y

    def generate_level(level):
        new_player = None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        return new_player

    def check_box(x, y):
        if 0 <= y < len(level_map) and 0 <= x < len(level_map[0]):
            return level_map[y][x] != '#'
        return False

    level_map = load_level(f'level{level}.txt')
    player = generate_level(level_map)

    move_cooldown = 200
    last_move_time = pygame.time.get_ticks()

    goal_x = len(level_map[0]) - 1
    goal_y = len(level_map) - 1

    vision_surface = pygame.Surface((5 * tile_width, 5 * tile_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                if not is_fullscreen:
                    current_width, current_height = event.w, event.h
                    screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        current_width, current_height = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > move_cooldown:
            if keys[pygame.K_RIGHT] and check_box(player.pos_x + 1, player.pos_y):
                player.pos_x += 1
                player.rect.x += tile_width
                last_move_time = current_time
            if keys[pygame.K_LEFT] and check_box(player.pos_x - 1, player.pos_y):
                player.pos_x -= 1
                player.rect.x -= tile_width
                last_move_time = current_time
            if keys[pygame.K_UP] and check_box(player.pos_x, player.pos_y - 1):
                player.pos_y -= 1
                player.rect.y -= tile_height
                last_move_time = current_time
            if keys[pygame.K_DOWN] and check_box(player.pos_x, player.pos_y + 1):
                player.pos_y += 1
                player.rect.y += tile_height
                last_move_time = current_time

        if player.pos_x == goal_x and player.pos_y == goal_y:
            balance += 10
            character_selection()
            level = start_screen()
            return game_loop(level)

        # Отрисовка поля зрения
        vision_surface.fill((0, 0, 0))
        start_x = player.pos_x - 2
        end_x = player.pos_x + 2
        start_y = player.pos_y - 2
        end_y = player.pos_y + 2

        for tile in tiles_group:
            if start_x <= tile.pos_x <= end_x and start_y <= tile.pos_y <= end_y:
                dx = tile.pos_x - player.pos_x
                dy = tile.pos_y - player.pos_y
                x = (dx + 2) * tile_width
                y = (dy + 2) * tile_height
                vision_surface.blit(tile.image, (x, y))

        player_vision_x = 2 * tile_width + 5
        player_vision_y = 2 * tile_height
        vision_surface.blit(player.image, (player_vision_x, player_vision_y))

        # Отрисовка на базовой поверхности
        base_surface.fill((0, 0, 0))
        base_surface.blit(vision_surface, (base_width // 2 - vision_surface.get_width() // 2,
                                           base_height // 2 - vision_surface.get_height() // 2))

        # Отображение баланса
        font = pygame.font.Font(None, 36)
        balance_text = font.render(f"Баланс: {balance}", True, pygame.Color('white'))
        base_surface.blit(balance_text, (10, 10))

        # Масштабирование и вывод на экран
        scale = min(current_width / base_width, current_height / base_height)
        scaled_width = int(base_width * scale)
        scaled_height = int(base_height * scale)
        scaled_surface = pygame.transform.scale(base_surface, (scaled_width, scaled_height))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - scaled_width) // 2, (current_height - scaled_height) // 2))
        pygame.display.flip()
        clock.tick(60)


# Основная программа
level = start_screen()
character_selection()
game_loop(level)