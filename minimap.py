# # # import pygame

# # # class MiniMap:
# # #     def __init__(self, screen_width, screen_height):
# # #         self.expanded = False
# # #         self.radius = 80  # Minimap circle radius when minimized
# # #         self.expanded_size = (400, 400)  # Size when expanded
        
# # #         # Position the minimap in the top-right corner
# # #         self.position = (screen_width - self.radius - 5, 200)
# # #         self.expanded_position = (screen_width//2 - self.expanded_size[0]//2, 
# # #                                 screen_height//2 - self.expanded_size[1]//2)
        
# # #         # Create surfaces only once for better performance
# # #         self.mini_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
# # #         self.expanded_surface = pygame.Surface(self.expanded_size, pygame.SRCALPHA)
        
# # #         # Store fuel stations
# # #         self.fuel_stations = []
# # #         self.max_stations_per_level = {
# # #             1: 1,
# # #             2: 2,
# # #             3: 1,
# # #             4: 1,
# # #             5: 1
# # #         }
    
# # #     def add_fuel_station(self, x, y, current_level):
# # #         """Add a fuel station if below maximum for current level"""
# # #         station_count = sum(1 for station in self.fuel_stations if station['level'] == current_level)
# # #         if station_count < self.max_stations_per_level.get(current_level, 1):
# # #             self.fuel_stations.append({
# # #                 'x': x,
# # #                 'y': y,
# # #                 'level': current_level
# # #             })
# # #             return True
# # #         return False
    
# # #     def toggle(self):
# # #         """Toggle between expanded and minimized state"""
# # #         self.expanded = not self.expanded
    
# # #     def draw(self, screen, player_pos, current_level):
# # #         """Draw the minimap"""
# # #         if self.expanded:
# # #             surface = self.expanded_surface
# # #             pos = self.expanded_position
# # #             size = self.expanded_size
# # #         else:
# # #             surface = self.mini_surface
# # #             pos = self.position
# # #             size = (self.radius * 2, self.radius * 2)
        
# # #         # Clear the surface
# # #         surface.fill((0, 0, 0, 0))
        
# # #         # Draw background
# # #         pygame.draw.circle(surface, (0, 0, 0, 128), 
# # #                          (size[0]//2, size[1]//2), 
# # #                          size[0]//2 if not self.expanded else size[0]//2 - 2)
        
# # #         # Draw road
# # #         road_width = size[0] // 4
# # #         pygame.draw.rect(surface, (100, 100, 100), 
# # #                         (size[0]//2 - road_width//2, 0, road_width, size[1]))
        
# # #         # Draw player
# # #         player_radius = 5 if not self.expanded else 8
# # #         pygame.draw.circle(surface, (0, 255, 0), 
# # #                          (size[0]//2 + (player_pos[0] / 20), size[1]//2), 
# # #                          player_radius)
        
# # #         # Draw fuel stations for current level
# # #         station_radius = 4 if not self.expanded else 6
# # #         for station in self.fuel_stations:
# # #             if station['level'] == current_level:
# # #                 station_pos = (
# # #                     size[0]//2 + (station['x'] / 20),
# # #                     size[1]//2 + (station['y'] / 20)
# # #                 )
# # #                 pygame.draw.circle(surface, (0, 0, 255), station_pos, station_radius)
        
# # #         # Draw the surface
# # #         screen.blit(surface, pos)
        
# # #         # Draw close button when expanded
# # #         if self.expanded:
# # #             close_btn = pygame.Rect(
# # #                 pos[0] + size[0] - 30, pos[1] + 10, 20, 20
# # #             )
# # #             pygame.draw.rect(surface, (255, 0, 0), (size[0] - 30, 10, 20, 20))
# # #             return close_btn
# # #         return None

# # #     def handle_click(self, pos, current_level):
# # #         """Handle mouse clicks on the minimap"""
# # #         if self.expanded:
# # #             # Convert click position to map coordinates
# # #             map_x = (pos[0] - self.expanded_position[0] - self.expanded_size[0]//2) * 20
# # #             map_y = (pos[1] - self.expanded_position[1] - self.expanded_size[1]//2) * 20
# # #             return self.add_fuel_station(map_x, map_y, current_level)
# # #         return False
# # # minimap.py

# # import pygame
# # from math import cos, sin, radians
# # import json

# # class Minimap:
# #     def __init__(self, screen_width, screen_height):
# #         self.screen_width = screen_width
# #         self.screen_height = screen_height
        
