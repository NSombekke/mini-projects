import pygame
pygame.init()

import random

class Snake:
  def __init__(self, window_size, block_size, head_color, body_color):
    self.window_size = window_size
    self.block_size = block_size
    self.head_color = head_color
    self.body_color = body_color
    self.body = [(window_size[0] // 2, window_size[1] // 2), (window_size[0] // 2 - block_size, window_size[1] // 2)]
    self.length = 2
    self.dx = block_size
    self.dy = 0
  
  def change_direction(self, dx, dy):
    if dx != -self.dx and dy != -self.dy:
      self.dx = dx
      self.dy = dy
  
  def move(self):
    new_head = (self.body[0][0] + self.dx, self.body[0][1] + self.dy)
    self.body = [new_head, *self.body[:-1]] # Add new head and remove last part of body
  
  def grow(self):
    self.length += 1
    self.body.append(self.body[-1])
    
class Food:
  def __init__(self, pos, color):
    self.pos = pos
    self.color = color
  
class Screen:
  def __init__(self, window_size, block_size, bg_color, grid_color):
    self.window_size = window_size
    self.block_size = block_size
    self.bg_color = bg_color
    self.grid_color = grid_color
    self.display = pygame.display.set_mode(window_size)
  
  def draw_background(self):
    self.display.fill(self.bg_color)
    
  def draw_grid(self):
    for x in range(0, self.window_size[0], self.block_size):
      for y in range(0, self.window_size[1], self.block_size):
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(self.display, self.grid_color, rect, 1)
        
  def draw_snake(self, snake):
    for i, part in enumerate(snake.body):
      rect = pygame.Rect(part[0], part[1], self.block_size, self.block_size)
      if i == 0:
        pygame.draw.rect(self.display, snake.head_color, rect)
      else:
        pygame.draw.rect(self.display, snake.body_color, rect)
  
  def draw_food(self, food):
    rect = pygame.Rect(food.pos[0], food.pos[1], self.block_size, self.block_size)
    pygame.draw.rect(self.display, food.color, rect)

class Game:
  # Colors
  BLACK = pygame.Color(0, 0, 0)
  WHITE = pygame.Color(255, 255, 255)
  RED = pygame.Color(255, 0, 0)
  LIGHT_GREEN = pygame.Color(0, 240, 0)
  DARK_GREEN = pygame.Color(0, 100, 0)
  BLUE = pygame.Color(0, 0, 255)
  def __init__(self, window_size, block_size):
    assert window_size[0] % block_size == 0, "Window width must be a multiple of block size."
    assert window_size[1] % block_size == 0, "Window height must be a multiple of block size."
    self.window_size = window_size
    self.block_size = block_size
    self.screen = Screen(window_size, block_size, self.BLACK, self.WHITE)
    self.clock = pygame.time.Clock()
    self.snake = Snake(window_size, block_size, self.LIGHT_GREEN, self.DARK_GREEN)
    self.running = True
    self.block_pos = [(x, y) for x in range(0, window_size[0], block_size) for y in range(0, window_size[1], block_size)]
    self.food = Food(random.choice([pos for pos in self.block_pos if pos not in self.snake.body]), self.RED)
    self.main()
    
  def main(self):
    while self.running:
      changed_direction = False
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        if event.type == pygame.KEYDOWN:
          if not changed_direction:
            if event.key == pygame.K_LEFT:
              self.snake.change_direction(-self.block_size, 0)
              changed_direction = True
            elif event.key == pygame.K_RIGHT:
              self.snake.change_direction(self.block_size, 0)
              changed_direction = True
            elif event.key == pygame.K_UP:
              self.snake.change_direction(0, -self.block_size)
              changed_direction = True
            elif event.key == pygame.K_DOWN:
              self.snake.change_direction(0, self.block_size)
              changed_direction = True
      
      # Move
      self.snake.move()
      
      # Check collision
      # Snake collides with itself
      if self.snake.body[0] in self.snake.body[1:]:
        self.running = False
      # Snake collides with wall
      if self.snake.body[0][0] < 0 or self.snake.body[0][0] >= self.window_size[0] or self.snake.body[0][1] < 0 or self.snake.body[0][1] >= self.window_size[1]:
        self.running = False
      # Snake collides with food
      if self.snake.body[0] == self.food.pos:
        self.snake.grow()
        self.food = Food(random.choice([pos for pos in self.block_pos if pos not in self.snake.body]), self.RED)
          
      # Draw
      self.screen.draw_background()
      self.screen.draw_grid()
      self.screen.draw_snake(self.snake)
      self.screen.draw_food(self.food)
            
      pygame.display.flip()
      self.clock.tick(8)
      
    pygame.quit()

if __name__ == "__main__":
  # Game settings
  WINDOW_SIZE = (400, 400)
  BLOCK_SIZE = 40
  Game(WINDOW_SIZE, BLOCK_SIZE)
