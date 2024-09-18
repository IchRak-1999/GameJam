import arcade

class Player(arcade.Sprite):
    def __init__(self, x, y, speed, jump_strength, gravity):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.jump_strength = jump_strength
        self.gravity = gravity
        self.velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = False

    def update(self, up_pressed, down_pressed, left_pressed, right_pressed, platforms, delta_time):
        if up_pressed and self.is_on_ground:
            self.velocity_y = self.jump_strength
            self.is_jumping = True
            self.is_on_ground = False

        self.velocity_y += self.gravity
        self.center_y += self.velocity_y

        if self.center_y <= 30:
            self.center_y = 30
            self.is_on_ground = True
            self.velocity_y = 0
            self.is_jumping = False

        self.check_platform_collisions(platforms)

        if up_pressed:
            self.center_y += self.speed * delta_time
        if down_pressed:
            self.center_y -= self.speed * delta_time
        if left_pressed:
            self.center_x -= self.speed
        if right_pressed:
            self.center_x += self.speed

    def check_platform_collisions(self, platforms):
        self.is_on_ground = False
        for platform in platforms:
            if (self.center_y - 30 <= platform.sprite.center_y + platform.sprite.height / 2 and
                self.center_y - 30 >= platform.sprite.center_y - platform.sprite.height / 2 and
                self.center_x >= platform.sprite.center_x - platform.sprite.width / 2 and
                self.center_x <= platform.sprite.center_x + platform.sprite.width / 2):
                self.is_on_ground = True
                self.center_y = platform.sprite.center_y + platform.sprite.height / 2 + 30
                self.velocity_y = 0
                self.is_jumping = False

        if self.center_y <= 30:
            self.center_y = 30
            self.is_on_ground = True
            self.velocity_y = 0
            self.is_jumping = False

    def rewind(self, rewind_time_elapsed, mana):
        rewind_frame_count = int(rewind_time_elapsed * 60)
        if mana > 0 and rewind_frame_count < len(self.pos_hist):
            self.center_x, self.center_y = self.pos_hist[-rewind_frame_count - 1]
        else:
            return False
        return True
