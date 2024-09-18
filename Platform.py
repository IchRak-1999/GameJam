from SolidObject import SolidObject
import arcade


SCREEN_WIDTH = 800
class Platform(SolidObject):
    def __init__(self, width, height, color, center_x, center_y):
        super().__init__(width, height, color, center_x, center_y)
        self.direction = 1

    def update(self, delta_time):
        self.sprite.center_x += self.direction * 100 * delta_time
        if self.sprite.center_x > SCREEN_WIDTH - self.sprite.width // 2 or self.sprite.center_x < self.sprite.width // 2:
            self.direction *= -1
