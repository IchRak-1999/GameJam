import arcade

class Background:
    def __init__(self, screen_width, screen_height, bg_color, layer_3_path, layer_4_path, scroll_speed_3=1, scroll_speed_4=2):
        arcade.set_background_color(bg_color)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll_speed_3 = scroll_speed_3
        self.scroll_speed_4 = scroll_speed_4

        self.bg_layer_3 = arcade.load_texture(layer_3_path)
        self.bg_layer_4 = arcade.load_texture(layer_4_path)
        
        self.bg_layer_3_x_1 = 0
        self.bg_layer_3_x_2 = screen_width
        self.bg_layer_4_x_1 = 0
        self.bg_layer_4_x_2 = screen_width
        self.bg_layer_5_x_1 = 0
        self.bg_layer_5_x_2 = screen_width
    
    def update(self, delta_time,player):
        """ Met à jour les positions des couches en fonction de leur vitesse de défilement """

        self.bg_layer_3_x_1 -= self.scroll_speed_3
        self.bg_layer_3_x_2 -= self.scroll_speed_3
        self.bg_layer_4_x_1 -= self.scroll_speed_4
        self.bg_layer_4_x_2 -= self.scroll_speed_4
        self.bg_layer_5_x_1 -= self.scroll_speed_4
        self.bg_layer_5_x_2 -= self.scroll_speed_4
        if self.bg_layer_3_x_1 <= -self.screen_width:
            self.bg_layer_3_x_1 = self.screen_width
        if self.bg_layer_3_x_2 <= -self.screen_width:
            self.bg_layer_3_x_2 = self.screen_width
        if self.bg_layer_4_x_1 <= -self.screen_width:
            self.bg_layer_4_x_1 = self.screen_width + player.center_x // 2
        if self.bg_layer_4_x_2 <= -self.screen_width:
            self.bg_layer_4_x_2 = self.screen_width + player.center_x // 2
        if self.bg_layer_5_x_1 <= -self.screen_width:
            self.bg_layer_5_x_1 = self.screen_width + player.center_x
        if self.bg_layer_5_x_2 <= -self.screen_width:
            self.bg_layer_5_x_2 = self.screen_width + player.center_x
    
    def draw(self):
        """ Dessine les deux couches du background """
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_3_x_1, 0, self.screen_width, self.screen_height, self.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_3_x_2, 0, self.screen_width, self.screen_height, self.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_4_x_1, 0, self.screen_width, self.screen_height, self.bg_layer_4)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_4_x_2, 0, self.screen_width, self.screen_height, self.bg_layer_4)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_5_x_1, 2, self.screen_width, self.screen_height, self.bg_layer_4)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_5_x_2, 2, self.screen_width, self.screen_height, self.bg_layer_4)
