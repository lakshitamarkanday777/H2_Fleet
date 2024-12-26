import pygame

class Countdown:
    def __init__(self, screen, font_path="images/joystix.ttf"):
        """
        Initialize Countdown with screen and font
        
        :param screen: Pygame screen surface
        :param font_path: Path to the font file
        """
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Initialize mixer
        pygame.mixer.init()
        
        # Load sounds
        self.countdown_sound = pygame.mixer.Sound("sound/countdown_beep.mp3")
        self.go_sound = pygame.mixer.Sound("sound/coin.wav")
        
        # Load font
        self.countdown_font = pygame.font.Font(font_path, 100)
    
    def show(self, 
             background_color="black", 
             countdown_color="white", 
             go_color="green"):
        """
        Display the countdown
        
        :param background_color: Color of the background during countdown
        :param countdown_color: Color of the countdown numbers
        :param go_color: Color of the "GO!" text
        :return: True when countdown is complete
        """
        for count in range(3, 0, -1):
            # Clear the screen
            self.screen.fill(background_color)
            
            # Render the countdown number
            countdown_text = self.countdown_font.render(str(count), True, countdown_color)
            text_rect = countdown_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
            
            # Play countdown sound
            self.countdown_sound.play()
            
            # Blit the countdown number
            self.screen.blit(countdown_text, text_rect)
            
            # Update the display
            pygame.display.flip()
            
            # Wait for 1 second
            pygame.time.wait(1000)
        
        # Final "GO!" message
        go_text = self.countdown_font.render("GO!", True, go_color)
        go_rect = go_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        
        # Play go sound
        self.go_sound.play()
        
        self.screen.blit(go_text, go_rect)
        pygame.display.flip()
        pygame.time.wait(500)
        
        return True