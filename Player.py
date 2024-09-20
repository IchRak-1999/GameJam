import arcade

class Player(arcade.Sprite):
    def __init__(self, x, y, speed, jump_strength, idle_right_sprite_path, run_right_sprite_path, idle_left_sprite_path, run_left_sprite_path, scale, animation_speed):
        super().__init__(scale=scale)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.jump_strength = jump_strength
        self.velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = False
        self.animation_speed = animation_speed
        self.scale = scale
        self.is_facing_right = True

        self.idle_right_textures = arcade.load_spritesheet(idle_right_sprite_path, sprite_width=93, sprite_height=112, columns=5, count=5)
        self.run_right_textures = arcade.load_spritesheet(run_right_sprite_path, sprite_width=93, sprite_height=112, columns=8, count=8)
        self.idle_left_textures = arcade.load_spritesheet(idle_left_sprite_path, sprite_width=93, sprite_height=112, columns=5, count=5)
        self.run_left_textures = arcade.load_spritesheet(run_left_sprite_path, sprite_width=93, sprite_height=112, columns=8, count=8)

        self.current_texture_index = 0
        self.is_running = False
        self.texture = self.idle_right_textures[self.current_texture_index]

    def update(self, up_pressed, down_pressed, left_pressed, right_pressed, delta_time):
        if up_pressed and self.is_on_ground:
            self.velocity_y = self.jump_strength
            self.is_jumping = True
            self.is_on_ground = False

        self.center_y += self.velocity_y

        if self.center_y <= 30:
            self.center_y = 30
            self.is_on_ground = True
            self.velocity_y = 0
            self.is_jumping = False

        if left_pressed:
            self.center_x -= self.speed
            self.is_running = True
            self.is_facing_right = False
        elif right_pressed:
            self.center_x += self.speed
            self.is_running = True
            self.is_facing_right = True
        else:
            self.is_running = False

        self.update_animation(delta_time)

    def update_animation(self, delta_time):
        self.current_texture_index += self.animation_speed
        if self.is_running:
            if self.current_texture_index >= len(self.run_right_textures):
                self.current_texture_index = 0
            if self.is_facing_right:
                self.texture = self.run_right_textures[int(self.current_texture_index)]
            else:
                self.texture = self.run_left_textures[int(self.current_texture_index)]
        else:
            if self.current_texture_index >= len(self.idle_right_textures):
                self.current_texture_index = 0
            if self.is_facing_right:
                self.texture = self.idle_right_textures[int(self.current_texture_index)]
            else:
                self.texture = self.idle_left_textures[int(self.current_texture_index)]
