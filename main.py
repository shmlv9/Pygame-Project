import pygame
import sys
from load_functions import load_image, load_level

# Инициализация Pygame
pygame.init()
pygame.display.set_caption("Get Out")
base_width, base_height = 500, 500
current_width, current_height = base_width, base_height
is_fullscreen = False
screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
base_surface = pygame.Surface((base_width, base_height))
clock = pygame.time.Clock()

# Переменные для меню
characters = ["chill-guy.png", "dog_with_apple.png", "nuggets.png", "steve.png", "gopher.png", "elephant.png"]
current_character = 0
balance = 0


def initial_screen():
    """
    Отображает начальный экран с надписью "Get Out" и кнопкой "Начать".
    Экран масштабируется пропорционально базовому разрешению.
    При нажатии на кнопку (либо клавишей ENTER, либо кликом мышью) возвращается управление.
    """
    global current_width, current_height, is_fullscreen, screen

    # Создаём шрифты для заголовка и кнопки
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)

    # Рендерим текст
    title_text = title_font.render("Get Out", True, pygame.Color('white'))
    button_text = button_font.render("Начать", True, pygame.Color('white'))

    # Вычисляем позиции: заголовок чуть выше центра, кнопка – ниже заголовка
    title_pos = (base_width // 2 - title_text.get_width() // 2, base_height // 2 - title_text.get_height() - 20)
    button_pos = (base_width // 2 - button_text.get_width() // 2, base_height // 2 + 20)
    # Для проверки клика определяем прямоугольную область кнопки (в координатах базовой поверхности)
    button_rect = button_text.get_rect(topleft=button_pos)

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
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                    pygame.mixer.music.play()
                    return  # Переход в меню выбора уровня
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    # Преобразуем координаты мыши из экранных в координаты базовой поверхности
                    scale = min(current_width / base_width, current_height / base_height)
                    scaled_width = int(base_width * scale)
                    scaled_height = int(base_height * scale)
                    offset_x = (current_width - scaled_width) // 2
                    offset_y = (current_height - scaled_height) // 2
                    rel_x = (event.pos[0] - offset_x) / scale
                    rel_y = (event.pos[1] - offset_y) / scale
                    if button_rect.collidepoint(rel_x, rel_y):
                        pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                        pygame.mixer.music.play()
                        return

        # Отрисовка на базовой поверхности
        base_surface.fill((0, 0, 0))
        base_surface.blit(title_text, title_pos)
        base_surface.blit(button_text, button_pos)

        # Масштабирование базовой поверхности под текущее окно
        scale = min(current_width / base_width, current_height / base_height)
        scaled_width = int(base_width * scale)
        scaled_height = int(base_height * scale)
        scaled_surface = pygame.transform.scale(base_surface, (scaled_width, scaled_height))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - scaled_width) // 2, (current_height - scaled_height) // 2))
        pygame.display.flip()
        clock.tick(60)


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
                    pygame.mixer.music.load('data/sounds/najatie-na-kompyuternuyu-knopku1.mp3')
                    pygame.mixer.music.play()
                    selected = (selected + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    pygame.mixer.music.load('data/sounds/najatie-na-kompyuternuyu-knopku1.mp3')
                    pygame.mixer.music.play()
                    selected = (selected - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                    pygame.mixer.music.play()
                    return selected + 1

        base_surface.fill((0, 0, 0))
        base_surface.blit(title, (base_width // 2 - title.get_width() // 2, 50))

        for i, button in enumerate(buttons):
            color = (255, 0, 0) if i == selected else (255, 255, 255)
            text = font.render(f"Уровень {i + 1}", True, color)
            base_surface.blit(text, (base_width // 2 - text.get_width() // 2, 150 + i * 60))

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
                    pygame.mixer.music.load('data/sounds/najatie-na-kompyuternuyu-knopku1.mp3')
                    pygame.mixer.music.play()
                    current_character = (current_character + 1) % len(characters)
                elif event.key == pygame.K_LEFT:
                    pygame.mixer.music.load('data/sounds/najatie-na-kompyuternuyu-knopku1.mp3')
                    pygame.mixer.music.play()
                    current_character = (current_character - 1) % len(characters)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                    pygame.mixer.music.play()
                    return

        base_surface.fill((0, 0, 0))
        base_surface.blit(title, (base_width // 2 - title.get_width() // 2, 50))

        character_image = load_image(characters[current_character])
        character_image = pygame.transform.scale(character_image, (200, 200))
        base_surface.blit(character_image, (base_width // 2 - 100, base_height // 2 - 100))

        scale = min(current_width / base_width, current_height / base_height)
        scaled_width = int(base_width * scale)
        scaled_height = int(base_height * scale)
        scaled_surface = pygame.transform.scale(base_surface, (scaled_width, scaled_height))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - scaled_width) // 2, (current_height - scaled_height) // 2))
        pygame.display.flip()
        clock.tick(60)


def victory_screen(time_str):
    """
    Отображает окно победы с поздравлением, временем прохождения и подсказкой.
    Размеры шрифтов вычисляются пропорционально текущему размеру окна, а текст отрисовывается по центру.
    """
    global current_width, current_height, screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Обновляем текущий размер окна и перезадаем режим
                current_width, current_height = event.w, event.h
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Выходим из окна победы

        # Вычисляем коэффициент масштабирования относительно базового разрешения
        scale = min(current_width / base_width, current_height / base_height)
        # Определяем размеры шрифтов с учётом масштаба
        header_size = max(1, int(40 * scale))
        time_size = max(1, int(30 * scale))
        hint_size = max(1, int(20 * scale))

        # Создаем шрифты с динамическими размерами
        victory_font = pygame.font.Font(None, header_size)
        time_font = pygame.font.Font(None, time_size)
        small_font = pygame.font.Font(None, hint_size)

        # Рендерим текст
        congrat_text = victory_font.render("Вы смогли выбраться.", True, pygame.Color('white'))
        time_text = time_font.render(f"Время прохождения: {time_str}", True, pygame.Color('white'))
        hint_text = small_font.render("Нажмите ENTER для выхода в главное меню", True, pygame.Color('white'))

        # Вычисляем координаты для центрирования
        congrat_x = (current_width - congrat_text.get_width()) // 2
        congrat_y = current_height // 3 - congrat_text.get_height() // 2
        time_x = (current_width - time_text.get_width()) // 2
        time_y = current_height // 2 - time_text.get_height() // 2
        hint_x = (current_width - hint_text.get_width()) // 2
        hint_y = (2 * current_width) // 3 - hint_text.get_height() // 2

        # Отрисовка окна победы
        screen.fill((0, 0, 0))
        screen.blit(congrat_text, (congrat_x, congrat_y))
        screen.blit(time_text, (time_x, time_y))
        screen.blit(hint_text, (hint_x, hint_y))
        pygame.display.flip()
        clock.tick(60)


# Основной игровой процесс
def game_loop(level):
    global balance, current_width, current_height, is_fullscreen, screen, TIME

    pygame.mixer.music.load('data/music/music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('floor.png'),
        'exit': load_image('exit.png')
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
                elif level[y][x] == 'E':
                    Tile('exit', x, y)
                    exit_coords = (x, y)
        return new_player, exit_coords

    def check_box(x, y):
        if 0 <= y < len(level_map) and 0 <= x < len(level_map[0]):
            return level_map[y][x] != '#'
        return False

    level_map = load_level(f'level{level}.txt')
    player, exit_coords = generate_level(level_map)
    move_cooldown = 200
    last_move_time = pygame.time.get_ticks()
    vision_surface = pygame.Surface((5 * tile_width, 5 * tile_height))

    # Засекаем время начала уровня
    start_time = pygame.time.get_ticks()

    while True:
        victory = False
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
            # Обработка движения с проверкой выхода за границы
            if keys[pygame.K_RIGHT]:
                new_x = player.pos_x + 1
                if (new_x, player.pos_y) == exit_coords:
                    victory = True
                elif check_box(new_x, player.pos_y):
                    player.pos_x = new_x
                    player.rect.x += tile_width
                    last_move_time = current_time

            if keys[pygame.K_LEFT]:
                new_x = player.pos_x - 1
                if (new_x, player.pos_y) == exit_coords:
                    victory = True
                elif check_box(new_x, player.pos_y):
                    player.pos_x = new_x
                    player.rect.x -= tile_width
                    last_move_time = current_time

            if keys[pygame.K_UP]:
                new_y = player.pos_y - 1
                if (player.pos_x, new_y) == exit_coords:
                    victory = True
                elif check_box(player.pos_x, new_y):
                    player.pos_y = new_y
                    player.rect.y -= tile_height
                    last_move_time = current_time

            if keys[pygame.K_DOWN]:
                new_y = player.pos_y + 1
                if (player.pos_x, new_y) == exit_coords:
                    victory = True
                elif check_box(player.pos_x, new_y):
                    player.pos_y = new_y
                    player.rect.y += tile_height
                    last_move_time = current_time

        # Вычисляем время прохождения в формате ММ:СС
        elapsed_ms = pygame.time.get_ticks() - start_time
        total_seconds = elapsed_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        if victory:
            # Записываем время прохождения уровня в переменную TIME в формате ММ:СС
            TIME = time_str
            balance += 10
            print("Уровень пройден!")
            print("Время прохождения уровня:", TIME)
            print("Баланс:", balance)
            pygame.mixer.music.stop()
            victory_screen(time_str)
            level = start_screen()
            character_selection()
            return game_loop(level)

        # Отрисовка игрового поля (ограниченная видимость)
        vision_surface.fill((0, 0, 0))
        start_x = player.pos_x - 2
        end_x = player.pos_x + 2
        start_y = player.pos_y - 2
        end_y = player.pos_y + 2

        dark_coords = []

        for tile in tiles_group:
            if start_x <= tile.pos_x <= end_x and start_y <= tile.pos_y <= end_y:
                dx = tile.pos_x - player.pos_x
                dy = tile.pos_y - player.pos_y
                x = (dx + 2) * tile_width
                y = (dy + 2) * tile_height
                vision_surface.blit(tile.image, (x, y))
            if start_x == tile.pos_x or start_y == tile.pos_y or end_x == tile.pos_x or end_y == tile.pos_y:
                dx = tile.pos_x - player.pos_x
                dy = tile.pos_y - player.pos_y
                x = (dx + 2) * tile_width
                y = (dy + 2) * tile_height
                dark_coords.append((x, y))
        for (x, y) in set(dark_coords):
            transparent_rect = pygame.Surface((50, 50), pygame.SRCALPHA)
            transparent_rect.fill((0, 0, 0, 128))
            vision_surface.blit(transparent_rect, (x, y))

        player_vision_x = 2 * tile_width + 5
        player_vision_y = 2 * tile_height
        vision_surface.blit(player.image, (player_vision_x, player_vision_y))

        # Отрисовка на базовой поверхности
        base_surface.fill((0, 0, 0))
        base_surface.blit(vision_surface, (base_width // 2 - vision_surface.get_width() // 2,
                                           base_height // 2 - vision_surface.get_height() // 2))

        # Отображение баланса и времени на базовой поверхности
        font_small = pygame.font.Font(None, 36)
        balance_text = font_small.render(f"Баланс: {balance}", True, pygame.Color('white'))
        base_surface.blit(balance_text, (10, 10))

        # Отображение времени в правом верхнем углу
        time_text = font_small.render(time_str, True, pygame.Color('white'))
        base_surface.blit(time_text, (base_width - time_text.get_width() - 10, 10))

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
initial_screen()
level = start_screen()
character_selection()
game_loop(level)
