"""
Score class for the shooter game.
Handles score tracking and display.
"""

import pygame


class Score:
    """Score manager following SRP - responsible only for score tracking and display."""
    
    def __init__(self):
        """Initialize the score system."""
        self.score = 0
        self.font_size = 36
        self.font = None
        self.gon_init_font()
        
        # Colors
        self.text_color = (255, 255, 255)  # White
        self.shadow_color = (0, 0, 0)      # Black shadow
        
        # Position
        self.position = (20, 20)  # Top-left corner
    
    def gon_init_font(self):
        """Initialize the font for score display."""
        try:
            self.font = pygame.font.Font(None, self.font_size)
        except:
            # Fallback to system default font
            self.font = pygame.font.SysFont('Arial', self.font_size)
    
    def gon_add_point(self):
        """Add one point to the score."""
        self.score += 1
    
    def gon_add_points(self, points):
        """Add multiple points to the score."""
        self.score += points
    
    def gon_reset_score(self):
        """Reset the score to zero."""
        self.score = 0
    
    def gon_get_score(self):
        """Get the current score."""
        return self.score
    
    def gon_draw(self, screen):
        """Draw the score on the screen."""
        # Create score text
        score_text = f"Score: {self.score}"
        
        # Render text with shadow effect
        shadow_surface = self.font.render(score_text, True, self.shadow_color)
        text_surface = self.font.render(score_text, True, self.text_color)
        
        # Draw shadow (offset by 2 pixels)
        shadow_pos = (self.position[0] + 2, self.position[1] + 2)
        screen.blit(shadow_surface, shadow_pos)
        
        # Draw main text
        screen.blit(text_surface, self.position)
    
    def gon_draw_with_stats(self, screen, player_stats):
        """Draw score along with additional player statistics."""
        # Main score
        score_text = f"Score: {self.score}"
        
        # Additional stats
        stats_text = f"Shots: {player_stats['shots_fired']} | Accuracy: {player_stats['accuracy']:.1f}%"
        
        # Render main score
        shadow_surface = self.font.render(score_text, True, self.shadow_color)
        text_surface = self.font.render(score_text, True, self.text_color)
        
        # Draw shadow and main text for score
        shadow_pos = (self.position[0] + 2, self.position[1] + 2)
        screen.blit(shadow_surface, shadow_pos)
        screen.blit(text_surface, self.position)
        
        # Render and draw stats (smaller font)
        stats_font = pygame.font.Font(None, 24)
        stats_shadow = stats_font.render(stats_text, True, self.shadow_color)
        stats_surface = stats_font.render(stats_text, True, self.text_color)
        
        stats_y = self.position[1] + self.font_size + 5
        stats_shadow_pos = (self.position[0] + 2, stats_y + 2)
        stats_pos = (self.position[0], stats_y)
        
        screen.blit(stats_shadow, stats_shadow_pos)
        screen.blit(stats_surface, stats_pos)
    
    def gon_set_position(self, x, y):
        """Set the position where the score will be displayed."""
        self.position = (x, y)
    
    def gon_get_high_score_text(self):
        """Get formatted text for displaying high score information."""
        return f"High Score: {self.score}"
