# music.py
import random
import threading
import time
import pygame

class MusicPlayer:
    def __init__(self):
        self.tracks = [
            "music/Track01.mp4",
            "music/Track02.mp4",
            "music/Track03.mp4",
            "music/Track04.mp4",
            "music/Track05.mp4",
            "music/Track06.mp4",
            "music/Track07.mp4",
            "music/Track08.mp4"
        ]
        self.playing = False
        pygame.mixer.init()

    def play_random_music(self):
        if self.playing:
            return
        def play_loop():
            self.playing = True
            while self.playing:
                track = random.choice(self.tracks)
                print(f"Now playing: {track}")
                pygame.mixer.music.load(track)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    if not self.playing:
                        pygame.mixer.music.stop()
                        return
                    time.sleep(0.1)
        threading.Thread(target=play_loop, daemon=True).start()

    def stop_music(self):
        self.playing = False
        pygame.mixer.music.stop()
        print("Music stopped.")

# Create one global instance
music_player = MusicPlayer()

