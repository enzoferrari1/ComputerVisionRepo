from glob import glob
import pickle
import random
import matplotlib.pyplot as plt
import cv2
import os
import shutil

backgrounds_pck_fn="backgrounds.pck"

class Backgrounds():
    def __init__(self,backgrounds_pck_fn=backgrounds_pck_fn):
        self._images=pickle.load(open(backgrounds_pck_fn,'rb'))
        self._nb_images=len(self._images)
        print("Nb of images loaded :", self._nb_images)
    def get_random(self, display=False):
        bg=self._images[random.randint(0,self._nb_images-1)]
        if display: cv2.imshow('Background sample', bg)#plt.imshow(bg)
        return bg
    
# backgrounds = Backgrounds()

# sample = backgrounds.get_random(display=True)

class ImageAugmentor:
    def __init__(self, original_image_path: str, mask_image_path: str, annotation_path: str, annotation_type: str, n_augmentations: int, save_dir: str, backgrounds: Backgrounds):
        self.original_image_path = original_image_path
        self.mask_image_path = mask_image_path
        self.save_dir = save_dir
        self.annotation_path = annotation_path
        self.annotation_type = annotation_type
        self.n_augmentations = n_augmentations
        self.backgrounds = backgrounds

        # Load the original image
        self.original_image = cv2.imread(original_image_path)

        # Load the mask image in grayscale
        self.mask = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)

        # Convert the mask to a binary mask
        _, self.binary_mask = cv2.threshold(self.mask, 127, 255, cv2.THRESH_BINARY)

        # Create an inverse binary mask
        self.binary_mask_inv = cv2.bitwise_not(self.binary_mask)

        # Extract the foreground using the binary mask
        self.foreground = cv2.bitwise_and(self.original_image, self.original_image, mask=self.binary_mask)

    def augment_with_random_background(self, starting_suffix = 0):
        # Create photos and annotations directories if they don't exist
        photos_dir = os.path.join(self.save_dir, "photos")
        annotations_dir = os.path.join(self.save_dir, "annotations")
        os.makedirs(photos_dir, exist_ok=True)
        os.makedirs(annotations_dir, exist_ok=True)
        last_suffix = starting_suffix
        for i in range(self.n_augmentations):
            original_base_name = os.path.splitext(os.path.basename(self.original_image_path))[0]

            # Get a random background image
            background_image = self.backgrounds.get_random()

            # Resize the background image to match the original image size
            background_image = cv2.resize(background_image, (self.original_image.shape[1], self.original_image.shape[0]))

            # Extract the background region using the inverse binary mask
            background = cv2.bitwise_and(background_image, background_image, mask=self.binary_mask_inv)

            # Combine the foreground and the extracted background
            augmented_image = cv2.add(self.foreground, background)

            # Generate a unique suffix for the augmented image
            unique_suffix = f"_{str(starting_suffix + i)}"
            augmented_image_name = f"{original_base_name}{unique_suffix}.jpg"
            save_path = os.path.join(photos_dir, augmented_image_name)
            cv2.imwrite(save_path, augmented_image)

            # Copy the original annotation file to the annotations directory with the new name
            annotation_name = f"{original_base_name}{unique_suffix}.{self.annotation_type}"
            annotation_save_path = os.path.join(annotations_dir, annotation_name)
            shutil.copy(self.annotation_path, annotation_save_path)
            last_suffix = starting_suffix + i

        return last_suffix

# original_image_path = 'to_augment/photos/20240531_234309.jpg'
# mask_image_path = 'to_augment/masks/20240531_234309.png'
# annotation_path = 'cartas_obstruidas_sobre_mesa/annotations/20240531_234309.json'
# save_dir = 'augmented_0'

#augmentor = ImageAugmentor(original_image_path, mask_image_path, annotation_path, 10, save_dir, backgrounds)

#augmentor.augment_with_random_background()
