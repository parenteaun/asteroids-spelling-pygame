#!/usr/bin/env python3
"""
Generate simple test sound files for the asteroids game.
This script creates basic sine wave sounds for testing purposes.
"""

import numpy as np
import wave
import struct
import os
from pathlib import Path

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave_data

def save_wav(filename, wave_data, sample_rate=44100):
    """Save wave data as a WAV file."""
    # Convert Path object to string
    filename_str = str(filename)
    with wave.open(filename_str, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Convert to 16-bit integers
        wave_data = (wave_data * 32767).astype(np.int16)
        
        # Write the data
        wav_file.writeframes(wave_data.tobytes())

def main():
    """Generate test sound files."""
    # Create directories if they don't exist
    sfx_dir = Path("assets/sounds/sfx")
    music_dir = Path("assets/sounds/music")
    
    sfx_dir.mkdir(parents=True, exist_ok=True)
    music_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sound effects
    sounds = {
        'explosion': (100, 0.5),      # Low frequency, short duration
        'shoot': (800, 0.1),          # High frequency, very short
        'collision': (200, 0.3),      # Medium frequency, short
        'powerup': (600, 0.2),        # Medium-high frequency, short
        'game_over': (150, 1.0),      # Low frequency, longer
        'victory': (400, 0.8),        # Medium frequency, longer
        'asteroid_hit': (300, 0.2),   # Medium frequency, short
        'ship_hit': (250, 0.4),       # Medium-low frequency, short
    }
    
    print("Generating sound effects...")
    for sound_name, (freq, duration) in sounds.items():
        filename = sfx_dir / f"{sound_name}.wav"
        wave_data = generate_sine_wave(freq, duration)
        save_wav(filename, wave_data)
        print(f"  Created: {filename}")
    
    # Generate background music (longer, more complex)
    print("Generating background music...")
    
    # Create a simple melody for background music
    notes = [
        (440, 0.5),  # A
        (494, 0.5),  # B
        (523, 0.5),  # C
        (587, 0.5),  # D
        (659, 0.5),  # E
        (698, 0.5),  # F
        (784, 0.5),  # G
    ]
    
    # Generate 10 seconds of music
    sample_rate = 44100
    total_duration = 10.0
    music_data = np.array([])
    
    t = 0
    while t < total_duration:
        for freq, duration in notes:
            if t >= total_duration:
                break
            note_data = generate_sine_wave(freq, duration, sample_rate, 0.1)
            music_data = np.concatenate([music_data, note_data])
            t += duration
    
    # Save as WAV (we'll use WAV for music too for simplicity)
    music_wav = music_dir / "background.wav"
    save_wav(music_wav, music_data)
    print(f"  Created: {music_wav}")
    
    # Create placeholder files for other music
    for music_name in ['menu', 'game_over']:
        filename = music_dir / f"{music_name}.wav"
        wave_data = generate_sine_wave(300, 2.0, 44100, 0.2)
        save_wav(filename, wave_data)
        print(f"  Created: {filename}")
    
    print("\nTest sound files generated successfully!")
    print("Note: These are simple sine wave sounds for testing.")
    print("Replace them with proper sound effects and music for the final game.")

if __name__ == "__main__":
    main()
