import arcade

class SolidObject:
    def __init__(self, width, height, color, center_x, center_y):
        self.sprite = arcade.SpriteSolidColor(width, height, color)
        self.sprite.center_x = center_x
        self.sprite.center_y = center_y

    def draw(self):
        self.sprite.draw()

    def update(self, delta_time):
        pass 
