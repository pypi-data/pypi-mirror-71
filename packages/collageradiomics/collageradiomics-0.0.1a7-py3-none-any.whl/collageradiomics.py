import matplotlib.pyplot as plt
import numpy as np
import random
import math
import SimpleITK as sitk
import mahotas as mt

from matplotlib.patches import Rectangle
from scipy import linalg
from skimage.util.shape import view_as_windows
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from itertools import product
from eolearn.features.haralick import HaralickTask
from eolearn.core import EOPatch
from skimage.feature.texture import greycomatrix

def svd_dominant_angle(x, y, dx_windows, dy_windows):
    dx_patch = dx_windows[y, x]
    dy_patch = dy_windows[y, x]
    
    window_area = dx_patch.size
    flattened_gradients = np.zeros((window_area, 2))
    flattened_gradients[:,0] = np.reshape(dx_patch, ((window_area)), order='F')
    flattened_gradients[:,1] = np.reshape(dy_patch, ((window_area)), order='F')
    
    U, S, V = linalg.svd(flattened_gradients)
    dominant_angle = math.atan2(V[0, 0], V[1, 0])
    
    return dominant_angle

def show_colored_image(figure, axis, image_data, colormap=plt.cm.jet):
    image = axis.imshow(image_data, cmap=colormap)
    divider = make_axes_locatable(axis)
    colorbar_axis = divider.append_axes("right", size="5%", pad=0.05)
    figure.colorbar(image, cax=colorbar_axis)

def create_highlighted_rectangle(x, y, w, h):
    return Rectangle((x, y), w, h, linewidth=3, edgecolor='cyan', facecolor='none')

def highlight_rectangle_on_image(image_data, min_x, min_y, w, h, colormap=plt.cm.gray):
    figure, axes = plt.subplots(1,2, figsize=(15,15))

    # Highlight window within image.
    show_colored_image(figure, axes[0], image_data, colormap)
    axes[0].add_patch(create_highlighted_rectangle(min_x, min_y, w, h))

    # Crop window.
    cropped_array = image_data[min_y:min_y+h, min_x:min_x+w]
    axes[1].set_title(f'Cropped Region ({w}x{h})')
    show_colored_image(figure, axes[1], cropped_array, colormap)
    
    plt.show()
    
    return cropped_array

def get_haralick_mt_value(img_array, center_x, center_y, window_size, haralick_feature, direction, symmetric, mean):
    min_x = int(max(0, center_x - window_size / 2))
    min_y = int(max(0, center_y - window_size / 2))
    max_x = int(min(img_array.shape[1] - 1, center_x + window_size / 2))
    max_y = int(min(img_array.shape[0] - 1, center_y + window_size / 2))
    cropped_img_array = img_array[min_y:max_y, min_x:max_x]
    cmat = np.empty((64, 64), np.int32)
    def all_cmatrices():
        for dir in range(4):
            mt.features.texture.cooccurence(cropped_img_array, dir, cmat, symmetric=symmetric)
            yield cmat
    har_feature = mt.features.texture.haralick_features(all_cmatrices(), return_mean=mean)
    if mean:
        return har_feature[haralick_feature]
    return har_feature[direction, haralick_feature]

def get_haralick_mt_feature(img, desired_haralick_feature, direction, haralick_window_size, symmetric=False, mean=False):
    haralick_image = np.zeros(img.shape)
    h, w = img.shape
    for pos in product(range(w), range(h)):
       result = get_haralick_mt_value(img, pos[0], pos[1], haralick_window_size, desired_haralick_feature, direction, symmetric, mean)
       haralick_image[pos[1], pos[0]] = result
    return haralick_image

