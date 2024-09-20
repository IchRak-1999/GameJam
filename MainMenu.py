import arcade
import os
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FONT_NAME
from Background import Background

class MainMenu:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.start_game = False
        self.quit_game = False

        self.title_x = SCREEN_WIDTH // 2
        self.title_y = SCREEN_HEIGHT // 2 + 100

        self.new_game_button_x = SCREEN_WIDTH // 2
        self.new_game_button_y = SCREEN_HEIGHT // 2

        self.quit_button_x = SCREEN_WIDTH // 2
        self.quit_button_y = SCREEN_HEIGHT // 2 - 100

        self.button_width = 270
        self.button_height = 50

        self.slide_out = False
        self.slide_speed = 500

        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT, self.game_engine.bg_color, self.game_engine.bg_layer_3_path, self.game_engine.bg_layer_4_path)

    def on_draw(self):
        self.background.draw()

        arcade.draw_text(SCREEN_TITLE, self.title_x, self.title_y, arcade.color.WHITE, font_size=50, anchor_x="center", font_name=FONT_NAME)

        arcade.draw_rectangle_filled(self.new_game_button_x, self.new_game_button_y, self.button_width, self.button_height, arcade.color.DARK_BLUE)
        arcade.draw_text("Nouvelle Partie", self.new_game_button_x, self.new_game_button_y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center", font_name=FONT_NAME)

        arcade.draw_rectangle_filled(self.quit_button_x, self.quit_button_y, self.button_width, self.button_height, arcade.color.DARK_RED)
        arcade.draw_text("Quitter", self.quit_button_x, self.quit_button_y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center", font_name=FONT_NAME)

    def update(self, delta_time,player):
        self.background.update(delta_time,player)

        if self.slide_out:
            self.title_y += self.slide_speed * delta_time
            self.new_game_button_y += self.slide_speed * delta_time
            self.quit_button_y += self.slide_speed * delta_time

            if self.new_game_button_y > SCREEN_HEIGHT + 100:
                self.start_game = True

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.new_game_button_x - self.button_width / 2 < x < self.new_game_button_x + self.button_width / 2
                and self.new_game_button_y - self.button_height / 2 < y < self.new_game_button_y + self.button_height / 2):
            self.slide_out = True

        if (self.quit_button_x - self.button_width / 2 < x < self.quit_button_x + self.button_width / 2
                and self.quit_button_y - self.button_height / 2 < y < self.quit_button_y + self.button_height / 2):
            self.quit_game = True
            arcade.close_window()
