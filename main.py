import sys
import time
from math import sin, cos
from random import choice, randint
from typing import List
import os
from Timer import Timer
from settings import *
import random
from fuelcells import FuelCell, RedFuelCell
from levels import Level
from FuelStation import FuelStation
from levels_assets import LevelAssets
from Line import Line
from StartUi import StartUI, show_loading_screen, RepairMenu,UI
from Countdown import Countdown
from Sprite import HealthBar
from moviepy import VideoFileClip
from MiniMap1 import MiniMap
# from Bluecell import Bullet
def drawQuad(
        surface: pygame.Surface,
        color: pygame.Color,
        x1: int,
        y1: int,
        w1: int,
        x2: int,
        y2: int,
        w2: int,
):
    # trapezoidal
    pygame.draw.polygon(surface, color, [(x1 - w1, y1), (x2 - w2, y2),
                                         (x2 + w2, y2), (x1 + w1, y1)])
game = None

class Game:

    def __init__(self):
        global game
        game = self
        pygame.init()
        pygame.mixer.init()
        # Load background music
        pygame.mixer.music.load("sound/game_bg/2.mp3")  # Update with your music file path
        pygame.mixer.music.set_volume(0.3)  # Set volume to 50%
        pygame.mixer.music.play(-1)  # Play the music in a loop (-1 means infinite loop)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.last_time = time.time()
        
        # Load initial level assets (Level 1)
        self.level_assets = LevelAssets()
        self.bg_image, self.sprites, self.colors = self.level_assets.load_level_assets(1)
        
        # Modify this part in __init__
        # Create background surface with three tiles
        self.bg_surf = pygame.Surface(
            (self.bg_image.get_width() * 3, self.bg_image.get_height())
        )

        # Blit the background image three times
        self.bg_surf.blit(self.bg_image, (0, 0))
        self.bg_surf.blit(self.bg_image, (self.bg_image.get_width(), 0))
        self.bg_surf.blit(self.bg_image, (self.bg_image.get_width() * 2, 0))

        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))

        # sprites
        # self.sprites: list[pygame.Surface] = []
        self.car_sprites: list[pygame.Surface] = []

        # for i in range(1, objects_num):
        #     self.sprites.append(pygame.image.load(f"images/{i}.png").convert_alpha())

        for j in range(0, 8):
            img = pygame.image.load(f"images/car{j}.png")
            if j == 0 or j == 6:
                img = pygame.transform.scale(img, (enemy_car_size, enemy_car_size)).convert_alpha()

            self.car_sprites.append(img)

        self.dt = 0
        self.pos = 0
        self.startPos = 0
        self.player_x = 0
        self.player_y = start_elevation

        self.distanceX_to_track: list[float] = [2.2, 3.5, 4.5, 5.8, 6.2, 8.5, -2.1, -3.3, -4.2, -5.0, -7.0, -9.0]
        self.distanceZ: list[float] = [10, 50, 80, 99, 110, 200, 240, 340, 390, 420, 520, 650]

        self.speed = 0
        self.delta_time = min_speed

        # my car
        img = pygame.image.load("images/car_me_-_Copy-removebg-preview.png").convert_alpha()
        left_img = pygame.image.load("images/car_me_-_Copy-removebg-preview.png").convert_alpha()
        right_img = pygame.image.load("images/car_me_-_Copy-removebg-preview.png").convert_alpha()

        self.player_image = pygame.transform.scale(img, (240, 220))

        self.left_image = pygame.transform.scale(left_img, (240, 220))
        self.right_image = pygame.transform.scale(right_img, (240, 220))
        self.straight_image = pygame.transform.scale(img, (240, 220))

        self.main_rect = self.player_image.get_rect()

        self.main_rect.x = mid_bottom[0]
        self.main_rect.y = mid_bottom[1] - 100

        self.direction = "straight"
        self.max_cars = 10

        # fuel cells
        self.fuel_cells = []
        self.fuel_count = 0
        self.fuel_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        
        # sound for collision
        pygame.mixer.init()  # Initialize the mixer module
        self.fuel_collect_sound = pygame.mixer.Sound("sound/subway-surfers-coin-collect.mp3")  # Load the fuel cell sound

        self.speed_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        
        # displaying level
        self.level_font = pygame.font.Font("images/joystix.ttf", 20)  # Adjust size as needed
        self.level_manager = Level()
        
        # Initializing collision counter
        self.enemy_car_collision_count = 0 
        self.red_fuel_cell_manager = RedFuelCell()
        self.red_fuel_cells_collected = 0
        self.total_red_cells_collected = 0  # New attribute to track total red cells
        self.red_cell_pause_duration = 3  # seconds to show message
        # Font for red cell counter
        try:
            self.red_cell_font = pygame.font.Font("images/joystix.ttf", 24)
        except:
            self.red_cell_font = pygame.font.SysFont("arial", 24)
        self.timers = {

                "on impact": Timer(200),
                "after impact": Timer(500)

            }
        # Add fuel system
        self.max_fuel = 100
        self.current_fuel = self.max_fuel
        self.fuel_consumption_rate = 0.1  # Fuel used per frame while moving
        self.fuel_stations = []
        self.refueling = False
        self.fuel_warning_font = pygame.font.Font("images/joystix.ttf", 30)
        
        # Load fuel station image once
        try:
            self.fuel_station_img = pygame.image.load("images/fuel_station/h2_fuel_station.png").convert_alpha()
            self.fuel_station_img = pygame.transform.scale(self.fuel_station_img, (100, 100))
        except:
            print("Warning: Fuel station image not found")
            self.fuel_station_img = pygame.Surface((100, 100))
            self.fuel_station_img.fill((0, 255, 0))
        
        # Create countdown instance
        self.countdown = Countdown(self.screen)
        try:
            self.maintenance_centre_img = pygame.image.load("images/fuel_station/maintenance_1.jpg").convert_alpha()
            self.maintenance_centre_img = pygame.transform.scale(self.maintenance_centre_img, (200, 200))
        except:
            print("Warning: Maintenance Centre image not found")
            self.maintenance_centre_img = pygame.Surface((100, 100))
            self.maintenance_centre_img.fill((255, 0, 0))

        # Create font
        self.health_font = pygame.font.Font("images/joystix.ttf", 10)
        # Initialize health bar
        try:
        # Existing initialization code...

            # Health bar initialization with explicit parameters
            self.health_bar = HealthBar(
                x=10,             # Explicit x position
                y=280,            # Explicit y position
                width=200,        # Explicit width
                height=20,        # Explicit height
                max_health=100,   # Explicit max health
                font=self.health_font  # Use the font you've already created
            )

        except Exception as e:
            print(f"Error in Game initialization: {e}")
            # Fallback initialization or error handling
            pygame.quit()
            sys.exit()
        # self.fuel_bar = FuelBar(x=10, y=300, width=200, height=20, max_fuel=self.max_fuel, font=self.health_font)
        self.ui = UI(self.screen)  # Create an instance of the UI class
        self.max_speed = 100
        self.min_speed =30
       
        # Define maps for each level
        self.level_maps = {
            1: "images/map/Edmonton.png",
            2: "images/map/Red_deer.png",
            3: "images/map/Calgary.png",
            4: "images/map/banff.png",
            5: "images/map/vancouver .png",
        }
        
        # Create a MiniMap instance
        self.minimap = MiniMap(self.screen, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150, 100, self.level_maps)
        self.fuel_station_count = 0  # Counter for placed fuel stations
        self.max_fuel_stations = 2  
        # Load the first level's map
        self.minimap.load_map(self.level_manager.current_level + 1)
        try:
            self.completion_sound = pygame.mixer.Sound("sound/complete.mp3")
        except pygame.error as e:
            print(f"Could not load sound file: {e}")
            self.completion_sound = None
    # def draw_red_cell_counter(self, screen):
    #     """
    #     Draw the red cell collection counter on the screen
    #     """
    #     # Render red cell count text
    #     red_cell_count_text = f"- {self.red_fuel_cells_collected}/5"

    #     # Create text surface
    #     red_cell_surface = self.red_cell_font.render(
    #         red_cell_count_text, 
    #         True, 
    #         (255, 255, 255)  # White color
    #     )

    #     # Position for the image (top right corner)
    #     image_x = SCREEN_WIDTH - 200
    #     image_y = 300 # Y position for the image

    #     # Draw the image
    #     screen.blit(self.red_cell_image, (image_x, image_y))

    #     # Position the text next to the image
    #     text_rect = red_cell_surface.get_rect(
    #         midleft=(image_x + self.red_cell_image.get_width() + 5, image_y + self.red_cell_image.get_height() // 2)  # 5 pixels to the right of the image
    #     )

    #     # Draw the text
    #     screen.blit(red_cell_surface, text_rect)
    def create_level_lines(self,lines):
    
        """Update the lines with level-specific sprites and colors"""
        current_level = self.level_manager.current_level + 1
        colors = self.level_assets.level_colors[current_level]
        sprite_count = len(self.sprites)
        distance_count = len(self.distanceX_to_track)
        
        for i, line in enumerate(lines):
            # Set colors based on current level
            grass_color = colors["light_grass"] if (i // 3) % 2 else colors["dark_grass"]
            rumble_color = white_rumble if (i // 3) % 2 else black_rumble
            road_color = colors["light_road"] if (i // 3) % 2 else colors["dark_road"]
            
            line.grass_color = grass_color
            line.rumble_color = rumble_color
            line.road_color = road_color

            if i % 5 == 0:  # Adjust this number to control sprite density
                line.sprite_x = self.distanceX_to_track[randint(0, distance_count - 1)]
                line.sprite = self.sprites[randint(0, sprite_count - 1)]
    def setup_fuel_stations(self, lines):
        """Setup fuel stations for the current level"""
        # Clear existing fuel stations
        self.fuel_stations.clear()

        # Calculate spacing between stations
        station_spacing = len(lines) // 6  # Divide track into 6 segments (5 stations + start)

        # Keep track of used positions
        used_positions = set()

        for i in range(5):
            base_position = (i + 1) * station_spacing
            # Find the next available position that isn't too close to a maintenance centre
            position = base_position
            while position < len(lines):
                if (position not in used_positions and 
                    not any(abs(position - p) < station_spacing//2 for p in used_positions)):
                    # Create new fuel station
                    fuel_station = FuelStation()
                    lines[position].sprite = self.fuel_station_img
                    lines[position].sprite_type = "fuel_station"
                    lines[position].sprite_x = fuel_station.sprite_x + 1.0  # Right side of road

                    # Store the position
                    self.fuel_stations.append(position)
                    used_positions.add(position)
                    break
                position += 1

    def setup_maintenance_centres(self, lines):
        """Setup maintenance centres for the current level."""
        station_spacing = len(lines) // 6  # Same spacing as fuel stations

        # Get existing fuel station positions
        used_positions = set(self.fuel_stations)

        for i in range(5):
            base_position = (i + 1) * station_spacing + station_spacing // 2  # Offset from fuel stations
            # Find the next available position that isn't too close to a fuel station
            position = base_position
            while position < len(lines):
                if (position not in used_positions and 
                    not any(abs(position - p) < station_spacing//2 for p in used_positions)):
                    lines[position].sprite = self.maintenance_centre_img
                    lines[position].sprite_type = "maintenance_centre"
                    lines[position].sprite_x = -3.0  # Left side of road
                    used_positions.add(position)
                    break
                position += 1    
    
    def run(self):
        show_loading_screen(self.screen)
        # create lines
        lines: List[Line] = []  # empty matrix
        cars: List = []  # cars matrix

        # track & road creation
        for i in range(track_length_design):
            line = Line()
            car = Line()
            line.z = i * seg_length + 0.0001  # add this small to avoid divided by zero

            lines.append(line)
            cars.append(car)

            # Initialize the first level
            self.create_level_lines(lines)
            ########################################Racking track design
            # creating turning track (right curve)
            if 100 < i < 500:
                line.curve = 0.5

                # push car to the left
            # left curve
            if 800 < i < 1000:
                line.curve = -0.4

                # push car to the right
            # creating up/down track using sin/cos curvature
            if i > 700:
                line.y = sin(i / 30.0) * 1000

            if 1000 > i > 800:
                line.y = cos(i / 40.0) * 1000

            if 1400 < i < 1950:
                line.curve = -0.8

            # enemy cars on roads
            # between 1.0 and -1.0
            '''
            if i % 100 == 0:
                index = randint(0, 5)
                line.sprite = self.car_sprites[index]

                line.sprite_x = random.uniform(-3.0, 3.0)
                print(line.sprite_x)
                line.sprite_type = "car"

                # cars.append(car)
            '''
            ########################################
    
        N = len(lines)

        # elapse of time for each frame   ..     self.dt = time.time() - self.last_time
        self.last_time = time.time()
        self.map_cars_update(lines, self.max_cars)
        # Add countdown before starting the new level
        self.countdown.show()
        # Create a fuel station instance to use its proximity methods
        fuel_station_manager = FuelStation()
        
        while True:

            self.screen.fill("green")

            self.update_timers()

            # parallax background
            if self.speed > 0:
                self.bg_rect.x -= lines[self.startPos].curve * 2
            elif self.speed < 0:
                self.bg_rect.x += lines[self.startPos].curve * 2

            if self.bg_rect.right < SCREEN_WIDTH:
                self.bg_rect.x -= lines[self.startPos].curve * 2
            elif self.bg_rect.left > 0:
                self.bg_rect.x += lines[self.startPos].curve * 2

            self.screen.blit(self.bg_surf, self.bg_rect)
            self.parallax_background(lines)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.minimap.handle_click(event.pos):
                            if self.fuel_station_count < self.max_fuel_stations:
                                print("Fuel station added at:", event.pos)
                                self.fuel_station_count += 1  # Increment the counter
                            else:
                                print("Maximum fuel stations reached for this level.")
                
                        
            camH = self.player_y + lines[self.startPos].y  # cam H is the elevation , lines.y is the road y
            max_y = SCREEN_HEIGHT
            x, dx = 0, 0

            self.input(N)

            # draw road
            for n in range(self.startPos, self.startPos + show_num_seg):
                current = lines[n % N]

                # looping from start to finish (repeat itself when n > len(lines)
                current.projection(self.player_x - x, camH, self.pos - (N * seg_length if n >= N else 0))
                x += dx
                dx += current.curve

                current.adj_sprite_y = max_y

                if current.Y >= max_y:
                    continue

                max_y = current.Y

                prev = lines[(n - 1) % N]  # previous lines

                # draw grass
                drawQuad(self.screen, current.grass_color, 0, prev.Y, SCREEN_WIDTH, 0, current.Y, SCREEN_WIDTH)

                # draw rumble
                drawQuad(self.screen, current.rumble_color, prev.X, prev.Y, prev.W * 1.2, current.X, current.Y,
                         current.W * 1.2)

                # draw road
                drawQuad(self.screen, current.road_color, prev.X, prev.Y, prev.W, current.X, current.Y, current.W)
    
            match self.direction:

                case "left":
                    self.player_image = self.left_image
                case "right":
                    self.player_image = self.right_image
                case "straight":
                    self.player_image = self.straight_image

            # reverse draw the buildings
            for n in range(self.startPos + show_num_seg, self.startPos, -1):
                self.collision = lines[n % N].drawSprite(self.screen, self.main_rect, self.player_image,game)

                if self.collision:
                    if lines[n % N].sprite_type == "car":
                        self.timers["on impact"].timer_on()  # Handle car collision
                        # Handle car collision
                        self.health_bar.take_damage()
                        
                elif lines[n % N].sprite_type == "fuel_cell":
                # Just print the message for fuel cell collection
                    continue  # Continue without affecting player
                
                if self.collision:
                    if lines[n % N].sprite_type == "fuel_station":
                        # Optional: Additional game-wide refueling logic if needed
                        break 
                if self.collision:
                    if lines[n % N].sprite_type == "red_cell":
                        
                        break  
            # Add fuel station proximity warning
            if fuel_station_manager.check_fuel_station_proximity(lines, self.startPos):
                fuel_station_manager.render_fuel_station_warning(self.screen)
            
            # Update fuel consumption (add this after the refueling check)
            if self.speed != 0 and not self.refueling:
                self.current_fuel -= self.fuel_consumption_rate * abs(self.delta_time / max_speed)
                if self.current_fuel < 0:
                    self.current_fuel = 0 
            # Update the fuel bar
            # self.fuel_bar.current_fuel = self.current_fuel  # Update the fuel bar with current fuel
            # If out of fuel, stop the car
            if self.current_fuel <= 0:
                self.current_fuel = 0
                self.speed = 0
                self.delta_time = min_speed
                warning = self.fuel_warning_font.render("Out of Fuel!", True, "red")
                self.screen.blit(warning, (SCREEN_WIDTH//2 - warning.get_width()//2, SCREEN_HEIGHT//2))  

            if self.level_manager.check_level_progression(self.fuel_count):
                if self.level_manager.current_level + 1 > 5:  # If level exceeds 5
                    self.display_end_screen()  # Show the end screen
                else:
                    self.reset_map(lines)
            
            self.clock.tick(min_speed + self.delta_time)
            
            self.ui.draw_level_display(self.level_manager.current_level)  # Call the method to draw the level display
            self.ui.draw_fuel_display(self.fuel_count,game)
            self.ui.draw_speed_display(self.delta_time)
            self.ui.draw_level_display(self.level_manager.current_level)
            self.ui.draw_h2_cars_display(self.level_manager.get_h2_cars_deployed())
            
            # Draw red cell counter
           
            self.draw_fuel_gauge()  # Draw the fuel gauge
            # # Draw the fuel bar
            # self.fuel_bar.draw(self.screen)
            self.health_bar.draw(self.screen)
            self.minimap.update_viewport(self.player_x, self.pos)
            self.minimap.draw()
            pygame.display.update()

    def parallax_background(self, lines):
        """
        Create a seamless, repeating background with smooth scrolling

        :param lines: List of road lines to determine scrolling speed and direction
        """
        # Calculate scroll speed based on curve and current speed
        scroll_speed = lines[self.startPos].curve * 2 * (self.speed / seg_length)

        # Update background position
        self.bg_rect.x -= scroll_speed

        # Get background image dimensions
        bg_width = self.bg_image.get_width()

        # Ensure seamless wrapping
        if self.bg_rect.right <= SCREEN_WIDTH:
            self.bg_rect.x = 0
        elif self.bg_rect.left >= 0:
            self.bg_rect.x = -bg_width

        # Blit the background surface
        self.screen.blit(self.bg_surf, self.bg_rect)
    def play_video(self, video_path):
        # Initialize MoviePy video clip
        clip = VideoFileClip(video_path)
        # Extract audio and save it to a temporary file
        audio_path = "images/ending/aircraft-248663.mp3"  # Temporary audio file
        clip.audio.write_audiofile(audio_path)

        # Play the audio using Pygame's mixer
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        # Play the video frame by frame
        for frame in clip.iter_frames(fps=30, dtype='uint8'):
            # Convert the frame to a Pygame surface
            frame_surface = pygame.surfarray.make_surface(frame)
            # Rotate the frame surface if needed (90 degrees clockwise)
            frame_surface = pygame.transform.rotate(frame_surface, -90)
            # Clear the screen with black
            self.screen.fill((0, 0, 0))

            # Get the dimensions of the frame
            frame_width, frame_height = frame_surface.get_size()

            # Calculate the scale to maintain aspect ratio
            scale = min(SCREEN_WIDTH / frame_width, SCREEN_HEIGHT / frame_height)
            new_width = int(frame_width * scale)
            new_height = int(frame_height * scale)

            # Resize the frame surface
            frame_surface = pygame.transform.scale(frame_surface, (new_width, new_height))

            # Calculate the position to center the video
            x_position = (SCREEN_WIDTH - new_width) // 2
            y_position = (SCREEN_HEIGHT - new_height) // 2

            # Draw the frame directly at the calculated position
            self.screen.blit(frame_surface, (x_position, y_position))
            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
        clip.close()  # Close the video clip after playing
        pygame.mixer.music.stop()  # Stop the audio playback
    # method to display  game over screen after a collision
    def display_end_screen(self):
        pygame.mixer.music.pause()
        try:
           
            self.completion_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")
        # Set up fonts
        end_screen_font = pygame.font.Font("images/joystix.ttf", 40)
        button_font = pygame.font.Font("images/joystix.ttf", 30)

        # Screen setup
        self.screen.fill((211, 211, 211))  # Gray background

        # Title
        title_text = end_screen_font.render("Congratulations!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)

        # Completion message
        completion_text = button_font.render("You've completed all levels!", True, (255, 255, 255))
        completion_rect = completion_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(completion_text, completion_rect)

        # Restart Button
        restart_text = button_font.render("Restart Game", True, (0, 0, 0))
        restart_button = pygame.Surface((300, 60))
        restart_button.fill((0, 255, 0))  # Green button
        restart_button_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_button.blit(restart_text, restart_text.get_rect(center=restart_button.get_rect().center))

        # Quit Button
        quit_text = button_font.render("Quit Game", True, (0, 0, 0))
        quit_button = pygame.Surface((300, 60))
        quit_button.fill((255, 0, 0))  # Red button
        quit_button_rect = quit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        quit_button.blit(quit_text, quit_text.get_rect(center=quit_button.get_rect().center))

        # Add buttons to the screen
        self.screen.blit(restart_button, restart_button_rect)
        self.screen.blit(quit_button, quit_button_rect)

        pygame.display.update()

        # Wait for player input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if Restart button is clicked
                    if restart_button_rect.collidepoint(mouse_pos):
                        waiting = False
                        self.restart_to_level_1()  # Call a new method to restart the game
                        pygame.mixer.music.unpause()
                    # Check if Quit button is clicked
                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def restart_to_level_1(self):
        # Reset the level manager to Level 1
        self.level_manager.current_level = 0

        # Reset other game variables
        self.fuel_count = 0
        self.speed = 0
        self.delta_time = min_speed
        self.current_fuel = self.max_fuel
        self.player_x = 0
        self.player_y = start_elevation
        self.total_red_cells_collected = 0

        # Reload Level 1 assets and state
        lines = []  # Clear the current lines
        for i in range(track_length_design):
            line = Line()
            line.z = i * seg_length + 0.0001  # Add small value to avoid divide-by-zero error
            lines.append(line)

        self.reset_map(lines)  # Reset the game map to Level 1
        self.run()  # Start the game loop again

    def reset_map(self, lines):

        current_level = self.level_manager.current_level + 1
        # Add countdown before starting the new level
        self.countdown.show()
        # Load new assets for the current level
        self.bg_image, new_sprites, colors = self.level_assets.load_level_assets(current_level)
        
        # Create a new background surface with three tiles of the current level's background
        self.bg_surf = pygame.Surface(
            (self.bg_image.get_width() * 3, self.bg_image.get_height())
        )
    
        # Blit the background image three times to create a seamless repeating background
        self.bg_surf.blit(self.bg_image, (0, 0))
        self.bg_surf.blit(self.bg_image, (self.bg_image.get_width(), 0))
        self.bg_surf.blit(self.bg_image, (self.bg_image.get_width() * 2, 0))
        
        # Reset the background rectangle to its initial position
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))
        
        # Setup fuel stations for the new level
        if self.level_manager.fuel_station_unlocked:
            self.setup_fuel_stations(lines)
            self.setup_maintenance_centres(lines)
        
        # Update sprites
        self.sprites = new_sprites
        self.pos = 0
        self.startPos = 0
        self.player_x = 0
        self.player_y = start_elevation
        self.speed = 0
        self.delta_time = min_speed
        self.fuel_station_count = 0
        self.minimap.reset_fuel_stations()
        # self.fuel_count = 0
        # if self.level_manager.current_level + 1 >= 5:
        #     self.level_manager.current_level = 0  # Reset to the first level
        # else:
        #     self.level_manager.current_level += 1
        # Initialize the first level
        self.create_level_lines(lines)
        self.minimap.load_map(self.level_manager.current_level + 1)
          
        # Reset fuel cell state for all lines that contain a fuel cell
        for line in lines:
            if line.sprite_type == "fuel_cell":
                line.reset_fuel_cell()

        # Update road colors for all lines
        for line in lines:
            line.grass_color = colors["light_grass"] if (lines.index(line) // 3) % 2 else colors["dark_grass"]
            line.road_color = colors["light_road"] if (lines.index(line) // 3) % 2 else colors["dark_road"]
        
        self.map_cars_update(lines, self.max_cars)
        self.max_cars += 1  # Increase difficulty for the new level
        print(f"Level {self.level_manager.current_level + 1} started!")
    
    def open_repair_menu(self):
        if not hasattr(self, 'repair_menu'):
            self.repair_menu = RepairMenu(self.screen,game)

        # Pause the game
        original_speed = self.speed
        self.speed = 0

        # Show repair menu
        self.repair_menu.is_active = True

        while self.repair_menu.is_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                self.repair_menu.handle_input(event)

            # Redraw the game state
            self.screen.fill("green")
            # Redraw your game background, road, etc.
            # You might want to add a method to quickly redraw the current game state

            # Draw the repair menu overlay
            self.repair_menu.draw()

            pygame.display.update()

        # Resume game speed
        self.speed = original_speed
    def input(self, N):

        keys = pygame.key.get_pressed()
        # # Add this to open repair menu
        if keys[pygame.K_RETURN]:  # When ENTER is pressed
            self.open_repair_menu()
        # acceleration
        if keys[pygame.K_UP] and not self.timers["on impact"].active:
            self.speed = seg_length

            if self.delta_time <= max_speed:
                self.delta_time += 0.1
            elif self.delta_time > 70:
                self.delta_time = 120

        elif self.timers["on impact"].active and not self.timers["after impact"].active:
            self.speed = - 10 * seg_length if self.delta_time > 70 else - 3 * seg_length
            self.timers["after impact"].timer_on()
            self.delta_time = min_speed
            self.player_x -= 100

        elif self.timers["after impact"].active:

            self.speed = 0

        # deceleration by brakes
        elif keys[pygame.K_DOWN] and self.pos > 0:
            self.delta_time -= 1
            if self.delta_time < min_speed:
                self.delta_time = min_speed
                self.speed = 0

        ## deceleration by friction
        else:

            self.delta_time -= 0.2
            self.speed = seg_length
            if self.delta_time < min_speed:
                self.delta_time = min_speed
                self.speed = 0
            ###################

        # # Set speed to zero if no acceleration or deceleration is happening
        # if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        #     self.delta_time = 0
        #     self.speed = 0

        self.pos += self.speed

        # direction control
        if keys[pygame.K_LEFT]:
            self.player_x -= 50
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.player_x += 50
            self.direction = "right"
        else:
            self.direction = "straight"

        while self.pos >= N * seg_length:
            self.pos -= N * seg_length
        while self.pos < 0:
            self.pos += N * seg_length

        self.startPos = self.pos // seg_length
        
    def _get_gradient_color(self, fuel_percentage):
        """
        Return a color based on the fuel percentage.
        Color will go from:
        - Green (100 to 80)
        - Orange (80 to 60)
        - Yellow (60 to 40)
        - Red (40 to 0)
        """
        if fuel_percentage > 0.8:
            return (0, 255, 0)  # Green
        elif fuel_percentage > 0.6:
            return (255, 165, 0)  # Orange
        elif fuel_percentage > 0.4:
            return (255, 255, 0)  # Yellow
        else:
            return (255, 0, 0)  # Red
    
    def draw_fuel_gauge(self):
        # Define dimensions and positions for the fuel gauge
        bar_width = 200  # Width of the fuel gauge
        bar_height = 20  # Height of the fuel gauge
        x_position = 10  # X position on the screen
        y_position = 340  # Y position on the screen
        border_radius = 10  # Radius for rounded corners

        # Calculate the filled width based on current fuel
        filled_width = (self.current_fuel / self.max_fuel) * bar_width
        
        # Get the gradient color based on the current fuel percentage
        bar_color = self._get_gradient_color(filled_width / bar_width)
        
        # Draw the background of the fuel gauge (neutral gray color for unfilled portion)
        pygame.draw.rect(self.screen, (200, 200, 200),  # Light gray background
                         (x_position, y_position, bar_width, bar_height), border_radius)

        # Draw the filled portion of the fuel gauge (color based on fuel percentage)
        pygame.draw.rect(self.screen, bar_color, 
                         (x_position, y_position, filled_width, bar_height), border_radius)

        # Optionally, adjust and draw the fuel percentage text above the gauge
        fuel_percentage_text = f"Fuel: {int((self.current_fuel / self.max_fuel) * 100)}%"
        
        # Get the color of the text based on the fuel percentage
        text_color = bar_color  # Use the same color as the fuel bar
        
        font = pygame.font.Font(None, 24)

        # Render the text
        text_surface = font.render(fuel_percentage_text, True, text_color)  # Use the same color as the bar

        # Draw the text at the center of the bar or just above the bar
        text_x = x_position + (bar_width - text_surface.get_width()) // 2
        text_y = y_position - 15  # Place text above the bar

        # Optionally, adjust text size based on fuel level
        if self.current_fuel / self.max_fuel < 0.2:  # If fuel is very low, increase text size
            font = pygame.font.Font(None, 30)
            text_surface = font.render(fuel_percentage_text, True, (255, 0, 0))  # Red text for low fuel
            text_y -= 10  # Adjust position if text size is larger

        self.screen.blit(text_surface, (text_x, text_y))

    
    def speed_limiter(self):

        if self.player_x > 1800 or self.player_x < -1800:
            self.delta_time -= 1
            if self.delta_time <= 10:
                self.delta_time = 10

    def map_cars_update(self, lines, max_cars):
        if self.level_manager.current_level + 1 == 5:
            max_cars = self.max_cars  # Keep it fixed
        # Reset fuel cells for each new level
        self.fuel_cells.clear()
        car_dist = 50 * (10 - max_cars)
        if car_dist <= 0:
            car_dist = 50
        fuel_cell_dist = 5 # adjust this value to change the frequency of fuel cells
        fuel_cell_chance = 0.7
        # print(car_dist)
        for i, line in enumerate(lines):
            if i % (car_dist - max_cars) == 0:
                index = randint(0, 7)
                line.sprite = self.car_sprites[index]
                line.sprite_x = random.uniform(-3.0, 3.0)
                line.sprite_type = "car"

             # Add fuel cells to the road at random positions
            if i % fuel_cell_dist == 0 and random.random() < fuel_cell_chance:  # 5% chance of adding a fuel cell
                fuel_cell = FuelCell()
                fuel_cell.sprite_x = random.uniform(-1.5, 1.5)
                line.sprite = fuel_cell.sprite
                line.sprite_type = "fuel_cell"
                self.fuel_cells.append(fuel_cell)
            # Add this line to spawn red fuel cells
        self.red_fuel_cell_manager.spawn_red_fuel_cell(lines)

    def show_red_cell_message(self, message):
        """
        Display the red cell collection message
        """
        # Pause the game
        original_speed = self.speed
        self.speed = 0
        
        # # Create font
        message_font = pygame.font.Font("images/joystix.ttf", 24)
        if isinstance(message, pygame.Surface):
        # Scale the image using transform.scale()
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Scale to 70% of screen width and height
            scaled_message = pygame.transform.scale(
                message, 
                (
                    int(screen_width * 0.4),  # width
                    int(screen_height * 0.4)  # height
                )
            )

            # Create rect centered on screen
            message_rect = scaled_message.get_rect(center=(screen_width // 2, screen_height // 2))

            # Blit the scaled image
            self.screen.blit(scaled_message, message_rect)

        else:
            # Fallback for text
            message_surface = self.red_cell_font.render(str(message), True, (255, 0, 0))
            message_rect = message_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(message_surface, message_rect)
        # Display message for a few seconds
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < self.red_cell_pause_duration * 1000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            # Redraw the screen with the message
            # self.screen.fill((0, 0, 0))  # Black background
            # self.screen.blit(message, message_rect)
            pygame.display.flip()
        
        # Resume game
        self.speed = original_speed

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()


if __name__ == "__main__":
    # Initialize start screen
    start_ui = StartUI(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Run the start screen
    start_game = start_ui.run()

    if start_game:
        game = Game()
        game.run()
