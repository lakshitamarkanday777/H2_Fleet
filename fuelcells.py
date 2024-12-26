import pygame
import random

class FuelCell:
    def __init__(self):
        # It initializes the fuelcell object.
        # sprite (pygame surface): it is for visual representation of the fuel cell, as a image(50*50)
        self.sprite = pygame.image.load("images/H2_cell-removebg.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        self.sprite_type = "fuel_cell" # sprite_type(str): This string identifies the sprite as a fuel cell.
        # rect (pygame.Rect): The rectangle around the fuel cell sprite is used for positioning and collision detection.
        self.rect = self.sprite.get_rect()
        # the value of the unit cell is set to one.
        self.value = 1 
        self.sprite_x = random.uniform(-1.5, 1.5)  # Random x position on the road, ranging from -1.5 to 1.5.
        self.z = 0  # z position on the road

    def draw(self, screen, player_rect, pos):
        ''' It draws the fuel cell on the screen and checks for the collision
        Screen: the fuel cell will be drawn on game screen.
        player_rect: The rectangle representing the player's vehicle. it is used to detect collision.
        pos: It is an tuple containing the player's current position (x, y) to adjust fuel cell position.
        return: it will return true if the fuel cell collides with the player's vehicle, otherwise, it will return false.'''
        # Update the position based on the z value
        self.rect.topleft = (self.sprite_x * 100 + pos[0], self.z)  # Example calculation
        screen.blit(self.sprite, self.rect) # draw the furl cells on screen
        return self.rect.colliderect(player_rect)  # Checking collision with player
        
def generate_fuel_cells(num_cells, road_length):
    ''' It will generate a list of fuel cells.
    num_cells: the number of fuel cells to generate.
    road_lenght: the total length of the road, where the fuel cells will be distributed.
    returns:  it will return the list of fuel cell objects based on road length.'''
    fuel_cells = []
    for i in range(num_cells):
        fuel_cell = FuelCell()
        fuel_cell.z = i * (road_length / num_cells)  # Spacing them out along the road
        fuel_cells.append(fuel_cell)
    return fuel_cells
# red_fuel_cell.py


class RedFuelCell:
    def __init__(self):
        try:
            self.sprite = pygame.image.load("images/h2_fuelcells/partners.png").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (40, 40))
        except:
            # Fallback if image not found
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 0))  # Red color
        
        self.sprite_x = 0
        
        # Load a single message image
        self.message = pygame.image.load("images/message_box/message_1.png").convert_alpha()
        # Optionally scale the message image if needed
        self.message = pygame.transform.scale(self.message, (700, 550))  # Example size
        # Add total red cells tracking
        
    def get_message(self):
        """
        Return the single message image
        """
        return self.message

    def spawn_red_fuel_cell(self, lines, fuel_cell_dist=5):
        """
        Spawn red fuel cells on the lines
        """
        for i, line in enumerate(lines):
            if i % fuel_cell_dist == 0 and random.random() < 0.1:  # 10% chance of adding a red fuel cell
                self.sprite_x = random.uniform(-1.5, 1.5)
                line.sprite = self.sprite
                line.sprite_type = "red_cell"
