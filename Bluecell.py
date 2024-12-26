# import pygame
# import math

# class BlueFuelCellShooter:
#     def __init__(self):
#         try:
#             # Load blue fuel cell projectile image
#             self.projectile_image = pygame.image.load("images/blue_fuel_cell_projectile.png").convert_alpha()
#             self.projectile_image = pygame.transform.scale(self.projectile_image, (30, 30))
#         except:
#             # Fallback if image not found
#             self.projectile_image = pygame.Surface((30, 30), pygame.SRCALPHA)
#             pygame.draw.circle(self.projectile_image, (0, 0, 255), (15, 15), 15)
        
#         self.projectiles = []
#         self.shoot_cooldown = 500  # milliseconds between shots
#         self.last_shoot_time = 0
    
#     def shoot(self, player_rect, target_line):
#         """
#         Shoot a blue fuel cell projectile
        
#         :param player_rect: Rectangle of the player's car
#         :param target_line: The line containing the enemy car to target
#         """
#         current_time = pygame.time.get_ticks()
        
#         # Check cooldown
#         if current_time - self.last_shoot_time < self.shoot_cooldown:
#             return False
        
#         # Create projectile
#         projectile = {
#             'x': player_rect.centerx,
#             'y': player_rect.centery,
#             'target_x': target_line.sprite_x,  # X position of enemy car
#             'target_y': target_line.Y,  # Y position on screen
#             'speed': 10,  # Projectile speed
#             'image': self.projectile_image
#         }
        
#         # Calculate trajectory
#         dx = projectile['target_x'] - projectile['x']
#         dy = projectile['target_y'] - projectile['y']
#         distance = math.sqrt(dx**2 + dy**2)
        
#         # Normalize and scale direction
#         projectile['dx'] = (dx / distance) * projectile['speed']
#         projectile['dy'] = (dy / distance) * projectile['speed']
        
#         self.projectiles.append(projectile)
#         self.last_shoot_time = current_time
#         return True
    
#     def update_and_draw_projectiles(self, screen, lines):
#         """
#         Update and draw blue fuel cell projectiles
        
#         :param screen: Pygame screen to draw on
#         :param lines: List of road lines to check for collisions
#         """
#         for projectile in self.projectiles[:]:
#             # Move projectile
#             projectile['x'] += projectile['dx']
#             projectile['y'] += projectile['dy']
            
#             # Draw projectile
#             screen.blit(projectile['image'], (projectile['x'], projectile['y']))
            
#             # Check collision with enemy cars
#             for line in lines:
#                 if line.sprite_type == "car":
#                     # Simple collision detection (you might want to refine this)
#                     car_rect = pygame.Rect(
#                         line.X - line.W, 
#                         line.Y, 
#                         line.W * 2, 
#                         50  # Approximate car height
#                     )
#                     projectile_rect = pygame.Rect(
#                         projectile['x'], 
#                         projectile['y'], 
#                         self.projectile_image.get_width(), 
#                         self.projectile_image.get_height()
#                     )
                    
#                     if car_rect.colliderect(projectile_rect):
#                         # Change car to blue (hit)
#                         line.sprite_type = "blue_hit_car"
#                         # Remove projectile
#                         self.projectiles.remove(projectile)
#                         break
            
#             # Remove projectile if it goes off screen
#             if (projectile['x'] < 0 or projectile['x'] > screen.get_width() or
#                 projectile['y'] < 0 or projectile['y'] > screen.get_height()):
#                 self.projectiles.remove(projectile)

class Bullet:
    def __init__(self, x, y, player_x, z=0):
        self.x = x  # Starting x position
        self.y = y  # Starting y position
        self.z = 0  # Initial z position 
        self.active = True
        self.speed = 10  # Speed of bullet movement
        self.max_distance = 1000  # Maximum distance the bullet can travel

    def update(self):
        # Move the bullet forward in z direction
        self.z += self.speed
        
        # Optionally adjust x to create a more dynamic inward movement
        self.x += 0.5  # Slight horizontal movement

        # Deactivate bullet if it travels too far
        if self.z > self.max_distance:
            self.active = False

# def shoot(self):   from 176
    #     # Create a bullet from the player's position
    #     bullet = Bullet(
    #         x=self.main_rect.x + self.main_rect.width // 2, 
    #         y=self.main_rect.y,
    #         player_x=self.player_x
    #     )
    #     self.bullets.append(bullet)

    # def draw_bullets(self,lines):
    #     for bullet in self.bullets:
    #         # Find the corresponding line for perspective projection
    #         line_index = int((self.pos + bullet.z) // seg_length)
    #         current_line = lines[line_index % len(lines)]

    #         # Project the bullet's position
    #         current_line.projection(self.player_x - bullet.x, 
    #                                 self.player_y + current_line.y, 
    #                                 self.pos - (len(lines) * seg_length if line_index >= len(lines) else 0))

    #         # Use the projected coordinates
    #         screen_x = current_line.X
    #         screen_y = current_line.Y

    #         # Adjust bullet size based on projection
    #         bullet_width = max(2, current_line.W * 0.3)
    #         bullet_height = max(4, current_line.W * 0.5)

    #         # Draw the bullet
    #         pygame.draw.rect(
    #             self.screen, 
    #             (255, 0, 0),  # Red color
    #             (screen_x, screen_y, bullet_width, bullet_height)
    #         )
     # Update bullets
            # self.update_bullets(lines)
            # Draw bullets
            # self.draw_bullets(lines)