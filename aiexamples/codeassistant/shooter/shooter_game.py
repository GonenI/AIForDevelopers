import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Target:
    def __init__(self):
        self.radius = 30
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.speed = random.uniform(2, 5)
        self.direction = random.uniform(0, 2 * math.pi)
        self.color = RED
        
    def update(self):
        # Move the target
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # Bounce off walls
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.direction = math.pi - self.direction
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.direction = -self.direction
            
        # Keep target in bounds
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        
    def is_clicked(self, mouse_pos):
        distance = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
        return distance <= self.radius
        
    def respawn(self):
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.speed = random.uniform(2, 5)
        self.direction = random.uniform(0, 2 * math.pi)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shooter Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.target = Target()
        self.score = 0
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if self.target.is_clicked(mouse_pos):
                        self.score += 1
                        self.target.respawn()
                        # Increase speed slightly as score increases
                        self.target.speed = min(8, self.target.speed + 0.1)
                        
    def update(self):
        self.target.update()
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw target
        self.target.draw(self.screen)
        
        # Draw crosshair at mouse position
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, WHITE, 
                        (mouse_pos[0] - 10, mouse_pos[1]), 
                        (mouse_pos[0] + 10, mouse_pos[1]), 2)
        pygame.draw.line(self.screen, WHITE, 
                        (mouse_pos[0], mouse_pos[1] - 10), 
                        (mouse_pos[0], mouse_pos[1] + 10), 2)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw instructions
        instruction_text = self.font.render("Click on the red target to shoot!", True, WHITE)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 40))
        
        pygame.display.flip()
        
    def run(self):
        # Hide mouse cursor for better crosshair visibility
        pygame.mouse.set_visible(False)
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
