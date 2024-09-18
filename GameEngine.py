import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "fenetre de jeu"

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("test", 300, 300, arcade.color.BLACK, 24)

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
