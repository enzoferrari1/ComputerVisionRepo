import os
import cv2

# Define the list of labels
labels = [
    "1O", "1C", "1E", "1B", "2O", "2C", "2E", "2B", "3O", "3C", "3E", "3B",
    "4O", "4C", "4E", "4B", "5O", "5C", "5E", "5B", "6O", "6C", "6E", "6B",
    "7O", "7C", "7E", "7B", "8O", "8C", "8E", "8B", "9O", "9C", "9E", "9B",
    "10O", "10C", "10E", "10B", "11O", "11C", "11E", "11B", "12O", "12C", "12E", "12B", "J"
]

# Directories
image_dir = 'prueba_recorte/images'
label_dir = 'prueba_recorte/labels'
output_dir = 'prueba_recorte/result'

from PIL import Image

def crop_and_save_bounding_boxes(image_dir, label_dir, output_dir):
    # Define the list of labels
    labels = [
        "1O", "1C", "1E", "1B", "2O", "2C", "2E", "2B", "3O", "3C", "3E", "3B",
        "4O", "4C", "4E", "4B", "5O", "5C", "5E", "5B", "6O", "6C", "6E", "6B",
        "7O", "7C", "7E", "7B", "8O", "8C", "8E", "8B", "9O", "9C", "9E", "9B",
        "10O", "10C", "10E", "10B", "11O", "11C", "11E", "11B", "12O", "12C", "12E", "12B", "J", "UNKNOWN"
    ]

    # Supported image formats
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all files in the image directory
    for image_filename in os.listdir(image_dir):
        # Check if the file is an image
        if any(image_filename.lower().endswith(ext) for ext in image_extensions):
            # Read the image
            image_path = os.path.join(image_dir, image_filename)
            image = Image.open(image_path)
            img_width, img_height = image.size

            # Corresponding label file
            label_filename = os.path.splitext(image_filename)[0] + '.txt'
            label_path = os.path.join(label_dir, label_filename)
            if not os.path.exists(label_path):
                continue
            # Read the label file
            with open(label_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    label_idx = int(parts[0])
                    label = labels[label_idx]
                    
                    # YOLO format: class x_center y_center width height
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])
                    
                    # Convert to pixel coordinates
                    x_center_pixel = int(x_center * img_width)
                    y_center_pixel = int(y_center * img_height)
                    width_pixel = int(width * img_width)
                    height_pixel = int(height * img_height)

                    # Calculate the top-left and bottom-right coordinates
                    x1 = x_center_pixel - width_pixel // 2
                    y1 = y_center_pixel - height_pixel // 2
                    x2 = x_center_pixel + width_pixel // 2
                    y2 = y_center_pixel + height_pixel // 2

                    # Ensure the coordinates are within image boundaries
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(img_width, x2)
                    y2 = min(img_height, y2)

                    # Crop the image
                    cropped_image = image.crop((x1, y1, x2, y2))

                    # Save the cropped image
                    cropped_image_filename = f"{label}_{os.path.splitext(image_filename)[0]}_{x1}_{y1}.png"
                    cropped_image_path = os.path.join(output_dir, cropped_image_filename)
                    cropped_image.save(cropped_image_path)

    print("Cropping and saving of images completed.")

# Example usage:
# crop_and_save_bounding_boxes('path/to/image_folder', 'path/to/label_folder', 'path/to/output_folder')
image_dir = 'ds-todas-las-cartas'
label_dir = 'ds-todas-las-cartas/bbox'
output_dir = 'ds-todas-las-cartas/cropped'

# image_dir = 'prueba_recorte/images'
# label_dir = 'prueba_recorte/labels'
# output_dir = 'prueba_recorte/results'
crop_and_save_bounding_boxes(image_dir, label_dir, output_dir)

from PIL import Image
import os

