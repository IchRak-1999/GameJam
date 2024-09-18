from PIL import Image

# Charger l'image complète
image = Image.open("Assets/env_ground.png")

# Définir la zone à découper (x1, y1, x2, y2)
left = 130  # Par exemple, la coordonnée x de début
top = 90    # La coordonnée y de début
right = 200  # La coordonnée x de fin
bottom = 110  # La coordonnée y de fin

# Découper la zone définie
cropped_image = image.crop((left, top, right, bottom))

cropped_image.save("Assets/background_element.png")
