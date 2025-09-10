"""
Main game controller class for the shooter game.
Handles the game loop, initialization, and coordination between game components.
"""

import pygame
import sys
from src.target import Target
from src.player import Player
from src.score import Score


class Game:
    """Main game controller following SRP - responsible only for game flow and coordination."""
    
    def __init__(self):
        """Initialize the game with default settings."""
        self.gon_init_pygame()
        self.gon_setup_display()
        self.gon_create_game_objects()
        self.running = True
        self.clock = pygame.time.Clock()
    
    def gon_init_pygame(self):
        """Initialize pygame modules."""
        pygame.init()
        pygame.mixer.init()
    
    def gon_setup_display(self):
        """Set up the game display window."""
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Shooter Game - Hit the Target!")
        
        # Colors
        self.bg_color = (30, 30, 50)  # Dark blue background
    
    def gon_create_game_objects(self):
        """Create all game objects."""
        self.target = Target(self.width, self.height)
        self.player = Player()
        self.score = Score()
    
    def gon_handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    hit = self.player.gon_shoot_at_target(mouse_pos, self.target)
                    if hit:
                        self.score.gon_add_point()
                        self.target.gon_reset_position()
    
    def gon_update_game_state(self):
        """Update all game objects."""
        self.target.gon_update()
        self.player.gon_update_shot_effects()
    
    def gon_render(self):
        """Render all game objects to the screen."""
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw game objects
        self.target.gon_draw(self.screen)
        self.player.gon_draw_shot_effects(self.screen)
        
        # Draw score with player stats
        player_stats = self.player.gon_get_stats()
        self.score.gon_draw_with_stats(self.screen, player_stats)
        
        # Update display
        pygame.display.flip()
    
    def gon_run(self):
        """Main game loop."""
        while self.running:
            self.gon_handle_events()
            self.gon_update_game_state()
            self.gon_render()
            self.clock.tick(60)  # 60 FPS
        
        self.gon_quit()
    
    def gon_quit(self):
        """Clean up and quit the game."""
        pygame.quit()
        sys.exit()
