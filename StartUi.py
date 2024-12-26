# start_ui.py
import pygame
import sys
import time
import math
from settings import SCREEN_HEIGHT,SCREEN_WIDTH
from pygame import Rect
pygame.init()
class StartUI:
    def __init__(self, screen_width, screen_height):
        # Ensure Pygame is fully initialized
        if not pygame.get_init():
            pygame.init()

        # Ensure display is initialized
        if not pygame.display.get_init():
            pygame.display.init()

        # Performance-focused screen setup
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        # Ensure screen is created before other initializations
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        pygame.display.set_caption("H2 Fleet Revolution")

        # Defensive initialization of Pygame modules
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception as e:
            print(f"Mixer initialization error: {e}")

        # Efficient color palette
        self.COLORS = {
            'BACKGROUND': (20, 30, 40),
            'TITLE': (0, 105, 255),
            'BUTTON': (52, 152, 219),
            'BUTTON_HOVER': (41, 128, 185),
            'TEXT': (255, 255, 255)
        }

        # Efficient font loading
        self.fonts = self._load_fonts()

        # Preload assets
        self.assets = self._preload_assets()

        # Defensive button creation with error handling
        try:
            self.buttons = self._create_buttons()
        except Exception as e:
            print(f"Button creation error: {e}")
            self.buttons = []  # Fallback to empty list

        # Load background music with error handling
        try:
            pygame.mixer.music.load("sound/game_bg/sound_1.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Music loading error: {e}")

        # Load sound effect with error handling
        try:
            self.button_click_sound = pygame.mixer.Sound("sound/click/click.mp3")
        except Exception as e:
            print(f"Sound effect loading error: {e}")
            self.button_click_sound = None

        # Performance optimization
        self.clock = pygame.time.Clock()
        self.is_first_render = True

    def _load_fonts(self):
        """Efficiently load fonts with minimal overhead"""
        try:
            return {
                'title': pygame.font.Font("images/joystix.ttf", 80),
                'button': pygame.font.Font("images/joystix.ttf", 40),
                'subtitle': pygame.font.Font("images/joystix.ttf", 30)
            }
        except:
            # Fallback to system fonts
            return {
                'title': pygame.font.SysFont('Arial', 80),
                'button': pygame.font.SysFont('Arial', 40),
                'subtitle': pygame.font.SysFont('Arial', 30)
            }

    def _preload_assets(self):
        """Efficiently preload and cache assets"""
        assets = {
            'background': None,
            'car': None
        }

        # Efficient image loading
        try:
            background = pygame.image.load("images/level1/My_Bg2_edited.png").convert()
            assets['background'] = pygame.transform.scale(
                background, 
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            )
        except:
            print("Background image not found")

        try:
            car = pygame.image.load("images/player.png").convert_alpha()
            assets['car'] = pygame.transform.scale(car, (300, 150))
        except:
            print("Car image not found")

        return assets

    def _create_buttons(self):
        """Create buttons with extensive error checking and logging"""
        try:
            # Double-check Pygame Rect is available
            if not hasattr(pygame, 'Rect'):
                raise RuntimeError("pygame.Rect is not available")
            
            # Verify screen dimensions are valid
            if self.SCREEN_WIDTH <= 0 or self.SCREEN_HEIGHT <= 0:
                raise ValueError("Invalid screen dimensions")
        
            # Create buttons with a Button class or dictionary representation
            buttons = [
                {
                    'text': 'Start',
                    'rect': pygame.Rect(
                        self.SCREEN_WIDTH // 2 - 90, 
                        self.SCREEN_HEIGHT // 2, 
                        170, 
                        60
                    ),
                    'action': self.start_game
                },
                {
                    'text': 'Instructions',
                    'rect': pygame.Rect(
                        self.SCREEN_WIDTH // 2 - 200, 
                        self.SCREEN_HEIGHT // 2 + 100, 
                        400, 
                        60
                    ),
                    'action': self.show_instructions
                },
                {
                    'text': 'Quit',
                    'rect': pygame.Rect(
                        self.SCREEN_WIDTH // 2 - 88, 
                        self.SCREEN_HEIGHT // 2 + 200, 
                        150, 
                        60
                    ),
                    'action': self.quit_game
                }
            ]
    
            # Validate button creation
            for button in buttons:
                if not isinstance(button['rect'], pygame.Rect):
                    print(f"Warning: Invalid rect for button {button['text']}")
                if not callable(button['action']):
                    print(f"Warning: Invalid action for button {button['text']}")
    
            return buttons
        
        except Exception as e:
            print(f"Button creation error in _create_buttons: {e}")
            import traceback
            traceback.print_exc()
            return []  # Return an empty list instead of None

    def render_background(self):
        """Efficiently render background"""
        if self.assets['background']:
            self.screen.blit(self.assets['background'], (0, 0))
        else:
            self.screen.fill(self.COLORS['BACKGROUND'])

    def render_title(self):
        """Efficient title rendering"""
        title = self.fonts['title'].render("H2 Fleet ", True, self.COLORS['TITLE'])
        title_rect = title.get_rect(centerx=self.SCREEN_WIDTH // 2, top=50)
        self.screen.blit(title, title_rect)

    def render_buttons(self):
        """Optimized button rendering with hover effects"""
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            # Determine button color based on hover
            color = (self.COLORS['BUTTON_HOVER'] 
                     if button['rect'].collidepoint(mouse_pos) 
                     else self.COLORS['BUTTON'])
            
            # Render button
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=10)
            
            # Render button text
            text = self.fonts['button'].render(
                button['text'], 
                True, 
                self.COLORS['TEXT']
            )
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def start_game(self):
        """Start game method"""
        return True

    def show_instructions(self):
        """Show game instructions"""
        instructions_screen = True
        while instructions_screen:
            self.screen.fill(self.COLORS['BACKGROUND'])
            
            # Render instruction text
            instructions = [
                "How to Play:",
                "Arrow Keys: Control Car",
                "UP: Accelerate",
                "DOWN: Brake",
                "LEFT/RIGHT: Steer",
                "Collect Fuel Cells",
                "Refuel at Stations",
                "",
                "Press ESC to Return"
            ]
            
            for i, line in enumerate(instructions):
                text = self.fonts['subtitle'].render(
                    line, 
                    True, 
                    self.COLORS['TITLE']
                )
                text_rect = text.get_rect(
                    centerx=self.SCREEN_WIDTH // 2, 
                    top=100 + i*50
                )
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        instructions_screen = False

    def quit_game(self):
        """Quit game method"""
        pygame.quit()
        sys.exit()

    def run(self):
        """Main menu loop"""
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            result = button['action']()
                            if result:  # If start_game returns True
                                return True

            # Render
            self.render_background()
            self.render_title()
            self.render_buttons()

            # Optional: Render car image
            if self.assets['car']:
                car_x = self.SCREEN_WIDTH - self.assets['car'].get_width() - 50
                car_y = self.SCREEN_HEIGHT - self.assets['car'].get_height() - 50
                self.screen.blit(self.assets['car'], (car_x, car_y))

            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS


