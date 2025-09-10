"""
Target class for the shooter game.
Handles target appearance, movement, and bouncing behavior.
"""

import pygame
import random


class Target:
    """Target object that bounces around the screen following SRP."""
    
    def __init__(self, screen_width, screen_height):
        """Initialize the target with random position and velocity."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Target properties
        self.radius = 30
        self.color = (255, 100, 100)  # Red color
        self.border_color = (255, 255, 255)  # White border
        self.border_width = 3
        
        # Initialize position and velocity
        self.gon_reset_position()
    
    def gon_reset_position(self):
        """Reset target to a random position with random velocity."""
        # Random starting position (avoiding edges)
        margin = self.radius + 10
        self.x = random.randint(margin, self.screen_width - margin)
        self.y = random.randint(margin, self.screen_height - margin)
        
        # Random velocity
        self.vel_x = random.choice([-1, 1]) * random.randint(3, 7)
        self.vel_y = random.choice([-1, 1]) * random.randint(3, 7)
    
    def gon_update(self):
        """Update target position and handle bouncing off walls."""
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Bounce off walls
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen_width:
            self.vel_x = -self.vel_x
            # Keep within bounds
            self.x = max(self.radius, min(self.screen_width - self.radius, self.x))
        
        if self.y - self.radius <= 0 or self.y + self.radius >= self.screen_height:
            self.vel_y = -self.vel_y
            # Keep within bounds
            self.y = max(self.radius, min(self.screen_height - self.radius, self.y))
    
    def gon_draw(self, screen):
        """Draw the target on the screen."""
        # Draw main circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw border
        pygame.draw.circle(screen, self.border_color, (int(self.x), int(self.y)), 
                          self.radius, self.border_width)
        
        # Draw crosshair for better visibility
        cross_size = self.radius // 2
        pygame.draw.line(screen, self.border_color, 
                        (self.x - cross_size, self.y), 
                        (self.x + cross_size, self.y), 2)
        pygame.draw.line(screen, self.border_color, 
                        (self.x, self.y - cross_size), 
                        (self.x, self.y + cross_size), 2)
    
    def gon_get_rect(self):
        """Get the bounding rectangle of the target for collision detection."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def gon_contains_point(self, point):
        """Check if a point is inside the target (circular collision detection)."""
        px, py = point
        distance_squared = (px - self.x) ** 2 + (py - self.y) ** 2
        return distance_squared <= self.radius ** 2
