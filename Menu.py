import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_SCROLL_SPEED_3, BACKGROUND_SCROLL_SPEED_4
class MainMenu:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.start_game = False
        self.quit_game = False

        # Position for menu items
        self.title_x = SCREEN_WIDTH // 2
        self.title_y = SCREEN_HEIGHT // 2 + 100

        self.new_game_button_x = SCREEN_WIDTH // 2
        self.new_game_button_y = SCREEN_HEIGHT // 2

        self.quit_button_x = SCREEN_WIDTH // 2
        self.quit_button_y = SCREEN_HEIGHT // 2 - 100

        # Button size
        self.button_width = 200
        self.button_height = 50

        # Animation control
        self.slide_out = False
        self.slide_speed = 500  # Speed of sliding animation (in pixels per second)

    def on_draw(self):
        # Draw background layers (parallax scrolling for layers 3 and 4)
        arcade.draw_lrwh_rectangle_textured(self.game_engine.bg_layer_3_x_1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_engine.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.game_engine.bg_layer_3_x_2, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_engine.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.game_engine.bg_layer_4_x_1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_engine.bg_layer_4)
        arcade.draw_lrwh_rectangle_textured(self.game_engine.bg_layer_4_x_2, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_engine.bg_layer_4)

        # Draw the title
        arcade.draw_text("Quantum Rewind", self.title_x, self.title_y, arcade.color.WHITE, font_size=50, anchor_x="center")

        # Draw buttons (New Game and Quit)
        arcade.draw_rectangle_filled(self.new_game_button_x, self.new_game_button_y, self.button_width, self.button_height, arcade.color.DARK_BLUE)
        arcade.draw_text("Nouvelle Partie", self.new_game_button_x, self.new_game_button_y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

        arcade.draw_rectangle_filled(self.quit_button_x, self.quit_button_y, self.button_width, self.button_height, arcade.color.DARK_RED)
        arcade.draw_text("Quitter", self.quit_button_x, self.quit_button_y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

    def update(self, delta_time):
        # Parallax background scrolling
        self.game_engine.bg_layer_3_x_1 -= BACKGROUND_SCROLL_SPEED_3
        self.game_engine.bg_layer_3_x_2 -= BACKGROUND_SCROLL_SPEED_3
        self.game_engine.bg_layer_4_x_1 -= BACKGROUND_SCROLL_SPEED_4
        self.game_engine.bg_layer_4_x_2 -= BACKGROUND_SCROLL_SPEED_4

        if self.game_engine.bg_layer_3_x_1 <= -SCREEN_WIDTH:
            self.game_engine.bg_layer_3_x_1 = SCREEN_WIDTH
        if self.game_engine.bg_layer_3_x_2 <= -SCREEN_WIDTH:
            self.game_engine.bg_layer_3_x_2 = SCREEN_WIDTH

        if self.game_engine.bg_layer_4_x_1 <= -SCREEN_WIDTH:
            self.game_engine.bg_layer_4_x_1 = SCREEN_WIDTH
        if self.game_engine.bg_layer_4_x_2 <= -SCREEN_WIDTH:
            self.game_engine.bg_layer_4_x_2 = SCREEN_WIDTH

        # Handle sliding out animation
        if self.slide_out:
            # Slide the menu items upwards
            self.title_y += self.slide_speed * delta_time
            self.new_game_button_y += self.slide_speed * delta_time
            self.quit_button_y += self.slide_speed * delta_time

            # If buttons are off screen, start the game
            if self.new_game_button_y > SCREEN_HEIGHT + 100:
                self.start_game = True

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if "Nouvelle Partie" button is clicked
        if (self.new_game_button_x - self.button_width / 2 < x < self.new_game_button_x + self.button_width / 2
                and self.new_game_button_y - self.button_height / 2 < y < self.new_game_button_y + self.button_height / 2):
            self.slide_out = True  # Trigger slide-out animation

        # Check if "Quitter" button is clicked
        if (self.quit_button_x - self.button_width / 2 < x < self.quit_button_x + self.button_width / 2
                and self.quit_button_y - self.button_height / 2 < y < self.quit_button_y + self.button_height / 2):
            self.quit_game = True  # Quit the game
            arcade.close_window()
