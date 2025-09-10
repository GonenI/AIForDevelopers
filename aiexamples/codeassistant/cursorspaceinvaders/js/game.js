class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.scoreElement = document.getElementById('scoreValue');
        
        // Set canvas size
        this.canvas.width = 800;
        this.canvas.height = 600;
        
        // Initialize game objects
        this.player = new Player(this.canvas);
        this.enemies = [];
        this.projectiles = [];
        this.particles = [];
        this.audioManager = new AudioManager();
        
        // Game state
        this.score = 0;
        this.gameOver = false;
        this.gameWon = false;
        this.mouseX = 0;
        this.mouseY = 0;
        
        // Initialize enemies
        this.initializeEnemies();
        
        // Event listeners
        this.canvas.addEventListener('mousemove', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            this.mouseX = e.clientX - rect.left;
            this.mouseY = e.clientY - rect.top;
        });
        
        this.canvas.addEventListener('click', (e) => {
            if (!this.gameOver && !this.gameWon) {
                const rect = this.canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                this.shoot(x, y);
            }
        });
        
        // Start game loop
        this.lastTime = 0;
        this.animate(0);
    }
    
    initializeEnemies() {
        const rows = 3;
        const cols = 8;
        const spacing = 60;
        
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const x = col * spacing + 50;
                const y = row * spacing + 50;
                const type = row === 0 ? 'special' : 'normal';
                this.enemies.push(new Enemy(x, y, type));
            }
        }
    }
    
    shoot(targetX, targetY) {
        const projectile = this.player.shoot(targetX, targetY);
        this.projectiles.push(projectile);
        this.audioManager.play('shoot');
    }
    
    update(deltaTime) {
        if (this.gameOver || this.gameWon) return;
        
        // Update player
        this.player.update(this.mouseX);
        
        // Update enemies
        this.enemies.forEach(enemy => enemy.update(this.canvas));
        
        // Update projectiles
        this.projectiles = this.projectiles.filter(projectile => {
            projectile.update();
            return !projectile.isOutOfBounds(this.canvas);
        });
        
        // Update particles
        this.particles = this.particles.filter(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life -= 0.02;
            return particle.life > 0;
        });
        
        // Check collisions
        this.checkCollisions();
        
        // Check game over
        if (this.enemies.some(enemy => enemy.y + enemy.height >= this.player.y)) {
            this.gameOver = true;
        }
        
        // Check win condition
        if (this.enemies.length === 0) {
            this.gameWon = true;
            // Create victory particles
            for (let i = 0; i < 50; i++) {
                this.particles.push(Utils.createParticles(
                    Utils.random(0, this.canvas.width),
                    Utils.random(0, this.canvas.height),
                    '#ffff00',
                    1,
                    this.ctx
                ));
            }
        }
    }
    
    checkCollisions() {
        // Check projectile-enemy collisions
        this.projectiles.forEach((projectile, projectileIndex) => {
            this.enemies.forEach((enemy, enemyIndex) => {
                if (Utils.checkCollision(projectile, enemy)) {
                    // Remove projectile
                    this.projectiles.splice(projectileIndex, 1);
                    
                    // Damage enemy
                    if (enemy.takeDamage()) {
                        // Remove enemy and add score
                        this.enemies.splice(enemyIndex, 1);
                        this.score += enemy.points;
                        this.scoreElement.textContent = this.score;
                        
                        // Create explosion particles
                        for (let i = 0; i < 10; i++) {
                            this.particles.push(Utils.createParticles(
                                enemy.x + enemy.width/2,
                                enemy.y + enemy.height/2,
                                enemy.color,
                                1,
                                this.ctx
                            ));
                        }
                        
                        this.audioManager.play('explosion');
                    }
                    
                    return;
                }
            });
        });
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw game objects
        this.player.draw(this.ctx);
        this.enemies.forEach(enemy => enemy.draw(this.ctx));
        this.projectiles.forEach(projectile => projectile.draw(this.ctx));
        
        // Draw particles
        this.particles.forEach(particle => {
            this.ctx.fillStyle = `rgba(255, 255, 255, ${particle.life})`;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        // Draw game over or victory screen
        if (this.gameOver || this.gameWon) {
            this.ctx.fillStyle = '#fff';
            this.ctx.font = '48px Arial';
            this.ctx.textAlign = 'center';
            
            if (this.gameWon) {
                this.ctx.fillText('Victory!', this.canvas.width/2, this.canvas.height/2);
                this.ctx.font = '24px Arial';
                this.ctx.fillText(`Final Score: ${this.score}`, this.canvas.width/2, this.canvas.height/2 + 40);
                this.ctx.fillText('You saved Earth from the invaders!', this.canvas.width/2, this.canvas.height/2 + 80);
            } else {
                this.ctx.fillText('Game Over', this.canvas.width/2, this.canvas.height/2);
                this.ctx.font = '24px Arial';
                this.ctx.fillText(`Final Score: ${this.score}`, this.canvas.width/2, this.canvas.height/2 + 40);
            }
        }
    }
    
    animate(currentTime) {
        const deltaTime = (currentTime - this.lastTime) / 1000;
        this.lastTime = currentTime;
        
        this.update(deltaTime);
        this.draw();
        
        requestAnimationFrame((time) => this.animate(time));
    }
}

// Start the game when the page loads
window.addEventListener('load', () => {
    new Game();
}); 