class RepairMenu:
    def __init__(self, screen,game):
        self.screen = screen
        self.font = pygame.font.Font("images/joystix.ttf", 20)
        self.title_font = pygame.font.Font("images/joystix.ttf", 36)
        
        # Menu options
        self.options = [
            "Repair Body",
            "Upgrade Engine",
            "Improve Fuel Efficiency", 
            "Add Armor Plating",
            "Enhance Suspension"
        ]
        
        # Prices for upgrades
        self.prices = [
            3,  # Repair Body
            5,  # Upgrade Engine
            6,  # Improve Fuel Efficiency
            6,  # Add Armor Plating
            12,  # Enhance Suspension
        ]
        
        # Current selections and states
        self.selected_index = 0
        self.game = game
        self.is_active = False
        self.upgrade_sound = pygame.mixer.Sound("sound/centre_upgrade/in-game-level-uptype-2-230567.mp3")  
        # Error sound (not enough red cells)
        self.error_sound = pygame.mixer.Sound("sound/centre_upgrade/error.mp3")
        self.red_cell_image = pygame.image.load("images/h2_fuelcells/partners.png").convert_alpha()
        self.red_cell_image = pygame.transform.scale(self.red_cell_image, (70, 70))
        # Load navigation sound
        # self.navigation_sound = pygame.mixer.Sound("sound/centre_upgrade/windows-error-sound-effect-35894.mp3")  # Update with your sound file path
    def draw(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title = self.title_font.render("Repair & Upgrade Workshop", True, (255, 255, 255))
        title_rect = title.get_rect(centerx=SCREEN_WIDTH//2, top=100)
        self.screen.blit(title, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_index else (150, 150, 150)
            
            # Render option text
            text = self.font.render(f"{option} - ${self.prices[i]}", True, color)
            text_rect = text.get_rect(
                centerx=SCREEN_WIDTH//2, 
                top=250 + i * 50
            )
            
            # Optional: Draw selection indicator
            if i == self.selected_index:
                pygame.draw.rect(self.screen, (255, 255, 0), text_rect.inflate(20, 10), 2)
            
            self.screen.blit(text, text_rect)
        
        # Instructions
        instructions = self.font.render("Use UP/DOWN to navigate, ENTER to select, ESC to exit", True, (255, 255, 255))
        instructions_rect = instructions.get_rect(centerx=SCREEN_WIDTH//2, bottom=SCREEN_HEIGHT-100)
        self.screen.blit(instructions, instructions_rect)
        
        # Draw total red cells with image
        red_cell_x = 10  # Adjust x position as needed
        red_cell_y = 200  # Adjust y position as needed
        # Blit the red cell image
        self.screen.blit(self.red_cell_image, (red_cell_x, red_cell_y))
        # Render the text for total red cells
        total_red_cells_text = f"- {self.game.total_red_cells_collected}"
        total_red_cell_surface = self.font.render(total_red_cells_text, True, (255, 0, 0))  # Red color
        # Position the text next to the image
        text_rect = total_red_cell_surface.get_rect(topleft=(red_cell_x + self.red_cell_image.get_width() + 5, red_cell_y+20))
        self.screen.blit(total_red_cell_surface, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # self.navigation_sound.play()
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                # self.navigation_sound.play()
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()
                # self.navigation_sound.play()
            elif event.key == pygame.K_ESCAPE:
                # self.navigation_sound.play()
                self.is_active = False
    
    def select_option(self):
        """
        Handle the selection of a menu option.
        In a real implementation, you'd pass the game state and apply actual upgrades.
        """
        # Check if player has enough red cells
        if self.game.total_red_cells_collected >= self.prices[self.selected_index]:
            # Deduct red cells
            self.game.total_red_cells_collected -= self.prices[self.selected_index]
            # Play upgrade sound if available
            if self.upgrade_sound:
                self.upgrade_sound.play()
            # Apply upgrade based on selected option
            selected_option = self.options[self.selected_index]
            
            # Implement specific upgrades
            if selected_option == "Repair Body":
                # Restore health
                self.game.health_bar.heal(self.game.health_bar.max_health) 
                print("Body repaired to full health!")
            
            elif selected_option == "Upgrade Engine":
                # Increase max speed
                self.game.max_speed = round(min(self.game.max_speed * 1.1, 150))  # 10% speed increase, cap at 150
                print(f"Engine upgraded. New max speed: {self.game.max_speed}")
            
            elif selected_option == "Improve Fuel Efficiency":
                # Reduce fuel consumption rate
                self.game.fuel_consumption_rate *= 0.9  # 10% reduction
                print(f"Fuel efficiency improved. New consumption rate: {self.game.fuel_consumption_rate}")
            
            elif selected_option == "Add Armor Plating":
                # Increase max health
                self.game.health_bar.max_health *= 1.2  # 20% health increase
                self.game.health_bar.heal(self.game.health_bar.max_health) 
                print(f"Armor plating added. New max health: {self.game.health_bar.max_health}")
            
            # elif selected_option == "Enhance Suspension":
            #     # Improve handling (reduce curve impact)
            #     self.game.curve_sensitivity *= 0.9  # 10% reduction in curve sensitivity
            #     print(f"Suspension enhanced. New curve sensitivity: {self.game.curve_sensitivity}")
            
        else:
            # Not enough red cells
            if self.error_sound:
                self.error_sound.play()
            print("Not enough red cells for this upgrade!")
        
    def toggle(self):
        """Toggle the menu's active state"""
        self.is_active = not self.is_active
        self.selected_index = 0
import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.fuel_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        self.h2_font= pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        self.speed_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        self.level_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        # Load the fuel cell image
        self.fuel_cell_image = pygame.image.load("images/h2_fuelcells/H2_cell-removebg.png").convert_alpha()  # Adjust the path as needed
        self.fuel_cell_image = pygame.transform.scale(self.fuel_cell_image, (80, 80))  # Resize if necessary
        self.red_cell_image = pygame.image.load("images/h2_fuelcells/partners.png")  # Load your red cell image
        self.red_cell_image = pygame.transform.scale(self.red_cell_image, (60, 60))  # Optionally scale the image
        self.red_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
    def draw_transparent_box(self, x, y, width, height, color, alpha):
        box_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Enable per-pixel alpha
        box_surface.fill((color[0], color[1], color[2], alpha))  # Fill the surface with the color and alpha
        self.screen.blit(box_surface, (x, y))

    def draw_fuel_display(self, fuel_count,game):
        x_position = SCREEN_WIDTH - 150  # 10 pixels from the right edge
        y_position = 70  # 10 pixels from the top
        box_width = 50
        box_height = 50
        box_color = (0, 0, 180)  # Blue color
        box_alpha = 128  # 50% transparent

        self.draw_transparent_box(x_position + 80, y_position + 20, box_width, box_height, box_color, box_alpha)

        # Draw the fuel cell image
        self.screen.blit(self.fuel_cell_image, (x_position + 10, y_position + 10))  # Position the image with padding
        # Draw the red cell image
        self.screen.blit(self.red_cell_image, (x_position + 10, y_position + 90))  # Position the image with padding
        # Create the fuel text with a dash
        fuel_text = self.fuel_font.render(f" -{fuel_count}", True, (255, 255, 255))  # White text
        # Position the text next to the image, adjusting for the image size
        self.screen.blit(fuel_text, (x_position + 70, y_position + 30))  # Position the text next to the image
        
        # Now draw the red cell counter below the fuel display
        red_cell_y_position = y_position + box_height + 60  # 20 pixels below the fuel display
        red_cell_count_text = f"- {game.red_fuel_cells_collected}/5"  # Example text for red cells

        # Create text surface for red cell count
        red_cell_surface = self.red_font.render(
            red_cell_count_text, 
            True, 
            (255, 255, 255)  # White color
        )

        # Position the text for red cell count
        red_cell_text_rect = red_cell_surface.get_rect(
            topleft=(x_position + 60, red_cell_y_position)  # Adjust x_position as needed
        )

        # Draw the red cell count text
        self.screen.blit(red_cell_surface, red_cell_text_rect)
    def draw_speed_display(self, speed):
        x_position = 10  # 10 pixels from the left edge
        y_position = 130  # 10 pixels from the top
        box_width = 270
        box_height = 50
        box_color = (0, 0, 180)  # Blue color
        box_alpha = 128  # 50% transparent

        self.draw_transparent_box(x_position, y_position, box_width, box_height, box_color, box_alpha)

        speed_text = self.speed_font.render(f"Speed: {int(speed)} Km/hr", True, (255, 255, 255))  # White text
        self.screen.blit(speed_text, (x_position + 10, y_position + 10))  # Add some padding

    def draw_level_display(self, current_level):
        x_position = 10
        y_position = 70
        box_width = 200
        box_height = 50
        box_color = (0, 0, 180)  # Blue color
        box_alpha = 120  # 50% transparent

        self.draw_transparent_box(x_position, y_position, box_width, box_height, box_color, box_alpha)

        current_level_text = f"Level: {current_level + 1}"  # Levels are 0-indexed
        level_surface = self.level_font.render(current_level_text, True, (255, 255, 255))  # White text
        self.screen.blit(level_surface, (x_position + 10, y_position + 10))  # Add some padding

    def draw_h2_cars_display(self, h2_cars_deployed):
        x_position = 10  # 10 pixels from the left edge
        y_position = 200  # Position below the fuel cell count
        box_width = 250
        box_height = 50
        box_color = (0, 0, 180)  # Blue color
        box_alpha = 128  # 50% transparent

        self.draw_transparent_box(x_position, y_position, box_width, box_height, box_color, box_alpha)

        h2_car_text = self.h2_font.render(f"H2 Cars: {h2_cars_deployed}", True, (255, 255, 255))  # White text
        self.screen.blit(h2_car_text, (x_position + 10, y_position + 10))  # Add some padding

    # You can add more methods for other UI elements here
def show_loading_screen(screen):
    # Set a loading font
    loading_font = pygame.font.Font("images/joystix.ttf", 48)
    loading_text = loading_font.render("Loading...", True, (255, 255, 255))
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Parameters for the loading beads
    num_beads = 8  # Number of beads
    radius = 50  # Radius of the circular path
    angle_offset = 0  # Initial angle offset
    bead_radius = 10  # Radius of each bead

    # Animation loop
    for _ in range(60):  # Loop for 60 frames (or adjust as needed)
        screen.fill((211, 211, 211))  # Fill with light grey again
        screen.blit(loading_text, loading_rect)

        # Draw the beads in a circular pattern
        for i in range(num_beads):
            angle = angle_offset + (i * (2 * math.pi / num_beads))  # Calculate the angle for each bead
            bead_x = SCREEN_WIDTH // 2 + radius * math.cos(angle)  # X position of the bead
            bead_y = SCREEN_HEIGHT // 2 + radius * math.sin(angle)  # Y position of the bead
            
            # Draw each bead
            pygame.draw.circle(screen, (255, 255, 255), (int(bead_x), int(bead_y)), bead_radius)  # Black bead

        pygame.display.flip()  # Update the display
        angle_offset += 0.1  # Increment the angle offset for animation
        pygame.time.delay(100)  # Delay for a short period to control the speed of the animation


