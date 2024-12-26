# import pygame

# class FuelStation:
#     def __init__(self):
#         # Load and scale the fuel station sprite
#         self.sprite = pygame.image.load("images/fuel_station/h2_fuel_station.png").convert_alpha()
#         self.sprite = pygame.transform.scale(self.sprite, (100, 100))
#         self.sprite_type = "fuel_station"
#         self.rect = self.sprite.get_rect()
        
#         # Fixed position on the side of the road
#         self.sprite_x = 2.0  # Positive value puts it on the right side
#         self.z = 0  # Will be set when placed on the road
        
#         # Refueling properties
#         self.refuel_range = 150  # Distance at which player can refuel
#         self.refuel_rate = 2  # How much fuel to add per frame
#         self.cost = 0  # Will be set based on level
#         self.is_unlocked = False
        
#     def can_refuel(self, player_rect, player_pos):
#         """Check if player is in range to refuel"""
#         if not self.is_unlocked:
#             return False
            
#         # Convert road coordinates to screen coordinates for distance check
#         screen_x = self.sprite_x * 100 + player_pos[0]
#         if abs(player_rect.centerx - screen_x) < self.refuel_range:
#             return True
#         return False

# fuel_station.py
import pygame


class FuelStation:
    def __init__(self):
        try:
            self.sprite = pygame.image.load("images/fuel_station/h2_fuel_station.png").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        except:
            # Create a fallback sprite if image is missing
            self.sprite = pygame.Surface((100, 100))
            self.sprite.fill((0, 255, 0))  # Green color as fallback
        
        self.sprite_type = "fuel_station"
        self.refuel_rate = 2.0  # Amount of fuel added per frame while refueling
        self.refuel_range = 300 # Distance at which player can refuel
        self.z = 0  # z-position on the road
        self.sprite_x = 3.0  # Fixed position on right side of road
        self.is_unlocked = True  # Whether this station is available for use
        # Add new attributes for proximity warning
        self.proximity_range = 100  # Lines ahead to check for warning
        self.warning_font = pygame.font.Font("images/joystix.ttf", 30)
    
    def check_fuel_station_proximity(self, lines, current_line_index):
        """
        Check if a fuel station is within the proximity range
        
        Args:
            lines (list): List of all track lines
            current_line_index (int): Current player's line index
        
        Returns:
            bool: True if fuel station is ahead, False otherwise
        """
        for i in range(current_line_index, min(current_line_index + self.proximity_range, len(lines))):
            if lines[i].sprite_type == "fuel_station":
                return True
        return False

    def render_fuel_station_warning(self, screen):
        """
        Render a blinking fuel station warning message
        
        Args:
            screen (pygame.Surface): Game screen to render warning on
        """
        warning_text = self.warning_font.render("FUEL STATION AHEAD", True, "red")
        
        # Position the warning in the center of the screen
        x = (screen.get_width() - warning_text.get_width()) // 2
        y = 150  # Adjust this value to position the warning
        
        # Create a slight blinking effect
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:  # Blink every 500 ms
            screen.blit(warning_text, (x, y))