# #         # Minimap properties
# #         self.radius = 100  # Radius of circular minimap
# #         self.position = (screen_width - 150, 150)  # Top-right corner position
# #         self.is_expanded = False
# #         self.expanded_size = (800, 600)  # Size when expanded
        
# #         # Load and scale map images
# #         try:
# #             self.map_image = pygame.image.load("images/backgrounds_1/city_skybg.jpg").convert_alpha()
# #             self.map_image = pygame.transform.scale(self.map_image, (200, 200))  # For circular minimap
# #             self.expanded_map = pygame.transform.scale(self.map_image, self.expanded_size)
# #         except:
# #             # Create placeholder if image not found
# #             self.map_image = pygame.Surface((200, 200))
# #             self.map_image.fill((200, 200, 200))
# #             self.expanded_map = pygame.Surface(self.expanded_size)
# #             self.expanded_map.fill((200, 200, 200))
        
# #         # Player marker
# #         self.player_marker_size = 10
# #         self.player_color = (255, 0, 0)
        
# #         # Close button for expanded map
# #         self.close_btn = pygame.Rect(screen_width - 50, 50, 30, 30)
        
# #         # Fuel stations
# #         self.fuel_stations = []
# #         self.max_stations_per_level = {
# #             1: 1,
# #             2: 2,
# #             3: 3,
# #             4: 4,
# #             5: 5
# #         }
# #         self.unlocked_stations = 0
        
# #         # Load saved stations if any
# #         self.fuel_stations()

# # class FuelStationManager:
# #     def __init__(self):
# #         self.unlocked_stations = 0
# #         self.placed_stations = []
# #         self.station_costs = {
# #             1: 1000,
# #             2: 2000,
# #             3: 3000,
# #             4: 4000,
# #             5: 5000
# #         }
        
# #     def unlock_new_station(self, level):
# #         """Called when a level is completed"""
# #         if self.unlocked_stations < self.max_stations_per_level[level]:
# #             return True
# #         return False
    
# #     def place_station(self, position, level):
# #         """Place a new fuel station at the selected position"""
# #         if len(self.placed_stations) < self.max_stations_per_level[level]:
# #             station = {
# #                 'position': position,
# #                 'level': level,
# #                 'cost': self.station_costs[level]
# #             }
# #             self.placed_stations.append(station)
# #             self.save_stations()
# #             return True
# #         return False
    
# #     def save_stations(self):
# #         """Save placed stations to a file"""
# #         with open('fuel_stations.json', 'w') as f:
# #             json.dump(self.placed_stations, f)
    
# #     def load_stations(self):
# #         """Load placed stations from file"""
# #         try:
# #             with open('fuel_stations.json', 'r') as f:
# #                 self.placed_stations = json.load(f)
# #         except:
# #             self.placed_stations = []

# # class MinimapInterface:
# #     def __init__(self, game):
# #         self.game = game
# #         self.minimap = Minimap(game.screen.get_width(), game.screen.get_height())
# #         self.station_manager = FuelStationManager()
        
# #     def update(self, player_pos, player_angle):
# #         """Update minimap with current player position"""
# #         # Convert world coordinates to minimap coordinates
# #         map_x = self.minimap.position[0] + (player_pos[0] / self.game.track_length) * self.minimap.radius
# #         map_y = self.minimap.position[1] + (player_pos[1] / self.game.track_length) * self.minimap.radius
        
# #         self.minimap.player_pos = (map_x, map_y)
# #         self.minimap.player_angle = player_angle
    
# #     def draw(self, screen):
# #         """Draw the minimap"""
# #         if not self.minimap.is_expanded:
# #             # Draw circular minimap
# #             minimap_surface = pygame.Surface((self.minimap.radius * 2, self.minimap.radius * 2), pygame.SRCALPHA)
# #             pygame.draw.circle(minimap_surface, (0, 0, 0, 128), 
# #                              (self.minimap.radius, self.minimap.radius), 
# #                              self.minimap.radius)
            
# #             # Draw the map image clipped to circle
# #             scaled_map = pygame.transform.scale(self.minimap.map_image, 
# #                                              (self.minimap.radius * 2, self.minimap.radius * 2))
# #             minimap_surface.blit(scaled_map, (0, 0))
            
# #             # Draw player marker
# #             pygame.draw.circle(minimap_surface, self.minimap.player_color,
# #                              (self.minimap.radius + cos(self.minimap.player_angle) * 5,
# #                               self.minimap.radius + sin(self.minimap.player_angle) * 5),
# #                              3)
            
