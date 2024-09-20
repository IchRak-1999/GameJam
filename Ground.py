import arcade

class Ground:
    def __init__(self, ground_sprite_list):
        """
        Initialise la classe Ground avec une liste de sprites représentant le sol.
        
        :param ground_sprite_list: La liste de sprites représentant le sol (ground).
        """
        self.ground_sprite_list = ground_sprite_list

    def check_collision(self, entity):
        """
        Vérifie les collisions entre l'entité donnée et les sprites du sol.
        
        :param entity: L'objet qui interagit avec le sol, par exemple un joueur.
        :return: True si une collision est détectée, False sinon.
        """
        # Vérifie si l'entité entre en collision avec un sprite du sol
        collision_list = arcade.check_for_collision_with_list(entity, self.ground_sprite_list)
        
        # Si collision_list n'est pas vide, il y a une collision
        if collision_list:
            return True,collision_list
        return False,collision_list

    def draw(self):
        """
        Dessine tous les sprites du sol.
        """
        self.ground_sprite_list.draw()

    def get_list(self):

        return self.ground_sprite_list
