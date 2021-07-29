"""
PyGame Simulation of Projectile Motion
~ Daniel Cortild, 29 July 2021
"""

# Libraries
from math import sqrt, atan, pi, cos, sin
import pygame

# Constants
WIDTH = 1200
HEIGHT = 500

RADIUS = 10

BLACK = (0, 0, 0)
GRAY = (64, 64, 64)
WHITE = (255, 255, 255)

START_X = WIDTH / 2
START_Y = HEIGHT - RADIUS - 1

# Ball Class
class Ball:
  def __init__(self, x, y, radius, color):
    """Initialize the Ball instance
    Params
      x: X position of ball
      y: Y position of ball
      radius: Radius of ball
      color: Color of ball
    """
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color

  def draw(self, window):
    """Draw the ball
    Params
      window: Window to draw on (PyGame Window Object)
    """
    pygame.draw.circle(window, BLACK, (self.x, self.y), self.radius)
    pygame.draw.circle(window, self.color, (self.x, self.y), self.radius - 1)

  @staticmethod
  def next_position(start_x, start_y, power, angle, time):
    """ Compute the next x and y positions of the ball
    Params
      start_x: Starting x position of the ball (Float)
      start_y: Starting y position of the ball (Float)
      power: Power of the shot (Float)
      angle: Angle of the shot (Float)
      time: Timestamp we want to compute the positions for (Float)
    Returns
      next_x: Next x position
      next_y: Next y position
    """
    velocity_x = cos(angle) * power
    velocity_y = sin(angle) * power

    distance_x = velocity_x * time
    distance_y = velocity_y * time - 4.9 * time ** 2

    next_x = start_x + distance_x
    next_y = start_y - distance_y

    return next_x, next_y

def draw_line(window, ball, shooting):
  """ Draw a line between the ball and the mouse when not shooting
  Params
    window: Window to draw on (PyGame Window Object)
    ball: Ball to draw (Ball Object)
    shooting: Whether we are shooting or not (Boolean)
  """
  if not shooting:
    pygame.draw.line(window, WHITE, (ball.x, ball.y), pygame.mouse.get_pos())

def draw_window(window, ball, shooting):
  """ Draw objects on window
  Params
    window: Window to draw on (PyGame Window Object)
    ball: Ball to draw (Ball Object)
    shooting: Whether we are shooting or not (Boolean)
  """
  window.fill(GRAY)
  ball.draw(window)
  draw_line(window, ball, shooting)
  pygame.display.update()

def get_power(line):
  """ Get power depending on the line between the ball and the mouse
  Params
    line: Line between ball and mouse (Array of pairs)
  Returns
    power: Power of the shot (Float)
  """
  return sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 8

def get_angle(line):
  """ Get angle depending on the line between the ball and the mouse
  Params
    line: Line between ball and mouse (Array of pairs)
  Returns
    angle: Angle of the shot (Float)
  """
  x = line[0][0]
  y = line[0][1]

  mouse_x = line[1][0]
  mouse_y = line[1][1]

  if mouse_x != x:
    angle = atan((mouse_y - y) / (mouse_x - x))
  else:
    angle = pi / 2

  if x < mouse_x and y > mouse_y:
    angle = abs(angle)
  elif x > mouse_x and y > mouse_y:
    angle = pi - angle
  elif x > mouse_x and y < mouse_y:
    angle = pi + abs(angle)
  elif x < mouse_x and y < mouse_y:
    angle = 2 * pi - angle

  return angle

# Initialize window, clock and ball object
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ball = Ball(START_X, START_Y, RADIUS, WHITE)

# Data about the ball
shooting = False
start_x = 0
start_y = 0
time = 0
power = 0
angle = 0

# Run the code until a QUIT event
while True:
  clock.tick(200)
  
  # Move the ball (Or stop it) if shooting
  if shooting:
    if ball.y <= HEIGHT - ball.radius:
      time += 0.05
      position = ball.next_position(start_x, start_y, power, angle, time)
      ball.x = position[0]
      ball.y = position[1]
    else:
      shooting = False
      ball.y = START_Y

  draw_window(window, ball, shooting)

  # Exit game if QUIT, start shot if MOUSEBUTTONDOWN
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      if not shooting:
        shooting = True
        line = [(ball.x, ball.y), pygame.mouse.get_pos()]
        start_x = ball.x
        start_y = ball.y
        time = 0
        power = get_power(line)
        angle = get_angle(line)