# #             screen.blit(minimap_surface, 
# #                        (self.minimap.position[0] - self.minimap.radius,
# #                         self.minimap.position[1] - self.minimap.radius))
# #         else:
# #             # Draw expanded map
# #             screen.blit(self.minimap.expanded_map, 
# #                        ((screen.get_width() - self.minimap.expanded_size[0]) // 2,
# #                         (screen.get_height() - self.minimap.expanded_size[1]) // 2))
            
# #             # Draw close button
# #             pygame.draw.rect(screen, (255, 0, 0), self.minimap.close_btn)
            
# #             # Draw placed fuel stations
# #             for station in self.station_manager.placed_stations:
# #                 pos = station['position']
# #                 pygame.draw.circle(screen, (0, 255, 0), pos, 5)
    
# #     def handle_click(self, pos):
# #         """Handle mouse clicks on the minimap"""
# #         if not self.minimap.is_expanded:
# #             # Check if click is within circular minimap
# #             dx = pos[0] - self.minimap.position[0]
# #             dy = pos[1] - self.minimap.position[1]
# #             if (dx * dx + dy * dy) <= self.minimap.radius * self.minimap.radius:
# #                 self.minimap.is_expanded = True
# #         else:
# #             # Check if close button clicked
# #             if self.minimap.close_btn.collidepoint(pos):
# #                 self.minimap.is_expanded = False
# #             # Check if placing new station
# #             elif self.game.level_manager.fuel_station_unlocked:
# #                 self.station_manager.place_station(pos, self.game.level_manager.current_level + 1)

# # def show_station_unlock_prompt(screen):
# #     """Show prompt when new station is available"""
# #     prompt_surface = pygame.Surface((400, 200))
# #     prompt_surface.fill((255, 255, 255))
# #     font = pygame.font.Font(None, 36)
# #     text = font.render("Unlock new fuel station?", True, (0, 0, 0))
# #     yes_btn = pygame.Rect(100, 100, 80, 40)
# #     no_btn = pygame.Rect(220, 100, 80, 40)
    
# #     prompt_surface.blit(text, (50, 50))
# #     pygame.draw.rect(prompt_surface, (0, 255, 0), yes_btn)
# #     pygame.draw.rect(prompt_surface, (255, 0, 0), no_btn)
    
# #     screen.blit(prompt_surface, 
# #                 ((screen.get_width() - 400) // 2,
# #                  (screen.get_height() - 200) // 2))
    
# #     return yes_btn, no_btn
# # import pygame
# # import osmnx as ox
# # import numpy as np

# # class MiniMap:
# #     def __init__(self, screen_width, screen_height, edmonton_map):
# #         self.screen_width = screen_width
# #         self.screen_height = screen_height
# #         self.edmonton_map = edmonton_map
        
# #         # Road colors for different road types
# #         self.road_colors = {
# #             'motorway': (255, 0, 0),        # Red for motorways
# #             'trunk': (255, 128, 0),         # Orange for trunk roads
# #             'primary': (255, 255, 0),       # Yellow for primary roads
# #             'secondary': (0, 255, 0),       # Green for secondary roads
# #             'tertiary': (0, 0, 255),        # Blue for tertiary roads
# #             'residential': (200, 200, 200), # Gray for residential roads
# #             'default': (100, 100, 100)      # Dark gray for unknown road types
# #         }
        
# #         self.mini_map_size = 200  # Size of the mini-map
    
# #     def create_minimap(self):
# #         # Create a surface for the mini-map with transparency
# #         mini_map_surface = pygame.Surface((self.mini_map_size, self.mini_map_size), pygame.SRCALPHA)
        
# #         # Find map bounds to calculate scaling
# #         x_coords = []
# #         y_coords = []
# #         for road in self.edmonton_map.roads:
# #             for x, y in road['coords']:
# #                 x_coords.append(x)
# #                 y_coords.append(y)
        
# #         min_x, max_x = min(x_coords), max(x_coords)
# #         min_y, max_y = min(y_coords), max(y_coords)
        
# #         # Calculate scaling factors
# #         width_scale = self.mini_map_size / (max_x - min_x)
# #         height_scale = self.mini_map_size / (max_y - min_y)
# #         scale_factor = min(width_scale, height_scale) * 0.9  # 90% of the mini-map size
        
