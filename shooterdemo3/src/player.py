"""
Player class for the shooter game.
Handles player input and shooting mechanics.
"""

import pygame


class Player:
    """Player controller following SRP - responsible only for player actions."""
    
    def __init__(self):
        """Initialize the player."""
        self.shots_fired = 0
        self.hits = 0
        
        # Visual feedback for shots
        self.shot_effects = []  # List to store shot effect positions and timers
    
    def gon_shoot(self, mouse_pos, target_rect):
        """
        Handle shooting action at mouse position.
        Returns True if target was hit, False otherwise.
        """
        self.shots_fired += 1
        
        # Add visual effect for the shot
        self.gon_add_shot_effect(mouse_pos)
        
        # Check if shot hit the target
        # We need to check against the target object directly for circular collision
        return False  # This will be handled by the target's contains_point method
    
    def gon_shoot_at_target(self, mouse_pos, target):
        """
        Handle shooting action with proper target collision detection.
        Returns True if target was hit, False otherwise.
        """
        self.shots_fired += 1
        
        # Add visual effect for the shot
        self.gon_add_shot_effect(mouse_pos)
        
        # Check if shot hit the target using circular collision
        hit = target.gon_contains_point(mouse_pos)
        if hit:
            self.hits += 1
        
        return hit
    
    def gon_add_shot_effect(self, position):
        """Add a visual effect at the shot position."""
        # Add position and timer (effect lasts for 0.3 seconds = 18 frames at 60 FPS)
        self.shot_effects.append([list(position), 18])
    
    def gon_update_shot_effects(self):
        """Update and remove expired shot effects."""
        # Decrease timer for each effect and remove expired ones
        self.shot_effects = [[pos, timer - 1] for pos, timer in self.shot_effects if timer > 1]
    
    def gon_draw_shot_effects(self, screen):
        """Draw visual effects for recent shots."""
        for pos, timer in self.shot_effects:
            # Calculate alpha based on remaining timer (fade out effect)
            alpha = int((timer / 18) * 255)
            
            # Create a surface for the effect with alpha
            effect_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            
            # Draw crosshair effect
            color_with_alpha = (255, 255, 0, alpha)  # Yellow with transparency
            pygame.draw.line(effect_surface, color_with_alpha[:3], (5, 10), (15, 10), 2)
            pygame.draw.line(effect_surface, color_with_alpha[:3], (10, 5), (10, 15), 2)
            
            # Draw circle around crosshair
            pygame.draw.circle(effect_surface, color_with_alpha[:3], (10, 10), 8, 2)
            
            # Blit to screen
            screen.blit(effect_surface, (pos[0] - 10, pos[1] - 10))
    
    def gon_get_accuracy(self):
        """Calculate and return shooting accuracy percentage."""
        if self.shots_fired == 0:
            return 0.0
        return (self.hits / self.shots_fired) * 100
    
    def gon_get_stats(self):
        """Get player statistics as a dictionary."""
        return {
            'shots_fired': self.shots_fired,
            'hits': self.hits,
            'accuracy': self.gon_get_accuracy()
        }
