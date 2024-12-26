import pygame

import sys
class MaintenanceCentre:
    def __init__(self):
        # Load maintenance centre image
        try:
            self.sprite = pygame.image.load("images/fuel_station/maintenance_1.jpg").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        except:
            print("Warning: Maintenance centre image not found")
            self.sprite = pygame.Surface((100, 100))
            self.sprite.fill((0, 255, 0))  # Green placeholder
        
        # Positioning on the road
        self.sprite_x = -2.0
    
    def check_maintenance_centre_proximity(self, lines, start_pos):
        """
        Check if a maintenance centre is near the player
        """
        for i in range(start_pos, start_pos + 20):  # Check next 20 segments
            if i < len(lines) and lines[i].sprite_type == "maintenance_centre":
                return True
        return False
    
    def render_maintenance_centre_warning(self, screen):
        """
        Render a warning that maintenance centre is nearby
        """
        warning_font = pygame.font.Font("images/joystix.ttf", 24)
        warning_text = warning_font.render("Maintenance Centre Nearby! Press ENTER", True, (255, 0, 0))
        
        # Position the warning at the top center of the screen
        warning_rect = warning_text.get_rect(
            center=(screen.get_width() // 2, 50)
        )
        screen.blit(warning_text, warning_rect)

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MaintenanceCentreMenu:
    def __init__(self, screen, game):
        # Ensure pygame is initialized
        if not pygame.get_init():
            pygame.init()

        self.screen = screen
        self.game = game
        
        # Create fonts
        try:
            self.title_font = pygame.font.Font("images/joystix.ttf", 36)
            self.button_font = pygame.font.Font("images/joystix.ttf", 24)
        except Exception as e:
            print(f"Font loading error: {e}")
            # Fallback to default font
            self.title_font = pygame.font.Font(None, 36)
            self.button_font = pygame.font.Font(None, 24)

    def show_maintenance_centre(self):
        # Ensure pygame.Rect is available
        Rect = pygame.Rect  # Create a local reference to pygame.Rect

        # Pause the game
        original_speed = self.game.speed
        self.game.speed = 0

        # Create maintenance centre background
        menu_width = 600
        menu_height = 400
        menu_surface = pygame.Surface((menu_width, menu_height))
        menu_surface.fill((50, 50, 50))  # Dark gray background

        # Upgrade options
        upgrades = [
            {
                'name': 'Vehicle Health',
                'description': 'Increase maximum health',
                'cost': 1,
                'current_level': 1,
                'upgrade_func': lambda: self.game.health_bar.increase_max_health(10)
            },
            # ... other upgrades ...
        ]

        # Button rects for click detection
        button_rects = []

        # Maintenance centre loop
        maintenance_active = True
        while maintenance_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # Exit maintenance centre
                    if event.key == pygame.K_ESCAPE:
                        maintenance_active = False
                        self.game.speed = original_speed

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Adjust for menu position on screen
                    screen_center_x = (self.screen.get_width() - menu_width) // 2
                    screen_center_y = (self.screen.get_height() - menu_height) // 2
                    
                    for i, rect in enumerate(button_rects):
                        adjusted_rect = rect.move(screen_center_x, screen_center_y)
                        if adjusted_rect.collidepoint(mouse_pos):
                            # Handle upgrade
                            upgrade = upgrades[i]
                            if self.game.red_fuel_cells_collected >= upgrade['cost']:
                                self.game.red_fuel_cells_collected -= upgrade['cost']
                                upgrade['upgrade_func']()
                                upgrade['current_level'] += 1
                                print(f"Upgraded {upgrade['name']} to level {upgrade['current_level']}")
                            else:
                                print("Not enough red cells to upgrade!")

            # Clear screen and draw maintenance menu
            self.screen.fill((0, 0, 0))  # Black background

            # Draw maintenance menu surface centered
            menu_rect = menu_surface.get_rect(
                center=(self.screen.get_width()//2, self.screen.get_height()//2)
            )
            self.screen.blit(menu_surface, menu_rect)

            # Draw title
            title = self.title_font.render("Maintenance Centre", True, (255, 255, 255))
            title_rect = title.get_rect(centerx=menu_width//2, top=20)
            title_pos = title_rect.move(
                (self.screen.get_width() - menu_width)//2, 
                (self.screen.get_height() - menu_height)//2
            )
            self.screen.blit(title, title_pos)

            # Draw buttons
            button_rects.clear()  # Clear previous rects
            for i, upgrade in enumerate(upgrades):
                # Use local Rect reference
                button_rect = Rect(
                    50, 
                    100 + i * 70, 
                    menu_width - 100, 
                    50
                )
                button_rects.append(button_rect)
                
                # Adjust rect position
                adjusted_rect = button_rect.move(
                    (self.screen.get_width() - menu_width)//2, 
                    (self.screen.get_height() - menu_height)//2
                )
                
                # Button background
                pygame.draw.rect(self.screen, (100, 100, 100), adjusted_rect)
                
                # Button text
                button_text = self.button_font.render(
                    f"{upgrade['name']} (Lv{upgrade['current_level']}) - {upgrade['cost']} Red Cells", 
                    True, 
                    (255, 255, 255)
                )
                text_rect = button_text.get_rect(center=adjusted_rect.center)
                self.screen.blit(button_text, text_rect)

            # Display current red cell count
            red_cell_text = self.button_font.render(
                f"Red Cells: {self.game.red_fuel_cells_collected}", 
                True, 
                (255, 0, 0)
            )
            red_cell_rect = red_cell_text.get_rect(
                topright=(self.screen.get_width() - 50, 50)
            )
            self.screen.blit(red_cell_text, red_cell_rect)

            pygame.display.flip()

        # Resume game
        self.game.speed = original_speed