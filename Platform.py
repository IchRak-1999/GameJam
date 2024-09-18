from SolidObject import SolidObject
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Platform(SolidObject):
    def __init__(self, width, height, color, center_x, center_y, direction_x, direction_y):
        super().__init__(width, height, color, center_x, center_y)
        self.direction_x = direction_x
        self.direction_y = direction_y

    def update(self, delta_time):
        self.sprite.center_x += self.direction_x * 100 * delta_time
        self.sprite.center_y += self.direction_y * 100 * delta_time
        if self.sprite.center_x > SCREEN_WIDTH - self.sprite.width // 2 or self.sprite.center_x < self.sprite.width // 2:
            self.direction_x *= -1
        if self.sprite.center_y > SCREEN_HEIGHT - self.sprite.height // 2 or self.sprite.center_y < self.sprite.height // 2:
            self.direction_y *= -1
