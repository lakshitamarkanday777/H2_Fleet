from settings import *
import pygame
import sys

pygame.init()

# for any images in the game to display
class Sprite(pygame.sprite.Sprite):

    def __init__(self, pos, image, groups):
        super().__init__(groups)

        self.image = image
        self.rect = self.image.get_frect(topleft=pos)

        self.hit_box=self.rect.copy()

# for any images in the game with animation
class Animated_sprite(Sprite):

    def __init__(self, pos, frames, groups, ani_speed):
        self.frames = frames  # got the animation list
        self.frame_index = 0  # animation index
        super().__init__(pos, self.frames[self.frame_index], groups)
        self.pos = pos
        self.animation_speed = ani_speed


    def animate(self):
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def update(self):
        self.animate()

# for text image to show in the game
class TextSprite:

    def __init__(self, text, pos, color, font):
        super().__init__()

        self.font =font
        self.text= text
        self.color = color
        self.image = self.font.render(self.text, "False", self.color)
        self.rect = self.image.get_rect(center=pos)

    def update(self, screen):

        screen.blit(self.image, self.rect)

# this class is used for display health bars, progress bars, ...
class Bars_Sprite(pygame.sprite.Sprite):
    # value is the existing parameter, max_value is the limit

    def __init__(self, pos, width, height, max_value, color):

        super().__init__()


        self.max_value= max_value
        self.color = color
        self.width = width
        self.height =height
        self.rect = pygame.Rect(pos[0],pos[1],width,height)

        self.bg_color = "grey"

    def update(self, screen, value):

        pygame.draw.rect(screen,self.bg_color,self.rect,0,3)
        ratio = value/self.max_value
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, ratio* self.width, self.height),
                         0, 3)

import pygame

