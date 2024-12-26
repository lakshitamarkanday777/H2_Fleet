
# import pygame
# import os

# class MiniMap:
#     def __init__(self, screen, x, y, radius, levels_maps, max_fuel_stations=2, zoom_factor=1.0):
#         """
#         Initialize the circular minimap with viewport functionality.

#         :param screen: The Pygame screen where the minimap will be displayed.
#         :param x: The x-coordinate of the center of the minimap.
#         :param y: The y-coordinate of the center of the minimap.
#         :param radius: The radius of the minimap.
#         :param levels_maps: A dictionary mapping levels to their corresponding map image file paths.
#         :param max_fuel_stations: The maximum number of fuel stations that can be added per level.
#         :param zoom_factor: The zoom level for the map.
#         """
#         self.screen = screen
#         self.x = x  # X position of minimap on screen
#         self.y = y  # Y position of minimap on screen
#         self.radius = radius
#         self.levels_maps = levels_maps
#         self.max_fuel_stations = max_fuel_stations  # Max fuel stations allowed
#         self.zoom_factor = zoom_factor  # Default zoom factor

#         # Viewport properties
#         self.viewport_width = int(radius * 2 * zoom_factor)
#         self.viewport_height = int(radius * 2 * zoom_factor)
        
#         # Current map and viewport position
#         self.current_map = None
#         self.viewport_x = 0
#         self.viewport_y = 0
        
#         self.fuel_stations = []  # List to store fuel stations (coordinates)
        
#         # Fallback surface if map loading fails
#         self.fallback_surface = None
#         self._create_fallback_surface()

#     def _create_fallback_surface(self):
#         """
#         Create a fallback surface with a simple pattern if map loading fails.
#         """
#         self.fallback_surface = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
#         # Create a checkered pattern
#         for x in range(0, self.viewport_width, 20):
#             for y in range(0, self.viewport_height, 20):
#                 color = (200, 200, 200) if (x // 20 + y // 20) % 2 == 0 else (150, 150, 150)
#                 pygame.draw.rect(self.fallback_surface, color, (x, y, 20, 20))

#     def load_map(self, level):
#         """
#         Load the full map image for the specified level.
        
#         :param level: The level number to load the map for.
#         """
#         # Reset current map
#         self.current_map = None
        
#         # Get map path
#         map_path = self.levels_maps.get(level)
        
#         if map_path and os.path.exists(map_path):
#             try:
#                 # Load the full, original map
#                 loaded_map = pygame.image.load(map_path)
                
#                 # Scale the map according to the zoom factor
#                 new_width = int(loaded_map.get_width() * self.zoom_factor)
#                 new_height = int(loaded_map.get_height() * self.zoom_factor)
#                 self.current_map = pygame.transform.scale(loaded_map, (new_width, new_height))
                
#                 print(f"Map loaded successfully: {map_path}")
#             except pygame.error as e:
#                 print(f"Error loading map {map_path}: {e}")
#                 self.current_map = None
#         else:
#             print(f"No map found for level {level}")
#             self.current_map = None

#     def update_viewport(self, player_x, player_y):
#         """
#         Update the viewport to center on the player's position.
        
#         :param player_x: X coordinate of the player
#         :param player_y: Y coordinate of the player
#         """
#         if not self.current_map:
#             return

#         # Center the viewport on the player, adjusted by the zoom factor
#         self.viewport_x = int(player_x * self.zoom_factor - self.radius)
#         self.viewport_y = int(player_y * self.zoom_factor - self.radius)

#         # Ensure viewport stays within map boundaries
#         self.viewport_x = max(0, min(self.viewport_x, 
#             self.current_map.get_width() - self.viewport_width))
#         self.viewport_y = max(0, min(self.viewport_y, 
#             self.current_map.get_height() - self.viewport_height))

#     def draw(self):
#         """Draw the minimap with its current viewport."""
#         # Determine which surface to use (either the map or the fallback surface)
#         map_surface = self.current_map if self.current_map else self.fallback_surface
    
#         # Create a surface for the minimap
#         minimap_surface = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
    
#         if self.current_map:
#             # Directly blit the portion of the map onto the minimap surface
#             minimap_surface.blit(map_surface, (0, 0), (self.viewport_x, self.viewport_y, self.viewport_width, self.viewport_height))
#         else:
#             # If no map, use the entire fallback surface
#             minimap_surface.blit(map_surface, (0, 0))
    
#         # Create a circular mask surface
#         mask_surface = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
#         pygame.draw.circle(mask_surface, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
    
#         # Apply circular mask
#         minimap_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
#         # Draw circular boundary around the minimap
#         pygame.draw.circle(self.screen, (0, 0, 0), (self.x, self.y), self.radius + 5, 2)
    
