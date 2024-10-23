from glob import glob
import random
import os
from load_backgrounds import Backgrounds
import cv2
from card_on_card_background import augment_card_with_background

background_loader = Backgrounds()

photos_files = glob("artificial_dataset_for_classification/mazo_completo/low-res/train/cropped/portions/*.png")
output_photos = "artificial_dataset_for_classification/mazo_completo/low-res/train/cropped/rotations/"
cards_background_folder = "artificial_dataset_for_classification/mazo_completo/backgrounds_cards"
for original_image_path in photos_files:
    for i in range(6):
        filename = os.path.splitext(os.path.basename(original_image_path))[0]
        original_base_name = os.path.splitext(os.path.basename(original_image_path))[0]

        if False:#if random.choice([0,1]) == 1: # 50% de probabilidades de aumentar con un background de cartas, 50% de hacerlo con uno random
            files = [f for f in os.listdir(cards_background_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]    
            if not files:
                raise ValueError("No image files found in the folder")
            # Choose a random file
            random_file = random.choice(files)
            background_path = os.path.join(cards_background_folder, random_file)
            background = cv2.imread(background_path)
            background_mode = 'card'
        else:
            background = background_loader.get_random()
            background_mode = 'random'
        # Example usage
        angle = random.uniform(0,360) 
        crop_size = 900  # Example crop size from the background
        output_image_path = os.path.join(output_photos, original_base_name + f'_{background_mode}_{i+1}.png')

        augment_card_with_background(original_image_path, background, angle, crop_size, output_image_path, mode=background_mode)


