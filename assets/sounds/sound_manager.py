# assets/sounds/sound_manager.py
import pygame
import os
from pathlib import Path
from assets.config import SOUND_ENABLED

class SoundManager:
    def __init__(self):
        """Initialize the sound manager and load all game sounds."""
        self.sounds = {}
        self.music_tracks = {}
        self.sound_enabled = SOUND_ENABLED
        self.music_enabled = SOUND_ENABLED
        self.sound_volume = 0.7
        self.music_volume = 0.5
        
        # Only initialize mixer and load sounds if sound is enabled
        if SOUND_ENABLED:
            # Initialize pygame mixer if not already done
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects and music tracks."""
        base_path = Path(__file__).parent
        
        # Define sound file mappings
        sound_files = {
            'explosion': 'explosion.wav',
            'shoot': 'shoot.wav',
            'collision': 'collision.wav',
            'powerup': 'powerup.wav',
            'game_over': 'game_over.wav',
            'victory': 'victory.wav',
            'asteroid_hit': 'asteroid_hit.wav',
            'ship_hit': 'ship_hit.wav'
        }
        
        # Load sound effects
        sfx_path = base_path / 'sfx'
        for sound_name, filename in sound_files.items():
            file_path = sfx_path / filename
            if file_path.exists():
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(str(file_path))
                    self.sounds[sound_name].set_volume(self.sound_volume)
                except pygame.error as e:
                    print(f"Warning: Could not load sound {filename}: {e}")
            else:
                print(f"Warning: Sound file not found: {file_path}")
        
        # Define music file mappings
        music_files = {
            'background': 'background.wav',  # Using WAV for now
            'menu': 'menu.wav',
            'game_over': 'game_over.wav'
        }
        
        # Load music tracks
        music_path = base_path / 'music'
        for music_name, filename in music_files.items():
            file_path = music_path / filename
            if file_path.exists():
                self.music_tracks[music_name] = str(file_path)
            else:
                print(f"Warning: Music file not found: {file_path}")
    
    def play_sound(self, sound_name):
        """Play a sound effect."""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"Error playing sound {sound_name}: {e}")
        else:
            print(f"Warning: Sound '{sound_name}' not found")
    
    def play_music(self, music_name, loops=-1):
        """Play background music."""
        if not self.music_enabled:
            return
        
        if music_name in self.music_tracks:
            try:
                pygame.mixer.music.load(self.music_tracks[music_name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
            except pygame.error as e:
                print(f"Error playing music {music_name}: {e}")
        else:
            print(f"Warning: Music '{music_name}' not found")
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """Pause background music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause background music."""
        pygame.mixer.music.unpause()
    
    def set_sound_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self.sound_enabled = not self.sound_enabled
    
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled:
            self.stop_music()
    
    def cleanup(self):
        """Clean up sound resources."""
        if SOUND_ENABLED and pygame.mixer.get_init():
            pygame.mixer.quit()
