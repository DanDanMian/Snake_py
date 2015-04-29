import pygame
import random

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the width and height of each snake segment
segment_width = 17
segment_height = 17
# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = segment_width + segment_margin
y_change = 0

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
 
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
 
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

# Set the title of the window
pygame.display.set_caption('Snake')

snake_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
for i in range(15):
    x = 300 - (segment_width + segment_margin) * i
    y = 40
    segment = Segment(x, y)
    snake_segments.append(segment)
    #snake_list.add(segment)
    all_sprites_list.add(segment)
    
# This represents a block
block = Block(WHITE, segment_width, segment_height)
 
# Set a random location for the block
block.rect.x = random.randrange(screen_width/20)*20
block.rect.y = random.randrange(screen_height/20)*20
 
# Add the block to the list of objects
block_list.add(block)
all_sprites_list.add(block)


clock = pygame.time.Clock()
done = False
eat = False
score = 0

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) *- 1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) *- 1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    if x < 0 or x > screen_width:
        done = True
    if y < 0 or y > screen_height:
        done = True
    else:
        segment = Segment(x, y)

    # Insert new segment into the list
    snake_segments.insert(0, segment)
    all_sprites_list.add(segment)

    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(snake_segments[0], block_list, True)
 
    # Check the list of collisions.
    for segment in blocks_hit_list:
        eat = True
        score += 1
        print(score)
        block = Block(WHITE, segment_width, segment_height)
 
        # Set a random location for the block
        block.rect.x = random.randrange(screen_width/20)*20
        block.rect.y = random.randrange(screen_height/20)*20
 
        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)

    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    if(not eat):
        old_segment = snake_segments.pop()
        all_sprites_list.remove(old_segment)
    eat = False

    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    all_sprites_list.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(5)

print("You Lose")

pygame.quit()