#         # Blit the masked minimap onto the screen at the correct position
#         self.screen.blit(minimap_surface, (self.x - self.radius, self.y - self.radius))
    
#         # Draw fuel stations if available
#         for station in self.fuel_stations:
#             if self.current_map:
#                 # Check if the fuel station is inside the viewport area
#                 if (self.viewport_x <= station[0] < self.viewport_x + self.viewport_width and
#                     self.viewport_y <= station[1] < self.viewport_y + self.viewport_height):
                    
#                     # Convert station coordinates to minimap coordinates
#                     station_x = station[0] - self.viewport_x + (self.x - self.radius)
#                     station_y = station[1] - self.viewport_y + (self.y - self.radius)
    
#                     # Check if the fuel station is inside the circular area
#                     dx = station_x - self.x
#                     dy = station_y - self.y
#                     if dx * dx + dy * dy <= self.radius * self.radius:
#                         pygame.draw.circle(self.screen, (0, 255, 0), (int(station_x), int(station_y)), 5)
    

#     def handle_click(self, mouse_pos):
#         """
#         Handle mouse clicks on the minimap, limiting the number of fuel stations.
        
#         :param mouse_pos: The (x, y) coordinates of the mouse click.
#         :return: True if a fuel station was added, False otherwise.
#         """
#         # Check if the maximum number of fuel stations is reached
#         if len(self.fuel_stations) >= self.max_fuel_stations:
#             print("Maximum number of fuel stations reached.")
#             return False  # Prevent adding more fuel stations
        
#         # Calculate distance from minimap center
#         dx = mouse_pos[0] - self.x
#         dy = mouse_pos[1] - self.y
#         distance = (dx ** 2 + dy ** 2) ** 0.5

#         if distance <= self.radius:
#             # Convert screen coordinates to map coordinates
#             map_x = self.viewport_x + (mouse_pos[0] - (self.x - self.radius))
#             map_y = self.viewport_y + (mouse_pos[1] - (self.y - self.radius))
            
#             # Add fuel station to the full map coordinates
#             self.fuel_stations.append((map_x, map_y))
#             print(f"Fuel station added at ({map_x}, {map_y})")
#             return True
#         return False
import pygame
import os

