import arcade

class Ladder:
    def __init__(self, echelle_list):
        """
        Initialize the Echelle class.
        
        :param echelle_list: List of ladder sprites (arcade.SpriteList)
        """
        self.echelle_list = echelle_list  # Store the list of ladder sprites

    def check_climb(self, player_sprite):
        """
        Check if the player is colliding with any ladder in the echelle_list and allow climbing.
        
        :param player_sprite: The player sprite to check for collisions
        :return: True if the player is touching a ladder, otherwise False
        """
        # Check if the player is touching a ladder
        hit_list = arcade.check_for_collision_with_list(player_sprite, self.echelle_list)
        if len(hit_list) > 0:
            return True
        return False

    def draw(self):
        """ Draw the ladders. """
        self.echelle_list.draw()

    def get_lists(self):
        return self.echelle_list