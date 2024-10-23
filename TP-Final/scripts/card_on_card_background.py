from PIL import Image, ImageOps
import numpy as np
import random
import math
import cv2

def pil_to_cv2(image):
    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image#cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def cv2_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# Function to get a random crop from the background
def get_random_crop(image, crop_size):
    h, w = image.shape[:2]
    left = random.randint(0, w - crop_size)
    top = random.randint(0, h - crop_size)
    crop = image[top:top + crop_size, left:left + crop_size]
    return crop

def rotate_image_with_padding(image, angle):
    # Get image dimensions
    h, w = image.shape[:2]
    
    # Calculate the rotation matrix
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Calculate new bounding box dimensions
    cos_theta = np.abs(M[0, 0])
    sin_theta = np.abs(M[0, 1])
    new_w = int((h * sin_theta) + (w * cos_theta))
    new_h = int((h * cos_theta) + (w * sin_theta))
    
    # Adjust the rotation matrix to take into account translation due to rotation
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # Perform the rotation
    rotated = cv2.warpAffine(image, M, (new_w, new_h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    
    return rotated


def resize_and_overlay(rotated_card, background, crop_size, mode='card'):
    # Step 2: Extract a random crop from the background
    if mode == 'card':
        random_crop = get_random_crop(background, crop_size)
    else:
        random_crop = background
    # Step 3: Resize the crop to match the largest dimension of the rotated card
    card_h, card_w = rotated_card.shape[:2]
    max_dim = max(card_w, card_h)
    resized_crop = cv2.resize(random_crop, (max_dim, max_dim), interpolation=cv2.INTER_LANCZOS4)
    
    # Step 4: Overlay the rotated card onto the resized crop
    y_offset = (max_dim - card_h) // 2
    x_offset = (max_dim - card_w) // 2
    
    # Create a mask where the black background is not included
    mask = cv2.inRange(rotated_card, (1, 1, 1), (255, 255, 255))  # Mask for non-black pixels
    mask_inv = cv2.bitwise_not(mask)  # Inverse mask for the background
    
    # Ensure rotated_card is RGB
    if rotated_card.shape[2] == 4:
        rotated_card = rotated_card[:, :, :3]  # Drop the alpha channel
    
    # Apply the mask to the rotated card and the inverse mask to the resized crop
    card_region = cv2.bitwise_and(rotated_card, rotated_card, mask=mask)
    background_region = cv2.bitwise_and(resized_crop[y_offset:y_offset+card_h, x_offset:x_offset+card_w], 
                                        resized_crop[y_offset:y_offset+card_h, x_offset:x_offset+card_w], 
                                        mask=mask_inv)
    
    # Combine the card and background regions
    combined_region = cv2.add(card_region, background_region)
    resized_crop[y_offset:y_offset+card_h, x_offset:x_offset+card_w] = combined_region

    # Step 5: Crop out any excess parts to match the original card dimensions
    final_crop = resized_crop[y_offset:y_offset+card_h, x_offset:x_offset+card_w]
    return final_crop

# Combined function
def augment_card_with_background(card_image_path, background_image, angle, crop_size, output_image_path, mode):
    card_image = cv2.imread(card_image_path)    
    rotated_card = rotate_image_with_padding(card_image, angle)
    augmented_image = resize_and_overlay(rotated_card, background_image, crop_size, mode)
    
    cv2.imwrite(output_image_path, augmented_image)
# Example usage
card_image_path = 'artificial_dataset_for_classification/mazo_completo/cropped/b0215721c2686db8e991b224e4df6916.jpg'
background_image_path = 'artificial_dataset_for_classification/mazo_completo/backgrounds_cards/20240628_173004.png'
angle = 300  # Rotate by 45 degrees
crop_size = 900  # Example crop size from the background
output_image_path = 'path_to_augmented_image.png'

# augment_card_with_background(card_image_path, background_image_path, angle, crop_size, output_image_path, mode='card')