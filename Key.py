import arcade

class Key(arcade.Sprite):
    def __init__(self, sprite):
        super().__init__()
        self.texture = sprite.texture  # Use the texture from the tilemap layer
        self.center_x = sprite.center_x
        self.center_y = sprite.center_y