# #         # Calculate offsets to center the map
# #         offset_x = (self.mini_map_size / 2) - ((max_x + min_x) / 2 * scale_factor)
# #         offset_y = (self.mini_map_size / 2) - ((max_y + min_y) / 2 * scale_factor)
        
# #         # Draw roads on the mini-map
# #         for road in self.edmonton_map.roads:
# #             coords = road['coords']
# #             road_type = road.get('type', 'default')
# #             color = self.road_colors.get(road_type, self.road_colors['default'])
            
# #             for i in range(len(coords) - 1):
# #                 # Transform coordinates
# #                 x1 = coords[i][0] * scale_factor + offset_x
# #                 y1 = coords[i][1] * scale_factor + offset_y
# #                 x2 = coords[i+1][0] * scale_factor + offset_x
# #                 y2 = coords[i+1][1] * scale_factor + offset_y
                
# #                 # Draw road segments
# #                 pygame.draw.line(mini_map_surface, color, (x1, y1), (x2, y2), 2)
        
# #         # Create circular mask
# #         mask = pygame.Surface((self.mini_map_size, self.mini_map_size), pygame.SRCALPHA)
# #         pygame.draw.circle(mask, (255, 255, 255, 255), 
# #                            (self.mini_map_size // 2, self.mini_map_size // 2), 
# #                            self.mini_map_size // 2)
        
# #         # Apply circular mask
# #         mini_map_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
# #         # # Draw buildings or other features (example)
# #         # for building in self.edmonton_map.buildings:
# #         #     pygame.draw.polygon(mini_map_surface, (100, 100, 255), building['coords'])
        
# #         return mini_map_surface
    
# #     def draw_minimap(self, screen, player_x=0, player_y=0):
# #         # Create mini-map surface
# #         mini_map_surface = self.create_minimap()
        
# #         # Calculate player position on the mini-map
# #         x_coords = [coord[0] for road in self.edmonton_map.roads for coord in road['coords']]
# #         y_coords = [coord[1] for road in self.edmonton_map.roads for coord in road['coords']]
# #         min_x, max_x = min(x_coords), max
        
# #         # Optional: Draw player position
# #         pygame.draw.circle(mini_map_surface, 
# #                            (255, 0, 0),  # Red dot for player
# #                            (self.mini_map_size // 2, self.mini_map_size // 2), 
# #                            5)
        
# #         # Position the mini-map on the screen
# #         screen.blit(mini_map_surface, (self.screen_width - self.mini_map_size - 20, 200))
# # mini_map.py
# import pygame
# import math
# from dataclasses import dataclass
# from typing import List, Tuple
# from settings import SCREEN_HEIGHT,SCREEN_WIDTH
# @dataclass
# class RoutePoint:
#     name: str
#     coords: Tuple[float, float]  # Latitude, Longitude
#     description: str

# class Route:
#     def __init__(self, name: str, points: List[RoutePoint], level: int):
#         self.name = name
#         self.points = points
#         self.level = level
#         self.completed = False
#         self.current_point_index = 0
    
#     def get_current_point(self) -> RoutePoint:
#         return self.points[self.current_point_index]
    
#     def get_next_point(self) -> RoutePoint:
#         if self.current_point_index + 1 < len(self.points):
#             return self.points[self.current_point_index + 1]
#         return self.points[-1]

# class CanadianMiniMap:
#     def __init__(self):
#         # Initialize mini-map properties
#         self.radius = 90
#         self.expanded_radius = 200
#         self.is_expanded = False
#         self.position = (100,100)
#         self.border_color = (50, 50, 50)
#         self.background_color = (200, 200, 200, 180)
#         self.current_level = 1
#         self.font = None
#         self.route_color = (255, 0, 0)
#         self.completed_route_color = (0, 255, 0)
        
#         # Define all routes with real coordinates
#         self.routes = [
#             Route("Edmonton Downtown Circuit", [
#                 RoutePoint("Downtown Edmonton", (53.5461, -113.4938), "Start: Edmonton Downtown"),
#                 RoutePoint("West Edmonton Mall", (53.5225, -113.6242), "Checkpoint 1"),
#                 RoutePoint("Anthony Henday Ring", (53.5084, -113.5019), "Checkpoint 2"),
#                 RoutePoint("Downtown Edmonton", (53.5461, -113.4938), "Finish")
#             ], 1),
            
