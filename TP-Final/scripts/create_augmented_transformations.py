# Ver https://augly.readthedocs.io/en/latest/README_image.html#augmentations
import augly.image as imaugs
from PIL import Image, ImageFilter
import numpy as np
import os
from glob import glob
import random
import shutil
from custom_labelme2yolo import Labelme2YOLO
import subprocess

# Single case

COLOR_JITTER_PARAMS = {
    "brightness_factor": 0.6,
    "contrast_factor": 1.4,
    "saturation_factor": 0.6,
}

AUGMENTATIONS = [
    # imaugs.Blur(radius=4),
    imaugs.ColorJitter(**COLOR_JITTER_PARAMS),
    imaugs.RandomNoise(var=0.05),
    # imaugs.OneOf(
    #     [imaugs.OverlayOntoScreenshot(), imaugs.OverlayEmoji(), imaugs.OverlayText()]
    imaugs.RandomEmojiOverlay(opacity=0.6, emoji_size=0.4, x_pos=0.0, y_pos=0.0, seed=None)
]

TRANSFORMS = imaugs.Compose(AUGMENTATIONS)
# TENSOR_TRANSFORMS = transforms.Compose(AUGMENTATIONS + [transforms.ToTensor()])

# aug_image is a PIL image with your augs applied!
# aug_tensor_image is a Tensor with your augs applied!
image = Image.open("balance_oclussion_numbers/photos/20240621_112041.jpg")
aug_image = TRANSFORMS(image)
aug_image.show()
image.show()


output_dir = "augmented_2"
output_photos = "augmented_2/photos"
output_labels = "augmented_2/annotations"
annotations_dir = "solo_carta_en_mano/annotations"
photos_dir = "solo_carta_en_mano/photos"
#creating the ground_truth folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_photos, exist_ok=True)
os.makedirs(output_labels, exist_ok=True)

# Crear los labels YOLO
annotation_files = glob("solo_carta_en_mano/annotations/*.json")
# Transformar json a txt YOLO antes de aumentar
for original_json_path in annotation_files:
    filename = os.path.splitext(os.path.basename(original_json_path))[0]
    command = f"""
labelme2yolo --json_dir {annotations_dir} --val_size 0 --test_size 0 --json_name {filename}.json --label_list 1O 1C 1E 1B 2O 2C 2E 2B 3O 3C 3E 3B 4O 4C 4E 4B 5O 5C 5E 5B 6O 6C 6E 6B 7O 7C 7E 7B 8O 8C 8E 8B 9O 9C 9E 9B 10O 10C 10E 10B 11O 11C 11E 11B 12O 12C 12E 12B J
"""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    temp_annotation_file = filename+'.txt'
    temp_photo_file = filename+'.png'
    shutil.move(temp_annotation_file, output_labels)
    shutil.move(temp_photo_file, output_photos)

# Multiple images case
# generate_jitter_value usa la distribución beta para generar distribuciones deseadas. Chequear validate_beta_distribution.py para visualizarlas

def generate_jitter_value(low=0.7, high=1.3, alpha=0.8, beta=0.8):
    np.random.seed()
    value = np.random.beta(alpha, beta)
    transformed_value = float('%.2f'%(low + (high - low) * value))
    return transformed_value

# output_dir = "augmented_2"
output_photos = "ds-todas-las-cartas/train/aug-images"
output_labels = "ds-todas-las-cartas/train/aug-labels"

annotations_dir = "ds-todas-las-cartas/train/labels"
photos_files = glob("ds-todas-las-cartas/train/images/*.png")
#loading the json file
for original_image_path in photos_files:
    filename = os.path.splitext(os.path.basename(original_image_path))[0]
    original_base_name = os.path.splitext(os.path.basename(original_image_path))[0]
    annotation_path = os.path.join(annotations_dir, filename+'.txt')


    for i in range(5):
        COLOR_JITTER_PARAMS = {
            "brightness_factor": generate_jitter_value(),
            "contrast_factor": generate_jitter_value(),
            "saturation_factor": generate_jitter_value(),
        }
        emoji_size = random.uniform(0.4,0.7) #generate_jitter_value(low=0.4, high=0.7, alpha=5, beta=5)
        # blur_radio = generate_jitter_value(low=1, high=1.3, alpha=1.2, beta=0.9)
        if random.choice([1,2,3,4,5,6]) == 0:
            AUGMENTATIONS = [imaugs.ApplyPILFilter(filter_type=ImageFilter.CONTOUR),
                             imaugs.RandomNoise(var=0.01)]
        else:
            AUGMENTATIONS = [
                imaugs.ColorJitter(**COLOR_JITTER_PARAMS),
                imaugs.OneOf([
                    # imaugs.ApplyPILFilter(filter_type=ImageFilter.CONTOUR ),
                    # imaugs.ApplyPILFilter(filter_type=ImageFilter.EDGE_ENHANCE),
                    # imaugs.ApplyPILFilter(filter_type=ImageFilter.EDGE_ENHANCE_MORE),
                    imaugs.ApplyPILFilter(filter_type=ImageFilter.DETAIL),
                    imaugs.ApplyPILFilter(filter_type=ImageFilter.SMOOTH),
                    imaugs.ApplyPILFilter(filter_type=ImageFilter.SHARPEN)
                ]),
                # imaugs.Rotate(degrees=random.uniform(-10,10)),
                imaugs.RandomEmojiOverlay(opacity=0.15, emoji_size=emoji_size, 
                                        x_pos=generate_jitter_value(low=emoji_size+0.01,high=1-0.01,alpha=1.5,beta=1.5)-emoji_size,
                                        y_pos=generate_jitter_value(low=emoji_size+0.01,high=1-0.01,alpha=1.5,beta=1.5)-emoji_size, seed=None),
                # imaugs.Blur(p=0.5, radius=1.05),
                imaugs.RandomNoise(p=0.5, var=0.005)
            ]
        # if random.choice([0,1]) == 1:
        #     AUGMENTATIONS = AUGMENTATIONS + [imaugs.HFlip(), imaugs.VFlip()]
        TRANSFORMS = imaugs.Compose(AUGMENTATIONS)
        image = Image.open(original_image_path)
        aug_image = TRANSFORMS(image)

        # Copy the original annotation file to the annotations directory with the new name
        annotation_name = f"{original_base_name}_emoji0_{str(i)}.txt"
        image_name = f"{original_base_name}_{str(i)}.png"
        aug_image.save(os.path.join(output_photos, image_name))
        annotation_save_path = os.path.join(output_labels, annotation_name)
        shutil.copy(annotation_path, annotation_save_path)

