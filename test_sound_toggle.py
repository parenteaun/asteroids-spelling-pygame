#!/usr/bin/env python3
"""
Test script to demonstrate sound toggle functionality.
"""

import pygame
from assets.sounds.sound_manager import SoundManager
from assets.config import SOUND_ENABLED

def test_sound_toggle():
    """Test the sound toggle functionality."""
    print("=== Sound Toggle Test ===")
    print(f"Current SOUND_ENABLED setting: {SOUND_ENABLED}")
    
    # Initialize pygame
    pygame.init()
    
    # Create sound manager
    print("\nCreating SoundManager...")
    sound_manager = SoundManager()
    
    print(f"Sound enabled: {sound_manager.sound_enabled}")
    print(f"Music enabled: {sound_manager.music_enabled}")
    
    # Test sound playback
    print("\nTesting sound playback...")
    sound_manager.play_sound('shoot')
    print("  - shoot sound triggered")
    
    sound_manager.play_music('background')
    print("  - background music triggered")
    
    # Test volume controls
    print("\nTesting volume controls...")
    sound_manager.set_sound_volume(0.5)
    sound_manager.set_music_volume(0.3)
    print("  - Volumes adjusted")
    
    # Test toggle functionality
    print("\nTesting toggle functionality...")
    original_sound = sound_manager.sound_enabled
    original_music = sound_manager.music_enabled
    
    sound_manager.toggle_sound()
    print(f"  - Sound toggled from {original_sound} to {sound_manager.sound_enabled}")
    
    sound_manager.toggle_music()
    print(f"  - Music toggled from {original_music} to {sound_manager.music_enabled}")
    
    # Cleanup
    print("\nCleaning up...")
    sound_manager.cleanup()
    pygame.quit()
    
    print("\n=== Test Complete ===")
    print("To disable sound globally, set SOUND_ENABLED = False in assets/config.py")

if __name__ == "__main__":
    test_sound_toggle()