#             Route("Edmonton-Calgary Corridor", [
#                 RoutePoint("Edmonton South", (53.4947, -113.4774), "Start: Edmonton"),
#                 RoutePoint("Red Deer", (52.2690, -113.8116), "Checkpoint 1"),
#                 RoutePoint("Calgary North", (51.1784, -114.1084), "Finish")
#             ], 2),
            
#             Route("Banff Mountain Run", [
#                 RoutePoint("Calgary West", (51.0447, -114.0719), "Start: Calgary"),
#                 RoutePoint("Canmore", (51.0884, -115.3479), "Checkpoint 1"),
#                 RoutePoint("Banff", (51.1784, -115.5708), "Finish")
#             ], 3),
            
#             Route("Pacific Route", [
#                 RoutePoint("Banff", (51.1784, -115.5708), "Start: Banff"),
#                 RoutePoint("Kamloops", (50.6745, -120.3273), "Checkpoint 1"),
#                 RoutePoint("Vancouver", (49.2827, -123.1207), "Finish")
#             ], 4),
            
#             Route("Return to Edmonton", [
#                 RoutePoint("Calgary", (51.0447, -114.0719), "Start: Calgary"),
#                 RoutePoint("Red Deer", (52.2690, -113.8116), "Checkpoint 1"),
#                 RoutePoint("Edmonton", (53.5461, -113.4938), "Finish")
#             ], 5)
#         ]
        
#         self.current_route = self.routes[0]
        
#     def initialize_font(self):
#         if self.font is None:
#             self.font = pygame.font.Font(None, 20)
#             self.title_font = pygame.font.Font(None, 24)
    
#     def convert_coords_to_screen(self, lat: float, lon: float, radius: float) -> Tuple[int, int]:
#         # Convert geographic coordinates to screen coordinates
#         # Normalized based on Canadian coordinate bounds
#         LAT_MIN, LAT_MAX = 49.0, 54.0  # Approximate bounds for the route area
#         LON_MIN, LON_MAX = -123.5, -113.0
        
#         x = self.position[0] + ((lon - LON_MIN) / (LON_MAX - LON_MIN) - 0.5) * radius * 1.8
#         y = self.position[1] + ((LAT_MAX - lat) / (LAT_MAX - LAT_MIN) - 0.5) * radius * 1.8
        
#         return int(x), int(y)
    
#     def update_level(self, level: int):
#         """Update the current level and route"""
#         if 1 <= level <= len(self.routes):
#             self.current_level = level
#             self.current_route = self.routes[level - 1]
#             return True
#         return False
    
#     def draw(self, screen):
#         self.initialize_font()
#         current_radius = self.expanded_radius if self.is_expanded else self.radius
        
#         # Draw background
#         pygame.draw.circle(screen, self.background_color, self.position, current_radius)
#         pygame.draw.circle(screen, self.border_color, self.position, current_radius, 2)
        
#         # Draw title
#         title = f"Level {self.current_level}: {self.current_route.name}"
#         title_surface = self.title_font.render(title, True, (0, 0, 0))
#         title_rect = title_surface.get_rect(center=(self.position[0], self.position[1] - current_radius - 10))
#         screen.blit(title_surface, title_rect)
        
#         # Draw routes
#         for route in self.routes:
#             color = self.completed_route_color if route.completed else self.route_color
#             for i in range(len(route.points) - 1):
#                 start = self.convert_coords_to_screen(
#                     route.points[i].coords[0], 
#                     route.points[i].coords[1], 
#                     current_radius
#                 )
#                 end = self.convert_coords_to_screen(
#                     route.points[i + 1].coords[0], 
#                     route.points[i + 1].coords[1], 
#                     current_radius
#                 )
#                 pygame.draw.line(screen, color, start, end, 2)
        
#         # Draw points for current route
#         for point in self.current_route.points:
#             x, y = self.convert_coords_to_screen(point.coords[0], point.coords[1], current_radius)
            
#             # Draw larger point for current location
#             if point == self.current_route.get_current_point():
#                 pygame.draw.circle(screen, (255, 165, 0), (x, y), 6)  # Orange for current position
#             else:
#                 pygame.draw.circle(screen, (0, 0, 255), (x, y), 4)  # Blue for other points
            
#             # Draw labels if expanded
#             if self.is_expanded:
#                 label = self.font.render(point.name, True, (0, 0, 0))
#                 label_rect = label.get_rect(center=(x, y - 15))
#                 screen.blit(label, label_rect)
    
