class Player {
    constructor(canvas) {
        this.canvas = canvas;
        this.width = 40;
        this.height = 40;
        this.x = canvas.width / 2 - this.width / 2;
        this.y = canvas.height - this.height - 20;
        this.speed = 5;
        this.color = '#00ffff';
    }

    update(mouseX) {
        // Move player towards mouse position
        const targetX = mouseX - this.width / 2;
        const dx = targetX - this.x;
        
        if (Math.abs(dx) > this.speed) {
            this.x += Math.sign(dx) * this.speed;
        }
        
        // Keep player within canvas bounds
        this.x = Math.max(0, Math.min(this.canvas.width - this.width, this.x));
    }

    draw(ctx) {
        // Draw player ship
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(this.x + this.width/2, this.y);
        ctx.lineTo(this.x + this.width, this.y + this.height);
        ctx.lineTo(this.x, this.y + this.height);
        ctx.closePath();
        ctx.fill();
        
        // Add glow effect
        ctx.shadowBlur = 20;
        ctx.shadowColor = this.color;
        ctx.fill();
        ctx.shadowBlur = 0;
        
        // Draw engine glow
        ctx.fillStyle = '#ffff00';
        ctx.beginPath();
        ctx.moveTo(this.x + this.width/4, this.y + this.height);
        ctx.lineTo(this.x + this.width/2, this.y + this.height + 10);
        ctx.lineTo(this.x + this.width*3/4, this.y + this.height);
        ctx.closePath();
        ctx.fill();
    }

    shoot(targetX, targetY) {
        return new Projectile(
            this.x + this.width/2,
            this.y,
            targetX,
            targetY
        );
    }
} 