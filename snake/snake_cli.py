import pygame, sys, random
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
             pygame.draw.rect(surface, pygame.Color('green'), block_rect)

    def check_collision(self):
        if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
            return False
        for block in self.body[1:]:
            if block == self.body[0]:
                return False
        return True

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

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

snake = Snake()
snack = Snack()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
        pygame.quit()
        sys.exit()
        
    if snake.body[0] == snack.position:
        snake.add_block()
        snack.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

    screen.fill(pygame.Color('blue'))
    snake.draw_snake(screen)
    snack.draw_snack(screen)
    draw_text(screen, f'Score: {snake.score}', 25, pygame.Color('white'), (cell_number * cell_size // 2, cell_size // 2))  # Draw score
    pygame.display.flip()
    clock.tick(60)






# import pygame, sys, random
# from pygame.math import Vector2

# class Snake:
#     def __init__(self):
#         self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]

#     def make_snake(self):
#         for block in self.body:
#              x_pos = int(block.x * cell_size)
#              y_pos = int(block.y * cell_size)
#              block_rect = pygame.Rect(x_pos, y_pos, cell_size,cell_size)
#              pygame.draw.rect(screen, pygame.Color('blue'),block_rect)

# class Snack:
#     def __init__(self):
#         self.x = random.randint(0, cell_number - 1)
#         self.y = random.randint(0, cell_number - 1)
#         self.pos = pygame.math.Vector2(self.x, self.y)

#     def make_snack(self):
#         snack_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
#         pygame.draw.rect(screen, pygame.Color('red'), snack_rect)

# pygame.init()
# cell_size = 40
# cell_number = 20
# # Sets screen display at start of game
# screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
# clock = pygame.time.Clock()

# food = Snack()
# snake = Snake()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()    

#     screen.fill((175,215,70))        
#     # Makes elements on the screen
#     food.make_snack()
#     snake.make_snake()
#     pygame.display.update()
#     # Controls the frame rate per sec 60fps is standard
#     clock.tick(60)


# import pygame, sys, random
# from pygame.math import Vector2

# class Snake:
#     def __init__(self):
#         self.body = [Vector2(5,10), Vector2(4,10)]
#         self.direction = Vector2(1,0)
#         self.new_block = False

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

#     def draw_snake(self, surface):
#         for block in self.body:
#             x_pos = int(block.x * cell_size)
#             y_pos = int(block.y * cell_size)
#             block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

#             # Paint head blue
#             if block == self.body[0]:
#                 pygame.draw.rect(surface, (0, 0, 255), block_rect)
#             # Paint rest of body green
#             else:
#                 pygame.draw.rect(surface, (0, 255, 0), block_rect)

#     def check_collision(self):
#         if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
#             return False
#         for block in self.body[1:]:
#             if block == self.body[0]:
#                 return False
#         return True

# class Snack:
#     def __init__(self):
#         self.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

#     def draw_snack(self, surface):
#         x_pos = int(self.position.x * cell_size)
#         y_pos = int(self.position.y * cell_size)
#         snack_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
#         pygame.draw.rect(surface, (183, 111, 122), snack_rect)

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
#             pygame.quit()
#             sys.exit()
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
#         pygame.quit()
#         sys.exit()
        
#     if snake.body[0] == snack.position:
#         snake.add_block()
#         snack.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        
#     screen.fill((175,215,70))
#     snake.draw_snake(screen)
#     snack.draw_snack(screen)
#     pygame.display.update()
#     clock.tick(60)