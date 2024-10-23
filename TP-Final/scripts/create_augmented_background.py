from load_backgrounds import Backgrounds, ImageAugmentor
from glob import glob
import json
import os
import subprocess
import shutil

backgrounds = Backgrounds()


output_dir = "augmented_1"
output_photos = "augmented_1/photos"
output_labels = "augmented_1/annotations"
mask_dir = "to_augment_1/masks"
annotation_dir = "to_augment_1/annotations"
#creating the ground_truth folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_photos, exist_ok=True)
os.makedirs(output_labels, exist_ok=True)

annotation_files = glob("to_augment_1/annotations/*.json")
# Transformar json a txt YOLO antes de aumentar
for original_json_path in annotation_files:
    filename = os.path.splitext(os.path.basename(original_json_path))[0]
    command = f"""
labelme2yolo --json_dir {annotation_dir} --val_size 0 --test_size 0 --json_name {filename}.json --label_list 1O 1C 1E 1B 2O 2C 2E 2B 3O 3C 3E 3B 4O 4C 4E 4B 5O 5C 5E 5B 6O 6C 6E 6B 7O 7C 7E 7B 8O 8C 8E 8B 9O 9C 9E 9B 10O 10C 10E 10B 11O 11C 11E 11B 12O 12C 12E 12B J
"""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    temp_annotation_file = filename+'.txt'
    temp_photo_file = filename+'.png'
    shutil.move(temp_annotation_file, output_labels)
    shutil.move(temp_photo_file, output_photos)
    

annotation_dir = "augmented_1/annotations"
photos_files = glob("to_augment_1/photos/*.jpg")
#loading the json file
for original_image_path in photos_files:
    filename = os.path.splitext(os.path.basename(original_image_path))[0]
    mask_image_path = os.path.join(mask_dir, filename+'.png')
    annotation_path = os.path.join(annotation_dir, filename+'.txt')
    augmentor = ImageAugmentor(original_image_path, mask_image_path, annotation_path, 'txt', 10, output_dir, backgrounds)
    augmentor.augment_with_random_background()


# Use masks in specific

import json
import base64
from PIL import Image
from io import BytesIO


def parse_labelme_masks(json_file_path, original_image_path, output_image_path):
    """
    Parse all masks from a Labelme JSON file and save them in one image of the original size.

    Parameters:
    - json_file_path: str, path to the Labelme JSON file
    - original_image_path: str, path to the original image to get its size
    - output_image_path: str, path to save the combined mask image

    Returns:
    - None
    """
    # Load the original image to get its size
    with Image.open(original_image_path) as original_image:
        original_size = original_image.size  # (width, height)

    # Step 1: Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Step 2: Initialize an empty image with the same size as the original image
    combined_mask = Image.new('L', (original_size[1], original_size[0]), 0)  # 'L' mode for grayscale, 0 for black

    # Step 3: Extract and decode each mask, then paste it on the combined image
    for shape in data['shapes']:
        if shape['shape_type'] == 'mask':
            mask_str = shape['mask']
            mask_bytes = base64.b64decode(mask_str)
            mask_image = Image.open(BytesIO(mask_bytes))

            # Extract the bounding box to place the mask image correctly
            x_min = int(shape['points'][0][0])
            y_min = int(shape['points'][0][1])
            x_max = int(shape['points'][1][0])
            y_max = int(shape['points'][1][1])
            
            # Create a mask image of the same size as the combined mask
            temp_mask = Image.new('L', (original_size[1], original_size[0]), 0)
            temp_mask.paste(mask_image, (x_min, y_min))

            # Combine the temp mask with the combined mask
            combined_mask = Image.composite(temp_mask, combined_mask, temp_mask)

    # Save the combined mask image
    combined_mask.save(output_image_path)
    print(f"Combined mask image saved to {output_image_path}")

# Usage example
original_image_path = 'balance_ocluded/photos/20240620_002438.jpg'
json_file_path = 'balance_ocluded/masks/20240620_002438.json'
output_image_path = 'balance_ocluded/masks_images/parsed_mask.png'
parse_labelme_masks(json_file_path, original_image_path, output_image_path)






