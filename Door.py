import arcade
from constants import SCREEN_WIDTH,SCREEN_HEIGHT

class Door(arcade.Sprite):
    def __init__(self, sprite):
        super().__init__()
        self.texture = sprite.texture  # Use the texture from the tilemap layer
        self.center_x = sprite.center_x
        self.center_y = sprite.center_y
        self.locked = True  # Door starts locked

    def unlock(self):
        arcade.draw_text("Level Completed!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=30, anchor_x="center",
                         multiline=True, width=SCREEN_WIDTH - 50)
