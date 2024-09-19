import arcade

class Sounds:
    def __init__(self):
        self.music = None

    def setup(self, music_path, volume):
        self.music = arcade.load_sound(music_path)
        arcade.play_sound(self.music, volume, looping=True)

    def stop_music(self):
        if self.music:
            arcade.stop_sound(self.music)
