# import pygame, sys, random, sqlite3
# from pygame.math import Vector2

# class Snake:
#     def __init__(self):
#         self.body = [Vector2(5,10), Vector2(4,10)]
#         self.direction = Vector2(1,0)
#         self.new_block = False
#         self.score = 0

#     def move_snake(self):
#         if self.new_block:
#             body_copy = self.body[:]
#             self.new_block = False
#         else:
#             body_copy = self.body[:-1]
#         body_copy.insert(0, body_copy[0] + self.direction)
#         self.body = body_copy[:]

#     def add_block(self):
#         self.new_block = True
#         self.score += 1

#     def draw_snake(self, surface):
#         for block in self.body:
#              x_pos = int(block.x * cell_size)
#              y_pos = int(block.y * cell_size)
#              block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
#              pygame.draw.rect(surface, pygame.Color('green'), block_rect)

#     def check_collision(self):
#         if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
#             return False
#         for block in self.body[1:]:
#             if block == self.body[0]:
#                 return False
#         return True

#     def game_over(self, name):
#         pygame.quit()
#         self.update_score_in_db(name)
#         sys.exit()

#     def update_score_in_db(self, name):
#         conn = sqlite3.connect('snake_game.db')
#         c = conn.cursor()

#         c.execute("SELECT score FROM player_score WHERE name = ?", (name,))
#         result = c.fetchone()

#         if result is None:
#             c.execute("INSERT INTO player_score (name, score) VALUES (?, ?)", (name, self.score))
#         elif self.score > result[0]:
#             c.execute("UPDATE player_score SET score = ? WHERE name = ?", (self.score, name))

#         conn.commit()
#         conn.close()


# class Snack:
#     def __init__(self):
#         self.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

#     def draw_snack(self, surface):
#         x_pos = int(self.position.x * cell_size)
#         y_pos = int(self.position.y * cell_size)
#         snack_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
#         pygame.draw.ellipse(surface, pygame.Color('red'), snack_rect)

# def draw_text(surface, text, size, color, position):
#     font = pygame.font.SysFont(None, size)
#     text_surface = font.render(text, True, color)
#     rect = text_surface.get_rect(center=position)
#     surface.blit(text_surface, rect)

# name = sys.argv[1]

# pygame.init()
# cell_size = 40
# cell_number = 20
# screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
# clock = pygame.time.Clock()

# snake = Snake()
# snack = Snack()

# SCREEN_UPDATE = pygame.USEREVENT
# pygame.time.set_timer(SCREEN_UPDATE, 150)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             snake.game_over(name)
#         if event.type == SCREEN_UPDATE:
#             snake.move_snake()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and snake.direction.y != 1:
#                 snake.direction = Vector2(0,-1)
#             if event.key == pygame.K_DOWN and snake.direction.y != -1:
#                 snake.direction = Vector2(0,1)
#             if event.key == pygame.K_LEFT and snake.direction.x != 1:
#                 snake.direction = Vector2(-1,0)
#             if event.key == pygame.K_RIGHT and snake.direction.x != -1:
#                 snake.direction = Vector2(1,0)
    
#     if not snake.check_collision():
#         snake.game_over(name)
        
#     if snake.body[0] == snack.position:
#         snake.add_block()
#         snack.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

#     screen.fill(pygame.Color('blue'))
#     snake.draw_snake(screen)
#     snack.draw_snack(screen)
#     draw_text(screen, f'Score: {snake.score}', 25, pygame.Color('white'), (cell_number * cell_size // 2, cell_size // 2))
#     pygame.display.flip()
#     clock.tick(60)


import pygame, sys, random, sqlite3
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.score = 0

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        self.score += 1

    def draw_snake(self, surface):
        for block in self.body:
             x_pos = int(block.x * cell_size)
             y_pos = int(block.y * cell_size)
             block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
             pygame.draw.rect(surface, pygame.Color('dark green'), block_rect)

    def check_collision(self):
        if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
            return False
        for block in self.body[1:]:
            if block == self.body[0]:
                return False
        return True

    def game_over(self, name):
        pygame.quit()
        self.update_score_in_db(name)
        sys.exit()

    def update_score_in_db(self, name):
        conn = sqlite3.connect('snake_game.db')
        c = conn.cursor()

        c.execute("SELECT score FROM player_score WHERE name = ?", (name,))
        result = c.fetchone()

        if result is None:
            c.execute("INSERT INTO player_score (name, score) VALUES (?, ?)", (name, self.score))
        elif self.score > result[0]:
            c.execute("UPDATE player_score SET score = ? WHERE name = ?", (self.score, name))

        conn.commit()
        conn.close()


class Snack:
    def __init__(self):
        self.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

    def draw_snack(self, surface):
        x_pos = int(self.position.x * cell_size)
        y_pos = int(self.position.y * cell_size)
        snack_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.ellipse(surface, pygame.Color('red'), snack_rect)

def draw_text(surface, text, size, color, position):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, rect)

name = sys.argv[1]

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

snake = Snake()
snack = Snack()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


background = pygame.image.load('snake/snakepic.png')
background = pygame.transform.scale(background, (cell_number * cell_size, cell_number * cell_size))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            snake.game_over(name)
        if event.type == SCREEN_UPDATE:
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction.y != 1:
                snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and snake.direction.y != -1:
                snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT and snake.direction.x != 1:
                snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT and snake.direction.x != -1:
                snake.direction = Vector2(1,0)

    if not snake.check_collision():
        snake.game_over(name)

    if snake.body[0] == snack.position:
        snake.add_block()
        snack.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))


    screen.blit(background, (0,0))
    
    snake.draw_snake(screen)
    snack.draw_snack(screen)
    draw_text(screen, f'Score: {snake.score}', 25, pygame.Color('black'), (cell_number * cell_size // 2, cell_size // 2))
    pygame.display.flip()
    clock.tick(60)