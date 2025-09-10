class Projectile {
    constructor(x, y, targetX, targetY) {
        this.x = x;
        this.y = y;
        this.width = 4;
        this.height = 4;
        this.speed = 10;
        
        // Calculate direction vector
        const angle = Math.atan2(targetY - y, targetX - x);
        this.vx = Math.cos(angle) * this.speed;
        this.vy = Math.sin(angle) * this.speed;
        
        this.color = '#00ff00';
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
    }

    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.width / 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Add glow effect
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.fill();
        ctx.shadowBlur = 0;
    }

    isOutOfBounds(canvas) {
        return this.x < 0 || this.x > canvas.width || 
               this.y < 0 || this.y > canvas.height;
    }
} 