class AudioManager {
    constructor() {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.sounds = {};
        this.loadSounds();
    }

    loadSounds() {
        // Create oscillator-based sounds
        this.sounds.shoot = () => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.type = 'square';
            oscillator.frequency.setValueAtTime(880, this.audioContext.currentTime);
            gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.1);
            
            oscillator.start();
            oscillator.stop(this.audioContext.currentTime + 0.1);
        };

        this.sounds.explosion = () => {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.type = 'sawtooth';
            oscillator.frequency.setValueAtTime(100, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(50, this.audioContext.currentTime + 0.3);
            gainNode.gain.setValueAtTime(0.5, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
            
            oscillator.start();
            oscillator.stop(this.audioContext.currentTime + 0.3);
        };
    }

    play(soundName) {
        if (this.sounds[soundName]) {
            this.sounds[soundName]();
        }
    }
} 