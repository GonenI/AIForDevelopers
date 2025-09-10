class Enemy {
    constructor(x, y, type = 'normal') {
        this.x = x;
        this.y = y;
        this.type = type;
        this.width = 30;
        this.height = 30;
        this.speed = 2;
        this.direction = 1;
        this.health = type === 'normal' ? 1 : 2;
        this.points = type === 'normal' ? 100 : 200;
        
        // Different colors for different enemy types
        this.color = type === 'normal' ? '#ff0000' : '#ff00ff';
    }

    update(canvas) {
        this.x += this.speed * this.direction;
        
        // Change direction if hitting canvas bounds
        if (this.x <= 0 || this.x + this.width >= canvas.width) {
            this.direction *= -1;
            this.y += 20; // Move down when changing direction
        }
    }

    draw(ctx) {
        // Draw enemy body
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(this.x + this.width/2, this.y);
        ctx.lineTo(this.x + this.width, this.y + this.height);
        ctx.lineTo(this.x, this.y + this.height);
        ctx.closePath();
        ctx.fill();
        
        // Add glow effect
        ctx.shadowBlur = 15;
        ctx.shadowColor = this.color;
        ctx.fill();
        ctx.shadowBlur = 0;
        
        // Draw eyes
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(this.x + this.width/3, this.y + this.height/2, 3, 0, Math.PI * 2);
        ctx.arc(this.x + this.width*2/3, this.y + this.height/2, 3, 0, Math.PI * 2);
        ctx.fill();
    }

    takeDamage() {
        this.health--;
        return this.health <= 0;
    }
} 