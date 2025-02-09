import pygame
import sys
import random
from load_functions import load_image, load_level
from database_command import get_record, update_record

# Инициализация Pygame и базовые настройки окна
pygame.init()
pygame.display.set_caption("Get Out")
base_width, base_height = 500, 500
current_width, current_height = base_width, base_height
is_fullscreen = False
screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
base_surface = pygame.Surface((base_width, base_height))
clock = pygame.time.Clock()

# Глобальные переменные для персонажей и баланса
all_characters = ["chill-guy.png", "dog_with_apple.png", "nuggets.png", "steve.png", "gopher.png", "elephant.png"]
owned_characters = all_characters[:2]  # изначально доступны только первые 2 персонажа
current_character = 0
balance = 0


def draw_balance(surface):
    """Отображает баланс в левом верхнем углу на переданной поверхности."""
    small_font = pygame.font.Font(None, 30)
    balance_text = small_font.render(f"Баланс: {balance}", True, pygame.Color('white'))
    surface.blit(balance_text, (10, 10))


# ==========================
# Главное меню
# ==========================
def main_menu():
    global current_width, current_height, is_fullscreen, screen
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)

    title_text = title_font.render("Get Out", True, pygame.Color('white'))
    start_text = button_font.render("Начать", True, pygame.Color('white'))
    buy_text = button_font.render("Купить персонажа", True, pygame.Color('white'))
    leaderboard_text = button_font.render("Таблица рекордов", True, pygame.Color('white'))

    # Позиционирование надписей
    title_pos = (base_width // 2 - title_text.get_width() // 2, 50)
    start_pos = (base_width // 2 - start_text.get_width() // 2, base_height // 2 - 60)
    buy_pos = (base_width // 2 - buy_text.get_width() // 2, base_height // 2)
    leaderboard_pos = (base_width // 2 - leaderboard_text.get_width() // 2, base_height // 2 + 60)

    # Прямоугольники для проверки кликов
    start_rect = start_text.get_rect(topleft=start_pos)
    buy_rect = buy_text.get_rect(topleft=buy_pos)
    leaderboard_rect = leaderboard_text.get_rect(topleft=leaderboard_pos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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
                    return "start"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    scale = min(current_width / base_width, current_height / base_height)
                    scaled_width = int(base_width * scale)
                    scaled_height = int(base_height * scale)
                    offset_x = (current_width - scaled_width) // 2
                    offset_y = (current_height - scaled_height) // 2
                    rel_x = (event.pos[0] - offset_x) / scale
                    rel_y = (event.pos[1] - offset_y) / scale
                    if start_rect.collidepoint(rel_x, rel_y):
                        pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                        pygame.mixer.music.play()
                        return "start"
                    elif buy_rect.collidepoint(rel_x, rel_y):
                        pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                        pygame.mixer.music.play()
                        return "buy"
                    elif leaderboard_rect.collidepoint(rel_x, rel_y):
                        pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                        pygame.mixer.music.play()
                        return "leaderboard"

        base_surface.fill((0, 0, 0))
        base_surface.blit(title_text, title_pos)
        base_surface.blit(start_text, start_pos)
        base_surface.blit(buy_text, buy_pos)
        base_surface.blit(leaderboard_text, leaderboard_pos)
        draw_balance(base_surface)

        scale = min(current_width / base_width, current_height / base_height)
        scaled_surface = pygame.transform.scale(base_surface, (int(base_width * scale), int(base_height * scale)))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - int(base_width * scale)) // 2,
                                     (current_height - int(base_height * scale)) // 2))
        pygame.display.flip()
        clock.tick(60)


# ==========================
# Экран выбора уровня
# ==========================
def start_screen():
    global current_width, current_height, is_fullscreen, screen
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор уровня", True, pygame.Color('white'))
    buttons = [font.render(f"Уровень {i + 1}", True, pygame.Color('white')) for i in range(5)]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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
            text = pygame.font.Font(None, 50).render(f"Уровень {i + 1}", True, color)
            base_surface.blit(text, (base_width // 2 - text.get_width() // 2, 150 + i * 60))
        draw_balance(base_surface)

        scale = min(current_width / base_width, current_height / base_height)
        scaled_surface = pygame.transform.scale(base_surface, (int(base_width * scale), int(base_height * scale)))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - int(base_width * scale)) // 2,
                                     (current_height - int(base_height * scale)) // 2))
        pygame.display.flip()
        clock.tick(60)


# ==========================
# Экран выбора персонажа
# ==========================
def character_selection():
    global current_character, current_width, current_height, is_fullscreen, screen, owned_characters
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор персонажа", True, pygame.Color('white'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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
                    current_character = (current_character + 1) % len(owned_characters)
                elif event.key == pygame.K_LEFT:
                    pygame.mixer.music.load('data/sounds/najatie-na-kompyuternuyu-knopku1.mp3')
                    pygame.mixer.music.play()
                    current_character = (current_character - 1) % len(owned_characters)
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('data/sounds/knopka-vyiklyuchatelya1.mp3')
                    pygame.mixer.music.play()
                    return
        base_surface.fill((0, 0, 0))
        base_surface.blit(title, (base_width // 2 - title.get_width() // 2, 50))
        character_image = load_image(owned_characters[current_character])
        character_image = pygame.transform.scale(character_image, (200, 200))
        base_surface.blit(character_image, (base_width // 2 - 100, base_height // 2 - 100))
        draw_balance(base_surface)

        scale = min(current_width / base_width, current_height / base_height)
        scaled_surface = pygame.transform.scale(base_surface, (int(base_width * scale), int(base_height * scale)))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - int(base_width * scale)) // 2,
                                     (current_height - int(base_height * scale)) // 2))
        pygame.display.flip()
        clock.tick(60)


# ==========================
# Экран покупки персонажа
# ==========================
def buy_character_screen():
    global balance, all_characters, owned_characters, current_width, current_height, is_fullscreen, screen
    # Используем меньший шрифт, чтобы текст поместился
    buy_font = pygame.font.Font(None, 30)
    # Разбиваем текст вопроса на две строки
    question_text1 = buy_font.render("Купить рандомного", True, pygame.Color('white'))
    question_text2 = buy_font.render("персонажа за 50 денег?", True, pygame.Color('white'))
    yes_text = buy_font.render("ДА", True, pygame.Color('white'))
    no_text = buy_font.render("НЕТ", True, pygame.Color('white'))

    # Позиционирование текста так, чтобы всё помещалось
    question_pos1 = (base_width // 2 - question_text1.get_width() // 2, base_height // 2 - 100)
    question_pos2 = (base_width // 2 - question_text2.get_width() // 2, base_height // 2 - 60)
    yes_pos = (base_width // 2 - yes_text.get_width() - 20, base_height // 2 + 20)
    no_pos = (base_width // 2 + 20, base_height // 2 + 20)

    yes_rect = yes_text.get_rect(topleft=yes_pos)
    no_rect = no_text.get_rect(topleft=no_pos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    scale = min(current_width / base_width, current_height / base_height)
                    scaled_width = int(base_width * scale)
                    scaled_height = int(base_height * scale)
                    offset_x = (current_width - scaled_width) // 2
                    offset_y = (current_height - scaled_height) // 2
                    rel_x = (event.pos[0] - offset_x) / scale
                    rel_y = (event.pos[1] - offset_y) / scale
                    if yes_rect.collidepoint(rel_x, rel_y):
                        if balance >= 50:
                            available_to_buy = [char for char in all_characters if char not in owned_characters]
                            if available_to_buy:
                                new_char = random.choice(available_to_buy)
                                owned_characters.append(new_char)
                                balance -= 50
                        return
                    elif no_rect.collidepoint(rel_x, rel_y):
                        return

        base_surface.fill((0, 0, 0))
        base_surface.blit(question_text1, question_pos1)
        base_surface.blit(question_text2, question_pos2)
        base_surface.blit(yes_text, yes_pos)
        base_surface.blit(no_text, no_pos)
        draw_balance(base_surface)

        scale = min(current_width / base_width, current_height / base_height)
        scaled_surface = pygame.transform.scale(base_surface, (int(base_width * scale), int(base_height * scale)))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - int(base_width * scale)) // 2,
                                     (current_height - int(base_height * scale)) // 2))
        pygame.display.flip()
        clock.tick(60)


# ==========================
# Экран таблицы рекордов
# ==========================
def leaderboard_screen():
    global current_width, current_height, is_fullscreen, screen
    # Используем отдельные шрифты для заголовка, списка рекордов и подсказки
    title_font = pygame.font.Font(None, 60)
    record_font = pygame.font.Font(None, 40)
    info_font = pygame.font.Font(None, 30)

    title_text = title_font.render("Рекорды", True, pygame.Color('white'))
    # Формируем список строк для каждого уровня (здесь для 5 уровней)
    records = [f"уровень {i + 1} - {get_record(f'level{i + 1}')}" for i in range(5)]
    record_texts = [record_font.render(rec, True, pygame.Color('white')) for rec in records]
    info_text = info_font.render("Нажмите ENTER для возврата", True, pygame.Color('white'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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
                    return

        base_surface.fill((0, 0, 0))
        # Отрисовываем заголовок "Рекорды" вверху
        title_pos = (base_width // 2 - title_text.get_width() // 2, 30)
        base_surface.blit(title_text, title_pos)
        # Отрисовываем список рекордов ниже заголовка
        start_y = title_pos[1] + title_text.get_height() + 20
        for i, rec_text in enumerate(record_texts):
            rec_pos = (base_width // 2 - rec_text.get_width() // 2, start_y + i * (rec_text.get_height() + 10))
            base_surface.blit(rec_text, rec_pos)
        # Подсказка для возврата
        info_pos = (base_width // 2 - info_text.get_width() // 2, base_height - info_text.get_height() - 20)
        base_surface.blit(info_text, info_pos)
        draw_balance(base_surface)

        scale = min(current_width / base_width, current_height / base_height)
        scaled_surface = pygame.transform.scale(base_surface, (int(base_width * scale), int(base_height * scale)))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - int(base_width * scale)) // 2,
                                     (current_height - int(base_height * scale)) // 2))
        pygame.display.flip()
        clock.tick(60)


# ==========================
# Экран победы
# ==========================
def victory_screen(time_str):
    global current_width, current_height, screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.w, event.h
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return
        scale = min(current_width / base_width, current_height / base_height)
        header_size = max(1, int(40 * scale))
        time_size = max(1, int(30 * scale))
        hint_size = max(1, int(20 * scale))

        victory_font = pygame.font.Font(None, header_size)
        time_font = pygame.font.Font(None, time_size)
        small_font = pygame.font.Font(None, hint_size)

        congrat_text = victory_font.render("Вы смогли выбраться.", True, pygame.Color('white'))
        time_text = time_font.render(f"Время прохождения: {time_str}", True, pygame.Color('white'))
        hint_text = small_font.render("Нажмите ENTER или ESC для выхода в главное меню", True, pygame.Color('white'))

        congrat_x = (current_width - congrat_text.get_width()) // 2
        congrat_y = current_height // 3 - congrat_text.get_height() // 2
        time_x = (current_width - time_text.get_width()) // 2
        time_y = current_height // 2 - time_text.get_height() // 2
        hint_x = (current_width - hint_text.get_width()) // 2
        hint_y = (2 * current_height) // 3 - hint_text.get_height() // 2

        screen.fill((0, 0, 0))
        screen.blit(congrat_text, (congrat_x, congrat_y))
        screen.blit(time_text, (time_x, time_y))
        screen.blit(hint_text, (hint_x, hint_y))
        draw_balance(screen)
        pygame.display.flip()
        clock.tick(60)


# ==========================
# Основной игровой цикл
# ==========================
def game_loop(level):
    global balance, current_width, current_height, is_fullscreen, screen, current_character, owned_characters
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('floor.png'),
        'exit': load_image('exit.png'),
        'money': load_image('floor-with-money.png')
    }
    # Используем выбранного персонажа из списка owned_characters
    player_image = load_image(owned_characters[current_character])
    player_image = pygame.transform.scale(player_image, (40, 40))
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    pygame.mixer.music.load('data/music/music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

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

    def generate_level(level_data):
        new_player = None
        exit_coords = None
        for y in range(len(level_data)):
            for x in range(len(level_data[y])):
                if level_data[y][x] == '.':
                    Tile('empty', x, y)
                elif level_data[y][x] == '#':
                    Tile('wall', x, y)
                elif level_data[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                elif level_data[y][x] == 'E':
                    Tile('exit', x, y)
                    exit_coords = (x, y)
                elif level_data[y][x] == 'M':
                    Tile('money', x, y)
        return new_player, exit_coords

    def check_box(x, y):
        if 0 <= y < len(level_map) and 0 <= x < len(level_map[0]):
            return level_map[y][x] != '#'
        return False

    def check_money(x, y):
        if 0 <= y < len(level_map) and 0 <= x < len(level_map[0]) and level_map[y][x] == 'M':
            sound = pygame.mixer.Sound('data/sounds/zvuk-monetyi-na-tverdoy-poverhnosti-4-30628.mp3')
            sound.play()
            for tile in tiles_group:
                pos_x = tile.rect.x // 50
                pos_y = tile.rect.y // 50
                if pos_x == x and pos_y == y:
                    tile.image = load_image('floor.png')
            level_map[y][x] = '.'
            return True
        return False

    level_map = load_level(f'level{level}.txt')
    player, exit_coords = generate_level(level_map)
    move_cooldown = 200
    last_move_time = pygame.time.get_ticks()
    vision_surface = pygame.Surface((5 * tile_width, 5 * tile_height))
    start_time = pygame.time.get_ticks()

    while True:
        victory = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
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
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > move_cooldown:
            if keys[pygame.K_RIGHT]:
                new_x = player.pos_x + 1
                if (new_x, player.pos_y) == exit_coords:
                    victory = True
                elif check_box(new_x, player.pos_y):
                    player.pos_x = new_x
                    player.rect.x += tile_width
                    last_move_time = current_time
                if check_money(new_x, player.pos_y):
                    balance += 1
            if keys[pygame.K_LEFT]:
                new_x = player.pos_x - 1
                if (new_x, player.pos_y) == exit_coords:
                    victory = True
                elif check_box(new_x, player.pos_y):
                    player.pos_x = new_x
                    player.rect.x -= tile_width
                    last_move_time = current_time
                if check_money(new_x, player.pos_y):
                    balance += 1
            if keys[pygame.K_UP]:
                new_y = player.pos_y - 1
                if (player.pos_x, new_y) == exit_coords:
                    victory = True
                elif check_box(player.pos_x, new_y):
                    player.pos_y = new_y
                    player.rect.y -= tile_height
                    last_move_time = current_time
                if check_money(player.pos_x, new_y):
                    balance += 1
            if keys[pygame.K_DOWN]:
                new_y = player.pos_y + 1
                if (player.pos_x, new_y) == exit_coords:
                    victory = True
                elif check_box(player.pos_x, new_y):
                    player.pos_y = new_y
                    player.rect.y += tile_height
                    last_move_time = current_time
                if check_money(player.pos_x, new_y):
                    balance += 1

        elapsed_ms = pygame.time.get_ticks() - start_time
        total_seconds = elapsed_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        if victory:
            pygame.mixer.music.stop()
            balance += 10 * level
            victory_screen(time_str)
            return

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
            if tile.pos_x in (start_x, end_x) or tile.pos_y in (start_y, end_y):
                dx = tile.pos_x - player.pos_x
                dy = tile.pos_y - player.pos_y
                x = (dx + 2) * tile_width
                y = (dy + 2) * tile_height
                dark_coords.append((x, y))
        for (x, y) in set(dark_coords):
            transparent_rect = pygame.Surface((50, 50), pygame.SRCALPHA)
            transparent_rect.fill((0, 0, 0, 196))
            vision_surface.blit(transparent_rect, (x, y))

        player_vision_x = 2 * tile_width + 5
        player_vision_y = 2 * tile_height
        vision_surface.blit(player.image, (player_vision_x, player_vision_y))

        base_surface.fill((0, 0, 0))
        base_surface.blit(vision_surface, (base_width // 2 - vision_surface.get_width() // 2,
                                           base_height // 2 - vision_surface.get_height() // 2))
        font_small = pygame.font.Font(None, 36)
        balance_text = font_small.render(f"Баланс: {balance}", True, pygame.Color('white'))
        base_surface.blit(balance_text, (10, 10))
        time_text = font_small.render(time_str, True, pygame.Color('white'))
        base_surface.blit(time_text, (base_width - time_text.get_width() - 10, 10))

        scale = min(current_width / base_width, current_height / base_height)
        scaled_surface = pygame.transform.scale(base_surface, (int(base_width * scale), int(base_height * scale)))
        screen.fill((0, 0, 0))
        screen.blit(scaled_surface, ((current_width - int(base_width * scale)) // 2,
                                     (current_height - int(base_height * scale)) // 2))
        pygame.display.flip()
        clock.tick(60)



while True:
    option = main_menu()
    if option == "start":
        level = start_screen()
        character_selection()
        game_loop(level)
    elif option == "buy":
        buy_character_screen()
    elif option == "leaderboard":
        leaderboard_screen()
