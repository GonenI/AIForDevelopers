const Utils = {
    // Random number generator between min and max (inclusive)
    random: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,

    // Check collision between two rectangles
    checkCollision: (rect1, rect2) => {
        return rect1.x < rect2.x + rect2.width &&
               rect1.x + rect1.width > rect2.x &&
               rect1.y < rect2.y + rect2.height &&
               rect1.y + rect1.height > rect2.y;
    },

    // Create a simple particle effect
    createParticles: (x, y, color, count, ctx) => {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 3 + 1;
            const size = Math.random() * 3 + 1;
            
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();
            
            // Animate particle
            const particle = {
                x, y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                size,
                life: 1
            };
            
            return particle;
        }
    }
}; 