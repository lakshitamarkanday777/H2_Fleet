# level_assets.py
import pygame
from typing import List, Dict

pygame.init()
class LevelAssets:
    def __init__(self):
        # Define backgrounds for each level
        self.backgrounds = {
            1: "images/level1/edm_street.png",      # City environment
            2: "images/level1/Red_deer1.jpg",    # Desert environment
            3: "images/backgrounds_1/My_Bg2_edited.png",    # Forest environment
            4: "images/level1/mountain-7064206_1280.jpg",      # Snow environment
            5: "images/level1/Vancouver_1.webp"      # Night city environment
        }
        
        # Define side sprites for each level
        self.level_sprites: Dict[int, List[str]] = {
            1: [  # City level sprites
                "images/3.png",
                "images/8.png"
            ],
            2: [  # Desert level sprites
                "images/6.png",
                
            ],
            3: [  # Forest level sprites
                "images/6.png",
                "images/10.png",
                "images/13.png",
                
            ],
            4: [  # Snow level sprites
                "images/6.png",
                "images/6.png","images/snow_tree.png"
                
            ],
            5: [  # Night city level sprites
                "images/12.png",
                
            ]
        }
        
        # Define road and environment colors for each level
        self.level_colors = {
            1: {  # Edm to Red Deer 
                "light_road": (100, 100, 100),
                "dark_road": (80, 80, 80),
                "light_grass": (16, 200, 16),
                "dark_grass": (0, 154, 0)
            },
            2: {  # Red Deer
                "light_road": (90, 90, 90),
                "dark_road": (70, 70, 70),
                "light_grass": (34, 139, 34),
                "dark_grass": (0, 100, 0)
            },
            3: {  # Desert
                "light_road": (230, 190, 150),
                "dark_road": (200, 160, 120),
                "light_grass": (238, 218, 130),
                "dark_grass": (218, 198, 110)
            },
            4: {  # Banff
                "light_road": (200, 200, 200),
                "dark_road": (180, 180, 180),
                "light_grass": (240, 240, 240),
                "dark_grass": (220, 220, 220)
            },
            5: {  # Vancouver
                "light_road": (50, 50, 50),
                "dark_road": (30, 30, 30),
                "light_grass": (0, 40, 0),
                "dark_grass": (0, 30, 0)
            }
        }
    
    def load_level_assets(self, level: int) -> tuple:
        """Load all assets for a specific level"""
        try:
            # Load background
            bg_image = pygame.image.load(self.backgrounds[level]).convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (1024, 500))
            
            # Load sprites
            sprites = []
            for sprite_path in self.level_sprites[level]:
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprites.append(sprite)
            
            # Get colors
            colors = self.level_colors[level]
            
            return bg_image, sprites, colors
        except KeyError:
            raise ValueError(f"Level {level} assets not found")
        except pygame.error as e:
            raise RuntimeError(f"Failed to load assets for level {level}: {e}")