class HealthBar:
    def __init__(self, x, y, width, height, max_health, font):
        """
        Initialize the health bar
        
        :param x: x-coordinate of health bar
        :param y: y-coordinate of health bar
        :param width: width of health bar
        :param height: height of health bar
        :param max_health: maximum health value
        :param font: pygame font for text
        """
        self.max_health = max_health
        self.current_health = max_health
        
        # Use the existing Bars_Sprite for the health bar
        self.bar = Bars_Sprite(
            pos=(x, y),
            width=width, 
            height=height, 
            max_value=max_health, 
            color=(0, 255, 0)  # Green color by default
        )
        
        # Create a text sprite for health percentage
        self.health_text = TextSprite(
            text=f"Health: {self.current_health}/{self.max_health}", 
            pos=(x + width // 2, y - 15),  # Position above the bar
            color=(255, 255, 255),  # Black color
            font=font
        )
        # Store font for potential re-rendering
        self.font = font
        # Collision damage
        self.collision_damage = 10

    def _update_text(self):
        """
        Update the health text sprite
        """
        # Recreate the text sprite to ensure it reflects current health
        self.health_text = TextSprite(
            text=f"Health: {self.current_health}/{self.max_health}", 
            pos=self.health_text.rect.center,  # Maintain previous position
            color=(255, 255, 255),  # Black color
            font=self.font
        )
    def take_damage(self, amount=None):
        """
        Reduce health when hit
        
        :param amount: amount of damage (defaults to collision_damage)
        :return: True if health reaches 0, False otherwise
        """
        damage = amount if amount is not None else self.collision_damage
        self.current_health = max(0, self.current_health - damage)
        
        # Update bar color based on health
        if self.current_health > self.max_health * 0.7:
            self.bar.color = (0, 255, 0)  # Green
        elif self.current_health > self.max_health * 0.3:
            self.bar.color = (255, 255, 0)  # Yellow
        else:
            self.bar.color = (255, 0, 0)  # Red
        self._update_text()
        
        return self.current_health <= 0

    def heal(self, amount):
        """
        Restore health
        
        :param amount: amount of health to restore
        """
        self.current_health = min(self.max_health, self.current_health + amount)
        
        
        # Reset color to green if health is restored
        self.bar.color = (0, 255, 0)    
        # Update health text
        self._update_text()   
    def _update_health_color(self):
        """Calculate health color based on current health"""
        health_percentage = self.current_health / self.max_health
        r = int(255 * (1 - health_percentage))
        g = int(255 * health_percentage)
        self.health_color = (r, g, 0)
    def draw(self, screen):
        """
        Draw the health bar on the screen
        
        :param screen: pygame screen surface
        """
        # Draw the bar
        self.bar.update(screen, self.current_health)
        
        # Draw the text
        self.health_text.update(screen)

    def is_alive(self):
        """
        Check if player is alive
        
        :return: True if health > 0, False otherwise
        """
        return self.current_health > 0


import pygame

# class FuelBar:
#     def __init__(self, x, y, width, height, max_fuel, font):
#         """
#         Initialize the fuel bar
        
#         :param x: x-coordinate of fuel bar
#         :param y: y-coordinate of fuel bar
#         :param width: width of fuel bar
#         :param height: height of fuel bar
#         :param max_fuel: maximum fuel value
#         :param font: pygame font for text
#         """
#         self.max_fuel = max_fuel
#         self.current_fuel = max_fuel
        
#         # Use the existing Bars_Sprite for the fuel bar
#         self.bar = Bars_Sprite(
#             pos=(x, y),
#             width=width, 
#             height=height, 
#             max_value=max_fuel, 
#             color=self.get_fuel_color()  # Set initial color based on full fuel
#         )
        
#         # Create a text sprite for fuel percentage
#         self.fuel_text = TextSprite(
#             text=f"Fuel: {self.current_fuel}/{self.max_fuel}", 
#             pos=(x + width // 2, y - 20),  # Position above the bar
#             color=(255, 255, 255),  # Black color
#             font=font
#         )
#         # Store font for potential re-rendering
#         self.font = font

#     def get_fuel_color(self):
#         """
#         Calculate the color of the fuel bar based on current fuel level.
        
#         :return: RGB color tuple
#         """
#         fuel_percentage = self.current_fuel / self.max_fuel
#         r = int(255 * (1 - fuel_percentage))  # Red increases as fuel decreases
#         g = int(255 * fuel_percentage)  # Green decreases as fuel decreases
#         return (r, g, 0)  # Return color as (R, G, B)

#     def _update_text(self):
#         """
#         Update the fuel text sprite to reflect the current fuel value.
#         """
#         # Recreate the text sprite to ensure it reflects current fuel
#         self.fuel_text = TextSprite(
#             text=f"Fuel: {int(self.current_fuel)}/{self.max_fuel}",  # Display as integer
#             pos=self.fuel_text.rect.center,  # Keep previous position
#             color=(255, 255, 255),  # White color for the text
#             font=self.font
#         )


#     def consume_fuel(self, amount=1):
#         """
#         Fast Decrement the fuel. Reduce the fuel instantly or by larger steps.

#         :param amount: amount of fuel to consume (default is 1)
#         """
#         if self.current_fuel == 100:
#             self.current_fuel = 99  # Directly decrement from 100 to 99
#         elif self.current_fuel > 0:
#             self.current_fuel -= amount  # Decrease the fuel instantly by 'amount'

#         # Ensure fuel value does not go below 0
#         self.current_fuel = max(0, self.current_fuel)

#         # Update the fuel bar color based on the current fuel level
#         self.bar.color = self.get_fuel_color()

#         # Update the fuel text
#         self._update_text()


#     def refill_fuel(self, amount):
#         """
#         Restore fuel
        
#         :param amount: amount of fuel to restore
#         """
#         self.current_fuel = min(self.max_fuel, self.current_fuel + amount)
#         self.bar.color = self.get_fuel_color()  # Update bar color based on current fuel
#         self._update_text()

#     def draw(self, screen):
#         """
#         Draw the fuel bar and text on the screen.

#         :param screen: pygame screen surface
#         """
#         # Draw the fuel bar
#         self.bar.update(screen, self.current_fuel)

#         # Draw the fuel text (percentage)
#         self.fuel_text.update(screen)