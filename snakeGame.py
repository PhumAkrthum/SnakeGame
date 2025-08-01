import pygame
import sys
import random

# Global variables
# Board / Field
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 48099

GRIDSIZE = 20 
GRID_WIDTH = SCREEN_HEIGHT / GRIDSIZE
GRID_HEIGHT = SCREEN_WIDTH / GRIDSIZE

# Possible movements of the snake
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


# Class represents moving snake
class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))] # List that keeps track of the building blocks of the snake
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        self.score = 0


    def get_head_position(self):
        '''
        Return position of the head of the snake
        '''
        return self.positions[0]


    def turn(self, point):
        '''
        Move snake
        '''
        # If snake starts
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        # other wise only 3 moving options
        else:
            self.direction = point

    def move(self):
        '''
        Calculate new position of snake given the current position and the 
        direction of the snake
        ''' 
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)

        # If len of snake > 2 & snake head overlaps with other part of the snake reset
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        # otherwise add new head position to positions list and pop last element
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def reset(self):
        '''
        Restore to default values
        '''
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT]) 
        self.score = 0


    def draw(self, surface):
        '''
        Draw a block for each x & y position of the snake
        '''
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)


    def handle_keys(self):
        '''
        Handle user inputs from keyboard
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)


# Class represents moving food block 
class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()


    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)


    def draw(self, surface):
        '''
        Draw food object on screen surface
        '''
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)


# DrawGrid function
def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for  x in range(0, int(GRID_WIDTH)):
            
            # Make surface a checkered background
            if (x + y) % 2 == 0:
                r = pygame.Rect((x * GRIDSIZE, y * GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x * GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)


# Main game loop
def main():
    # Create screen & game environment
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    # Draw screen & surface that gets updated after every action performed
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 16)

    while(True):
        # Handle events in the snake game
        
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()

        # Check if head position == food position
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)

        # After action in game update screen & surface
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        pygame.display.update()

if __name__ == '__main__':
    main()