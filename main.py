import pygame
import sys
from load_functions import load_image, load_level

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

characters = ['mario.png', 'chill-guy.png', 'dog_with_apple.png']
current_character = 0
balance = 0


def start_screen():
    font = pygame.font.Font(None, 50)
    title = font.render("Выбор уровня", True, pygame.Color('white'))
    buttons = [font.render(f"Уровень {i + 1}", True, pygame.Color('white')) for i in range(5)]

    selected = 0

    while True:
        screen.fill((100, 100, 100))
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
        screen.fill((100, 100, 100))
        screen.blit(title, (width // 2 - title.get_width() // 2, 50))

        character_image = load_image(characters[current_character])
        character_image = pygame.transform.scale(character_image, (200, 200))
        screen.blit(character_image, (width // 2 - 100, height // 2 - 100))

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


def game_loop(level):
    global balance

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

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 5)
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

        if player.pos_x == goal_x and player.pos_y == goal_y:
            balance += 10
            character_selection()
            level = start_screen()
            return game_loop(level)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)

        font = pygame.font.Font(None, 36)
        balance_text = font.render(f"Баланс: {balance}", True, pygame.Color('white'))
        screen.blit(balance_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)


level = start_screen()
character_selection()
game_loop(level)