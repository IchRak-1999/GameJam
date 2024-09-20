from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import arcade

class Platform2:
    def __init__(self, platform_list,platform_background_list, direction_x, direction_y):
        """
        Initialize the Platform class.

        :param platform_list: List of platform sprites
        :param direction_x: Movement direction in x-axis
        :param direction_y: Movement direction in y-axis
        """
        self.platform_list = platform_list  # Store the list of platform sprites
        self.platform_bg = platform_background_list #Store the list of platform background link to platform (optionnal)
        self.direction_x = direction_x      # Movement direction for x-axis
        self.direction_y = direction_y      # Movement direction for y-axis
        self.counter = 0
        self.reverse = False

    def draw(self):
        """
        Dessine tous les sprites du sol.
        """
        self.platform_list.draw()
        self.platform_bg.draw()

    def get_list(self):

        return self.platform_list

    def update(self, delta_time):
        """
        Update the position of the platforms based on direction and delta_time.
        
        :param delta_time: Time elapsed between frames
        """
        
        #Incrementation of counter for reverse direction of platform
        self.counter+=1

        # Check boundaries for x-axis and reverse direction if needed
        if self.counter>350:
            self.direction_x *= -1
            self.direction_y *= -1
            self.counter = 0

        for platform in self.platform_list:
            # Move platform
            platform.center_x += self.direction_x * 15 * delta_time
            platform.center_y += self.direction_y * 15 * delta_time

        for platform in self.platform_bg:
            # Move platform
            platform.center_x += self.direction_x * 15 * delta_time
            platform.center_y += self.direction_y * 15 * delta_time