class Collage:
    def __init__(self, img_array, mask_min_x, mask_min_y, mask_max_x, mask_max_y, patch_window_width, patch_window_height, svd_radius, verbose_logging=False):
        self.img_array = img_array
        self.mask_min_x = mask_min_x
        self.mask_min_y = mask_min_y
        self.mask_max_x = mask_max_x
        self.mask_max_y = mask_max_y
        self.patch_window_width = patch_window_width
        self.patch_window_height = patch_window_height
        self.svd_radius = svd_radius
        self.verbose_logging = verbose_logging

    def execute(self):
        mask_min_x = self.mask_min_x
        mask_min_y = self.mask_min_y
        mask_max_x = self.mask_max_x
        mask_max_y = self.mask_max_y
        patch_window_width = self.patch_window_width
        patch_window_height = self.patch_window_height
        svd_radius = self.svd_radius
        img_array = self.img_array[:,:,0]
        if self.verbose_logging:
            print(f'IMAGE:\nwidth={img_array.shape[1]} height={img_array.shape[0]}')

        haralick_radius = svd_radius * 2 + 1

        cropped_array = highlight_rectangle_on_image(img_array, mask_min_x, mask_min_y, patch_window_width, patch_window_height)
        if self.verbose_logging:
            print(cropped_array.shape)

        # Extend outwards
        padded_mask_min_x = max(mask_min_x - svd_radius, 0)
        padded_mask_min_y = max(mask_min_y - svd_radius, 0)
        padded_mask_max_x = min(mask_max_x + svd_radius, img_array.shape[1]-1)
        padded_mask_max_y = min(mask_max_y + svd_radius, img_array.shape[0]-1)
        if self.verbose_logging:
            print(f'x = {padded_mask_min_x}:{padded_mask_max_x} ({padded_mask_max_x - padded_mask_min_x})')
            print(f'y = {padded_mask_min_y}:{padded_mask_max_y} ({padded_mask_max_y - padded_mask_min_y})')
        padded_cropped_array = img_array[padded_mask_min_y:padded_mask_max_y, padded_mask_min_x:padded_mask_max_x]
        if self.verbose_logging:
            print(padded_cropped_array.shape)
        
        # Calculate gradient
        rescaled_padded_cropped_array = padded_cropped_array / 256
        dx=np.gradient(rescaled_padded_cropped_array, axis=1)
        dy=np.gradient(rescaled_padded_cropped_array, axis=0)
        self.dx = dx
        self.dy = dy

        # loop through all regions and calculate dominant angles

        dominant_angles_array = np.zeros((patch_window_height,patch_window_width), np.single)

        if self.verbose_logging:
            print(f'dx shape = {dx.shape}')
            print(f'dominant angles shape = {dominant_angles_array.shape}')

        svd_diameter = svd_radius*2+1
        dx_windows = view_as_windows(dx, (svd_diameter, svd_diameter))
        dy_windows = view_as_windows(dy, (svd_diameter, svd_diameter))

        if self.verbose_logging:
            print(f'svd radius = {svd_radius}')
            print(f'svd diameter = {svd_diameter}')
            print(f'dx windows shape = {dx_windows.shape}')

        center_x_range = range(dx_windows.shape[1])
        center_y_range = range(dx_windows.shape[0])

        if self.verbose_logging:
            print(f'{center_x_range}, {center_y_range}')
        for current_svd_center_x in center_x_range:
            for current_svd_center_y in center_y_range:
                current_dominant_angle = svd_dominant_angle(
                    current_svd_center_x, current_svd_center_y,
                    dx_windows, dy_windows)
                dominant_angles_array[current_svd_center_y, current_svd_center_x] = current_dominant_angle
                if (random.randint(0,500)==0):
                    if self.verbose_logging:
                        print(f'x={current_svd_center_x}, y={current_svd_center_y}')
                        print(f'angle={current_dominant_angle}')

        if self.verbose_logging:
            print('Done calculating dominant angles.')

        self.dominant_angles_array = dominant_angles_array

        # Rescale the range of the pixels to have discrete grey level values
        greylevels = 64

        new_max = greylevels-1
        new_min = 0

        dominant_angles_max = dominant_angles_array.max()
        dominant_angles_min = dominant_angles_array.min()

        dominant_angles_shaped = (dominant_angles_array - dominant_angles_min) / (dominant_angles_max - dominant_angles_min)
        dominant_angles_shaped = dominant_angles_shaped * (new_max - new_min) + new_min
        dominant_angles_shaped = np.round(dominant_angles_shaped)
        dominant_angles_shaped = dominant_angles_shaped.astype(int)
        self.dominant_angles_shaped =  dominant_angles_shaped

        # Calculate haralick
        haralick_window_size = svd_radius * 2 + 1

        haralick_features = np.empty((patch_window_height, patch_window_width, 13))

        for feature in range(13):
            print(f'Calculating feature {feature+1}:')
            haralick_features[:,:,feature] = get_haralick_mt_feature(dominant_angles_shaped, feature, greylevels, haralick_window_size, symmetric=False, mean=True)
            print('Calculated.')

        self.haralick_features = haralick_features

        return haralick_features
