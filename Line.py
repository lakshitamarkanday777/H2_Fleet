import pygame
from settings import *
from Timer import Timer

pygame.init()
class Line:
    def __init__(self):
        
        self.x = self.y = self.z = 0.0  # 3d space position
        self.X = self.Y = self.W = 0.0  # 2d space position
        self.scale = 0.0  # scale
        self.curve = 0.0  # for curvature surface

        self.sprite_x = 0.0  # sprite x position
        self.adj_sprite_y = 0.0  # adjust sprite y position
        self.sprite: pygame.Surface = None
        self.sprite_rect = pygame.Rect = None
        self.sprite_type = None

        self.grass_color: pygame.Color = "black"
        self.rumble_color: pygame.Color = "black"
        self.road_color: pygame.Color = "black"
        self.font = pygame.font.Font("images/joystix.ttf", 50)
        
        self.collected = False
        self.is_refueling = False

        self.timer = Timer(2000)

    def drawSprite(self, draw_surface: pygame.Surface, main_rect, player_image,game):

        self.timer.update()
        collided = False

        if self.sprite is None:
            return

        w = self.sprite.get_width()
        h = self.sprite.get_height()

        destX = self.X + self.scale * self.sprite_x * SCREEN_WIDTH / 2
        destY = self.Y + 4

        destW = w * self.W / 266  # deformed size for width and height based on view from distance
        destH = h * self.W / 266

        destX += destW * self.sprite_x
        destY += destH * -1

        clipH = destY + destH - self.adj_sprite_y
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        # avoid scaling up images which causes lag
        if destW > w + 400:
            return

        scaled_sprite = pygame.transform.scale(self.sprite, (destW, destH))
        crop_surface = scaled_sprite.subsurface(0, 0, destW, destH - clipH)

        # draw sprites
        draw_surface.blit(crop_surface, (destX, destY))
        main_hitbox = main_rect.inflate(0, -10)  # shrink to fit with the actual
    
        if self.sprite_type == "car":
            self.sprite_rect = self.sprite.get_rect()
            self.sprite_rect.topleft = (destX, destY)
        
            self.hit_box = self.sprite_rect.copy()
            self.hit_box.size = (destW, destH)
        
            pygame.draw.rect(draw_surface, "red", self.hit_box, 2, 2)
        
            if self.hit_box.colliderect(main_hitbox):
                if not self.timer.active:  # Only process collision if timer is not active
                    print("Yes, collision !! ")
                    collided = True
                    self.timer.timer_on()
        
                    # # Ensure fuel deduction only occurs once
                    # if not hasattr(self, 'collision_processed'):
                    #     self.collision_processed = True  # Mark collision as processed
                    #     # Deduct fuel logic
                    #     if game.current_fuel < game.max_fuel and game.fuel_count >= 10:
                    #         game.current_fuel = min(game.max_fuel, game.current_fuel + 5.0)  # Refuel amount
                    #         game.fuel_count -= 10
                    #         print("Refueling...")
                    #         print(f"10 fuel cells deducted. Total fuel cells: {game.fuel_count}")
                    #     else:
                    #         print("Not enough fuel cells to deduct.")
        
                # if self.timer.active:
                #     text_surf = self.font.render("Collision!!!", True, "red")
                #     draw_surface.blit(text_surf, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            else:
                # Reset collision processing if no longer colliding
                if hasattr(self, 'collision_processed'):
                    del self.collision_processed  # Reset for next collision
        
        elif self.sprite_type == "fuel_cell":
        # Check for collision with fuel cell
            self.sprite_rect = self.sprite.get_rect()
            self.sprite_rect.topleft = (destX, destY)

            self.hit_box = self.sprite_rect.copy()
            self.hit_box.size = (destW, destH)

             # **Draw fuel cell hitbox (visual debugging)**
            # pygame.draw.rect(draw_surface, "blue", self.hit_box, 2, 2) was just to to check the collisions i ahd drawn

            if self.hit_box.colliderect(main_hitbox):
                if not self.collected:  # Check if the fuel cell has already been collected
                    print("Fuel cell collected!")  # Print the message only once
                    self.collected = True  # Mark the fuel cell as collected
                    collided = True  # Set collided to True if collected
            
                    # Increment the fuel count in the Game class
                    game.fuel_count += 1 
                    print(f"Total fuel cells collected: {game.fuel_count}")
                    # Remove the sprite from the screen
                    self.sprite = None  # This will remove the cell from rendering
                    self.sprite_type = None  # Reset the sprite type
                    # Play the fuel collection sound
                    game.fuel_collect_sound.play() 
            return collided
            
        if self.sprite_type == "fuel_station":
            # Create hitbox for fuel station
            self.sprite_rect = self.sprite.get_rect()
            self.sprite_rect.topleft = (destX, destY)

            self.hit_box = self.sprite_rect.copy()
            self.hit_box.size = (destW, destH)

            # Check collision with player
            if self.hit_box.colliderect(main_hitbox):
                print("Fuel Station Detected!")

                # Display refueling prompt
                font = pygame.font.Font("images/joystix.ttf", 50)
                text_surf = font.render("Press SPACE to Refuel", True, "white")
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                # Optional: Add a background to make text more readable
                bg_surf = pygame.Surface(text_rect.size)
                bg_surf.fill("black")
                bg_surf.set_alpha(200)
                bg_rect = bg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                draw_surface.blit(bg_surf, bg_rect)
                draw_surface.blit(text_surf, text_rect)

                # Check for refueling input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if not self.is_refueling:  # Only refuel if not already refueling
                        self.is_refueling = True  # Set flag to indicate refueling
                        
                        # Refuel logic
                        if game.current_fuel < game.max_fuel and game.fuel_count >= 10 :  # Ensure the fuel doesn't exceed max
                            game.current_fuel = game.max_fuel  # Refuel amount
                            
                            game.fuel_count -= 5
                            print("Refueling...")
                            print(f"10 fuel cells deducted. Total fuel cells: {game.fuel_count}")
                        else:
                            print("Not enough fuel cells to deduct.")
                    
                    game.draw_fuel_gauge()  # Calling the draw_fuel_gauge method to update the gauge
                
                collided = True
                self.is_refueling = False
        
        elif self.sprite_type == "maintenance_centre":
            self.sprite_rect = self.sprite.get_rect()
            # Create hitbox for maintenance centre
            self.sprite_rect.topleft = (destX, destY)
            self.hit_box = self.sprite_rect.copy()
            self.hit_box.size = (destW, destH)
            
            # Check collision with player
            if self.hit_box.colliderect(main_hitbox):
                print("Maintenance Centre Hit!")
                
                # Display "Press Enter to Repair" message
                font = pygame.font.Font("images/joystix.ttf", 50)
                text_surf = font.render("Press ENTER to Repair", True, "white")
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                
                # Optional: Add a background to make text more readable
                bg_surf = pygame.Surface(text_rect.size)
                bg_surf.fill("black")
                bg_surf.set_alpha(200)
                bg_rect = bg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                
                draw_surface.blit(bg_surf, bg_rect)
                draw_surface.blit(text_surf, text_rect)
                
                # Check for repair input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:  # Check if Enter key is pressed
                    # Increment the player's health
                    # game.health_bar.heal(20)  # Call heal method to update health bar
                    # game.open_repair_menu()
                    # Optional: Display repaired message
                    repair_text_surf = font.render("Repaired!", True, "black")
                    draw_surface.blit(repair_text_surf, 
                        (SCREEN_WIDTH // 2 - repair_text_surf.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 50))
                    
                    return True
                
                return True
            return False
        elif self.sprite_type == "red_cell":
            # Check for collision with red cell
            self.sprite_rect = self.sprite.get_rect()
            self.sprite_rect.topleft = (destX, destY)

            self.hit_box = self.sprite_rect.copy()
            self.hit_box.size = (destW, destH)

            # Optional: Draw hitbox (visual debugging)
            # pygame.draw.rect(draw_surface, "blue", self.hit_box, 2, 2)

            if self.hit_box.colliderect(main_hitbox):
                if not hasattr(self, 'collected'):
                    self.collected = False

                if not self.collected:
                    print("Red Cell Collected!")  # Print confirmation
                    self.collected = True
                    collided = True

                    # Increment red cell count in the Game class
                    game.red_fuel_cells_collected += 1 
                    game.total_red_cells_collected +=1
                    print(f"Total red cells collected: {game.red_fuel_cells_collected}")
                    # Remove the sprite from the screen
                    self.sprite = None  # This will remove the cell from rendering
                    self.sprite_type = None  # Reset the sprite type
                    # Check if 5 red cells are collected
                    if game.red_fuel_cells_collected >= 5:
                        # Get a random message
                        message = game.red_fuel_cell_manager.get_message()

                        # Pause the game and show message
                        game.show_red_cell_message(message)

                        # Reset the counter
                        game.red_fuel_cells_collected = 0
            return collided   
        draw_surface.blit(player_image, main_rect)
        pygame.draw.rect(draw_surface, "green", main_hitbox, 2, 2)
        if collided:
            return True
        else:
            return False
    
    def reset_fuel_cell(self):
        self.collected = False
        self.sprite = None
        self.sprite_type = None
    
    def projection(self, camX: int, camY: int, camZ: int):
        self.scale = cam_depth / (self.z - camZ)
        # getting 2D space position and convert to 3D projection

        self.X = (1 + self.scale * (self.x - camX)) * SCREEN_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * SCREEN_HEIGHT / 2
        self.W = self.scale * road_width * SCREEN_WIDTH / 2
    
    def check_red_cell_collision(self, player_rect):
        """
        Check if the red cell collides with the player's car

        :param player_rect: Rectangle of the player's car
        :return: Boolean indicating collision
        """
        if self.sprite and self.sprite_type == "red_cell":
            # Create a rect for the red cell based on its position on the screen
            red_cell_rect = self.sprite.get_rect(
                center=(
                    self.X + self.sprite_x * self.W, 
                    self.Y
                )
            )

            # Check for collision
            return player_rect.colliderect(red_cell_rect)

        return False