#     def toggle_expansion(self, mouse_pos):
#         distance = math.sqrt((mouse_pos[0] - self.position[0])**2 + 
#                            (mouse_pos[1] - self.position[1])**2)
        
#         if distance <= (self.expanded_radius if self.is_expanded else self.radius):
#             self.is_expanded = not self.is_expanded
#             return True
#         return False
    
#     def mark_current_level_complete(self):
#         """Mark the current route as completed and prepare for next level"""
#         self.current_route.completed = True
#         next_level = self.current_level + 1
#         if next_level <= len(self.routes):
#             self.update_level(next_level)
#             return True
#         return False
import pygame
import os

class MiniMap:
    def __init__(self, screen, level_manager):
        """
        Initialize the MiniMap for different game levels
        
        :param screen: Main game screen surface
        :param level_manager: Level management object to track current level
        """
        self.screen = screen
        self.level_manager = level_manager
        
        # Load minimap images for different levels
        self.minimap_images = {
            1: pygame.image.load("images/map/edm to Red deer.png"),
            2: pygame.image.load("images/map/edm to Red deer.png"),
            3: pygame.image.load("images/map/edm to Red deer.png"),
            4: pygame.image.load("images/map/edm to Red deer.png"),
            5: pygame.image.load("images/map/edm to Red deer.png")
        }
        
        # Resize images to a consistent size
        self.minimap_size = (200, 200)
        for level, img in self.minimap_images.items():
            self.minimap_images[level] = pygame.transform.scale(img, self.minimap_size)
        
        # Circular mask for minimap
        self.circular_mask = self._create_circular_mask(self.minimap_size[0], self.minimap_size[1])
        
        # Minimap position and state
        self.position = (pygame.display.get_surface().get_width() - 250, 50)
        self.is_visible = False
        self.is_interactive = False
        
        # Fuel station placement points (example coordinates, adjust as needed)
        self.fuel_station_points = {
            1: [(100, 150)],  # Example point for level 1
            2: [(150, 100)],  # Example point for level 2
            3: [(50, 100)],   # Example point for level 3
            4: [(75, 175)],   # Example point for level 4
            5: [(125, 50)]    # Example point for level 5
        }
        
        # Fuel station marker
        self.fuel_station_marker = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.fuel_station_marker, (255, 0, 0), (10, 10), 10)
    
    def _create_circular_mask(self, width, height):
        """
        Create a circular mask for the minimap
        
        :param width: Width of the mask
        :param height: Height of the mask
        :return: Circular surface mask
        """
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255), (width//2, height//2), min(width, height)//2)
        return mask
    
    def toggle_visibility(self):
        """Toggle minimap visibility"""
        self.is_visible = not self.is_visible
    
    def enable_interaction(self):
        """Enable minimap interaction after level completion"""
        self.is_interactive = True
    
    def disable_interaction(self):
        """Disable minimap interaction"""
        self.is_interactive = False
    
    def draw(self):
        """
        Draw the minimap if visible
        
        Draw the minimap as a circular image with optional fuel station markers
        """
        if not self.is_visible:
            return
        
        # Get current level's minimap
        current_level = self.level_manager.current_level + 1
        current_map = self.minimap_images.get(current_level)
        
        if current_map:
            # Create a surface with the same size as minimap
            map_surface = current_map.copy()
            
            # Apply circular mask
            map_surface.blit(self.circular_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Draw fuel station markers
            if current_level in self.fuel_station_points:
                for point in self.fuel_station_points[current_level]:
                    marker_pos = (point[0] - 10, point[1] - 10)
                    map_surface.blit(self.fuel_station_marker, marker_pos)
            
            # Blit the minimap
            self.screen.blit(map_surface, self.position)
    
    def handle_click(self, mouse_pos):
        """
        Handle click events on the minimap
        
        :param mouse_pos: Position of mouse click
        :return: Fuel station point if clicked, else None
        """
        if not (self.is_visible and self.is_interactive):
            return None
        
        # Adjust mouse position relative to minimap
        relative_x = mouse_pos[0] - self.position[0]
        relative_y = mouse_pos[1] - self.position[1]
        
        current_level = self.level_manager.current_level + 1
        
        # Check if clicked point is near a fuel station
        if current_level in self.fuel_station_points:
            for point in self.fuel_station_points[current_level]:
                if ((relative_x - point[0])**2 + (relative_y - point[1])**2) < 100:  # 10px radius
                    return point
        
        return None