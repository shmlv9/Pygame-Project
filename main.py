import pygame
import sys
import os

# Инициализация Pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Переменные для меню
characters = ["mario.png", "chill-guy.png", "dog_with_apple.png"]
current_character = 0
balance = 0


# Функции

def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    return pygame.image.load(fullname)


def start_screen():
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор уровня", True, pygame.Color('white'))
    buttons = [font.render(f"Уровень {i + 1}", True, pygame.Color('white')) for i in range(5)]

    selected = 0

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        for i, button in enumerate(buttons):
            color = (255, 0, 0) if i == selected else (255, 255, 255)
            text = font.render(f"Уровень {i + 1}", True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, 150 + i * 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    return selected + 1

        pygame.display.flip()
        clock.tick(60)


def character_selection():
    global current_character
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор персонажа", True, pygame.Color('white'))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        character_image = load_image(characters[current_character])
        character_image = pygame.transform.scale(character_image, (100, 100))
        screen.blit(character_image, (width // 2 - 50, height // 2 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_character = (current_character + 1) % len(characters)
                elif event.key == pygame.K_LEFT:
                    current_character = (current_character - 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    return

        pygame.display.flip()
        clock.tick(60)


# Основной игровой процесс
def game_loop(level):
    global balance

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image(characters[current_character])

    tile_width = tile_height = 50

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
            self.pos_x = pos_x  # Добавляем координаты клетки
            self.pos_y = pos_y  #

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
            self.pos_x = pos_x
            self.pos_y = pos_y

    def load_level(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

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

    move_cooldown = 200  # Задержка между ходами (мс)
    last_move_time = pygame.time.get_ticks()

    # Определяем крайнюю точку карты (правый нижний угол)
    goal_x = len(level_map[0]) - 1
    goal_y = len(level_map) - 1

    # Создаем поверхность для поля зрения 5x5
    vision_surface = pygame.Surface((5 * tile_width, 5 * tile_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        # Проверка на достижение цели
        if player.pos_x == goal_x and player.pos_y == goal_y:
            balance += 10
            print("Уровень пройден! Баланс:", balance)
            character_selection()
            level = start_screen()
            return game_loop(level)

        # Отрисовка поля зрения 5x5
        vision_surface.fill((0, 0, 0))  # Очищаем поверхность

        # Границы поля зрения
        start_x = player.pos_x - 2
        end_x = player.pos_x + 2
        start_y = player.pos_y - 2
        end_y = player.pos_y + 2

        # Отрисовываем тайлы в поле зрения
        for tile in tiles_group:
            if start_x <= tile.pos_x <= end_x and start_y <= tile.pos_y <= end_y:
                # Вычисляем позицию на поверхности поля зрения
                dx = tile.pos_x - player.pos_x
                dy = tile.pos_y - player.pos_y
                x = (dx + 2) * tile_width
                y = (dy + 2) * tile_height
                vision_surface.blit(tile.image, (x, y))

        # Отрисовываем игрока в центре поля зрения
        player_vision_x = 2 * tile_width + 15  # Смещение как в оригинале
        player_vision_y = 2 * tile_height + 5
        vision_surface.blit(player.image, (player_vision_x, player_vision_y))

        # Отрисовка на основном экране
        screen.fill((0, 0, 0))
        # Размещаем поле зрения по центру экрана
        screen.blit(vision_surface, (width // 2 - vision_surface.get_width() // 2,
                                     height // 2 - vision_surface.get_height() // 2))

        # Отображение баланса
        font = pygame.font.Font(None, 36)
        balance_text = font.render(f"Баланс: {balance}", True, pygame.Color('white'))
        screen.blit(balance_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


# Основная программа
character_selection()
level = start_screen()
game_loop(level)