def augment_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            width, height = image.size

            # Cropping the 1/6 top portion
            # top_sixth = image.crop((0, 0, width, height // 8))
            # top_sixth.save(os.path.join(output_folder, filename.split('.')[0] + '_top_sixth.' + filename.split('.')[-1]))

            # # Cropping the 1/6 bottom portion
            # bottom_sixth = image.crop((0, 7 * height // 8, width, height))
            # bottom_sixth.save(os.path.join(output_folder, filename.split('.')[0] + '_bottom_sixth.' + filename.split('.')[-1]))
            # Cropping the top half
            top_half = image.crop((0, 0, width, height // 2))
            top_half.save(os.path.join(output_folder, filename.split('.')[0] + '_top_half.' + filename.split('.')[-1]))

            # Cropping the bottom half
            bottom_half = image.crop((0, height // 2, width, height))
            bottom_half.save(os.path.join(output_folder, filename.split('.')[0] + '_bottom_half.' + filename.split('.')[-1]))

            # Cropping the left half
            left_half = image.crop((0, 0, width // 2, height))
            left_half.save(os.path.join(output_folder, filename.split('.')[0] + '_left_half.' + filename.split('.')[-1]))

            # Cropping the right half
            right_half = image.crop((width // 2, 0, width, height))
            right_half.save(os.path.join(output_folder, filename.split('.')[0] + '_right_half.' + filename.split('.')[-1]))

            # Cropping the top left quarter
            top_left_quarter = image.crop((0, 0, width // 2, height // 2))
            top_left_quarter.save(os.path.join(output_folder, filename.split('.')[0] + '_top_left_quarter.' + filename.split('.')[-1]))

            # # Cropping the bottom right quarter
            # bottom_right_quarter = image.crop((width // 2, height // 2, width, height))
            # bottom_right_quarter.save(os.path.join(output_folder, filename.split('.')[0] + '_bottom_right_quarter.' + filename.split('.')[-1]))

input_folder = 'artificial_dataset_for_classification/mazo_completo/cropped'
output_folder = 'artificial_dataset_for_classification/mazo_completo/cropped/portions'
augment_images(input_folder, output_folder)


import os

def delete_files_with_string(directory, string):
    try:
        # Iterate over all files in the specified directory
        for filename in os.listdir(directory):
            # Check if the specified string is in the filename
            if string in filename:
                # Construct the full file path
                file_path = os.path.join(directory, filename)
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("Deletion complete.")
    except Exception as e:
        print(f"Error: {e}")

# Specify the directory and the string to look for
directory_path = '/path/to/your/folder'
search_string = 'your_string'

# Call the function to delete the files
delete_files_with_string(directory_path, search_string)

import os

def delete_files_not_containing_strings(directory, string_list):
    try:
        # Iterate over all files in the specified directory
        for filename in os.listdir(directory):
            # Check if the filename does not contain any of the strings in the list
            if not any(string in filename for string in string_list):
                # Construct the full file path
                file_path = os.path.join(directory, filename)
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("Deletion complete.")
    except Exception as e:
        print(f"Error: {e}")

# Specify the directory and the list of strings to look for
directory_path = 'artificial_dataset_for_classification/mazo_completo/train/cropped/rotations_on_cards'
search_strings = ['half', 'sixth', 'quarter']

# Call the function to delete the files
delete_files_not_containing_strings(directory_path, search_strings)

import os

def delete_files_ending_with_chars(directory, end_chars):
    try:
        # Iterate over all files in the specified directory
        for filename in os.listdir(directory):
            # Split the filename and its extension
            base_name, ext = os.path.splitext(filename)
            # Check if the base filename ends with any of the specified characters
            if any(base_name.endswith(char) for char in end_chars):
                # Construct the full file path
                file_path = os.path.join(directory, filename)
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("Deletion complete.")
    except Exception as e:
        print(f"Error: {e}")

# Specify the directory and the list of characters to check for
directory_path = 'artificial_dataset_for_classification/mazo_completo/train/cropped/rotations_on_cards'
ending_characters = ['2', '3', '4', '5', '6', '7', '8', '9']  # Example characters to check for

# Call the function to delete the files
delete_files_ending_with_chars(directory_path, ending_characters)


import os
import shutil
import random

def split_dataset(input_folder, train_folder, val_folder, val_split=0.1):
    # Create directories if they don't exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # Get all files from the input folder
    all_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    # Shuffle the files
    random.shuffle(all_files)

    # Calculate the split index
    split_index = int(len(all_files) * val_split)

    # Split the files into validation and training sets
    val_files = all_files[:split_index]
    train_files = all_files[split_index:]

    # Copy files to respective folders
    for f in val_files:
        shutil.copy(os.path.join(input_folder, f), os.path.join(val_folder, f))

    for f in train_files:
        shutil.copy(os.path.join(input_folder, f), os.path.join(train_folder, f))

    print(f"Total files: {len(all_files)}")
    print(f"Training files: {len(train_files)}")
    print(f"Validation files: {len(val_files)}")

# Define your folders
input_folder = 'ds-todas-las-cartas/cropped'
train_folder = 'ds-todas-las-cartas/cropped/train'
val_folder = 'ds-todas-las-cartas/cropped/val'

# Call the function to split the dataset
split_dataset(input_folder, train_folder, val_folder)