class MiniMap:
    def __init__(self, screen, x, y, radius, levels_maps, max_fuel_stations=2, zoom_factor=1.0, fuel_icon_path=None):
        """
        Initialize the circular minimap with viewport functionality.

        :param screen: The Pygame screen where the minimap will be displayed.
        :param x: The x-coordinate of the center of the minimap.
        :param y: The y-coordinate of the center of the minimap.
        :param radius: The radius of the minimap.
        :param levels_maps: A dictionary mapping levels to their corresponding map image file paths.
        :param max_fuel_stations: The maximum number of fuel stations that can be added per level.
        :param zoom_factor: The zoom level for the map.
        :param fuel_icon_path: Path to the fuel station icon image.
        """
        self.screen = screen
        self.x = x  # X position of minimap on screen
        self.y = y  # Y position of minimap on screen
        self.radius = radius
        self.levels_maps = levels_maps
        self.max_fuel_stations = max_fuel_stations  # Max fuel stations allowed
        self.zoom_factor = zoom_factor  # Default zoom factor
    
        # # Fuel station icon
        # self.fuel_icon = 
        # if fuel_icon_path:
        try:
            self.fuel_icon = pygame.image.load("images/fuel_station/h2_fuel_station.png")
            self.fuel_icon = pygame.transform.scale(self.fuel_icon, (20, 20))  # Adjust icon size
        except pygame.error as e:
            print(f"Error loading fuel icon: {e}")
            self.fuel_icon = None

        # Viewport properties
        self.viewport_width = int(radius * 2 * zoom_factor)
        self.viewport_height = int(radius * 2 * zoom_factor)
        
        # Current map and viewport position
        self.current_map = None
        self.viewport_x = 0
        self.viewport_y = 0
        
        self.fuel_stations = []  # List to store fuel stations (coordinates)
        
        # Fallback surface if map loading fails
        self.fallback_surface = None
        self._create_fallback_surface()

    def _create_fallback_surface(self):
        """
        Create a fallback surface with a simple pattern if map loading fails.
        """
        self.fallback_surface = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
        # Create a checkered pattern
        for x in range(0, self.viewport_width, 20):
            for y in range(0, self.viewport_height, 20):
                color = (200, 200, 200) if (x // 20 + y // 20) % 2 == 0 else (150, 150, 150)
                pygame.draw.rect(self.fallback_surface, color, (x, y, 20, 20))

    def load_map(self, level):
        """
        Load the full map image for the specified level.
        
        :param level: The level number to load the map for.
        """
        # Reset current map
        self.current_map = None
        
        # Get map path
        map_path = self.levels_maps.get(level)
        
        if map_path and os.path.exists(map_path):
            try:
                # Load the full, original map
                loaded_map = pygame.image.load(map_path)
                
                # Scale the map according to the zoom factor
                new_width = int(loaded_map.get_width() * self.zoom_factor)
                new_height = int(loaded_map.get_height() * self.zoom_factor)
                self.current_map = pygame.transform.scale(loaded_map, (new_width, new_height))
                
                print(f"Map loaded successfully: {map_path}")
            except pygame.error as e:
                print(f"Error loading map {map_path}: {e}")
                self.current_map = None
        else:
            print(f"No map found for level {level}")
            self.current_map = None

    def update_viewport(self, player_x, player_y):
        """
        Update the viewport to center on the player's position.
        
        :param player_x: X coordinate of the player
        :param player_y: Y coordinate of the player
        """
        if not self.current_map:
            return

        # Center the viewport on the player, adjusted by the zoom factor
        self.viewport_x = int(player_x * self.zoom_factor - self.radius)
        self.viewport_y = int(player_y * self.zoom_factor - self.radius)

        # Ensure viewport stays within map boundaries
        self.viewport_x = max(0, min(self.viewport_x, 
            self.current_map.get_width() - self.viewport_width))
        self.viewport_y = max(0, min(self.viewport_y, 
            self.current_map.get_height() - self.viewport_height))

    def draw(self):
        """Draw the minimap with its current viewport."""
        # Determine which surface to use (either the map or the fallback surface)
        map_surface = self.current_map if self.current_map else self.fallback_surface
    
        # Create a surface for the minimap
        minimap_surface = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
    
        if self.current_map:
            # Directly blit the portion of the map onto the minimap surface
            minimap_surface.blit(map_surface, (0, 0), (self.viewport_x, self.viewport_y, self.viewport_width, self.viewport_height))
        else:
            # If no map, use the entire fallback surface
            minimap_surface.blit(map_surface, (0, 0))
    
        # Create a circular mask surface
        mask_surface = pygame.Surface((self.viewport_width, self.viewport_height), pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
    
        # Apply circular mask
        minimap_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
        # Draw circular boundary around the minimap
        pygame.draw.circle(self.screen, (0, 0, 0), (self.x, self.y), self.radius + 5, 2)
    
        # Blit the masked minimap onto the screen at the correct position
        self.screen.blit(minimap_surface, (self.x - self.radius, self.y - self.radius))
    
        # Draw fuel stations with icons if available
        for station in self.fuel_stations:
            if self.fuel_icon:
                # Check if the fuel station is inside the viewport area
                if (self.viewport_x <= station[0] < self.viewport_x + self.viewport_width and
                    self.viewport_y <= station[1] < self.viewport_y + self.viewport_height):
                    
                    # Convert station coordinates to minimap coordinates
                    station_x = station[0] - self.viewport_x + (self.x - self.radius)
                    station_y = station[1] - self.viewport_y + (self.y - self.radius)
    
                    # Check if the fuel station is inside the circular area
                    dx = station_x - self.x
                    dy = station_y - self.y
                    if dx * dx + dy * dy <= self.radius * self.radius:
                        # Draw the fuel station icon at the correct position
                        self.screen.blit(self.fuel_icon, (station_x - self.fuel_icon.get_width() // 2, 
                                                          station_y - self.fuel_icon.get_height() // 2))

    def handle_click(self, mouse_pos):
        """
        Handle mouse clicks on the minimap, limiting the number of fuel stations.
        
        :param mouse_pos: The (x, y) coordinates of the mouse click.
        :return: True if a fuel station was added, False otherwise.
        """
        # Check if the maximum number of fuel stations is reached
        if len(self.fuel_stations) >= self.max_fuel_stations:
            print("Maximum number of fuel stations reached.")
            return False  # Prevent adding more fuel stations
        
        # Calculate distance from minimap center
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance <= self.radius:
            # Convert screen coordinates to map coordinates
            map_x = self.viewport_x + (mouse_pos[0] - (self.x - self.radius))
            map_y = self.viewport_y + (mouse_pos[1] - (self.y - self.radius))
            
            # Add fuel station to the full map coordinates
            self.fuel_stations.append((map_x, map_y))
            print(f"Fuel station added at ({map_x}, {map_y})")
            return True
        return False
    def reset_fuel_stations(self):
        """Reset the list of fuel stations for a new level."""
        self.fuel_stations.clear()