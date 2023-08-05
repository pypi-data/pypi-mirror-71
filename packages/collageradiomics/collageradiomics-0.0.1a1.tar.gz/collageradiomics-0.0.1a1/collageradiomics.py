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

def collage(img_path, mask_path):
    img_s = sitk.ReadImage(img_path)

    # Turn image into a Numpy array.
    img_array = sitk.GetArrayFromImage(img_s)
    patch_window_width = 50
    patch_window_height = 50
    mask_min_x = 252
    mask_min_y = 193
    mask_max_x = mask_min_x + patch_window_width
    mask_max_y = mask_min_y + patch_window_height
    collage(img_array, mask_min_x, mask_min_y, mask_max_x, mask_max_y);

def collage(img_array, mask_min_x, mask_min_y, mask_max_x, mask_max_y):
    img_array = img_array[:,:,0]
    print(f'IMAGE:\nwidth={img_array.shape[1]} height={img_array.shape[0]}')

    # Create random window.
    svd_radius = 5
    patch_window_width = 50
    patch_window_height = 50
    mask_min_x = 252
    mask_min_y = 193
    mask_max_x = mask_min_x + patch_window_width
    mask_max_y = mask_min_y + patch_window_height
    haralick_radius = svd_radius * 2 + 1

    cropped_array = highlight_rectangle_on_image(img_array, mask_min_x, mask_min_y, patch_window_width, patch_window_height)
    print(cropped_array.shape)

    # Extend outwards
    padded_mask_min_x = max(mask_min_x - svd_radius, 0)
    padded_mask_min_y = max(mask_min_y - svd_radius, 0)
    padded_mask_max_x = min(mask_max_x + svd_radius, img_array.shape[1]-1)
    padded_mask_max_y = min(mask_max_y + svd_radius, img_array.shape[0]-1)
    print(f'x = {padded_mask_min_x}:{padded_mask_max_x} ({padded_mask_max_x - padded_mask_min_x})')
    print(f'y = {padded_mask_min_y}:{padded_mask_max_y} ({padded_mask_max_y - padded_mask_min_y})')
    padded_cropped_array = img_array[padded_mask_min_y:padded_mask_max_y, padded_mask_min_x:padded_mask_max_x]
    print(padded_cropped_array.shape)

    # Calculate gradient
    rescaled_padded_cropped_array = padded_cropped_array/256
    dx=np.gradient(rescaled_padded_cropped_array, axis=1)
    dy=np.gradient(rescaled_padded_cropped_array, axis=0)

    # Display dx & dy.
    figure, axes = plt.subplots(1, 2, figsize=(15, 15))
    show_colored_image(figure, axes[0], dx)
    axes[0].set_title(f'Gx size={dx.shape}')
    show_colored_image(figure, axes[1], dy)
    axes[1].set_title(f'Gy size={dy.shape}')

    # loop through all regions and calculate dominant angles

    dominant_angles_array = np.zeros_like(cropped_array, np.single)
        
    print(f'dx shape = {dx.shape}')
    print(f'dominant angles shape = {dominant_angles_array.shape}')

    svd_diameter = svd_radius*2+1
    dx_windows = view_as_windows(dx, (svd_diameter, svd_diameter))
    dy_windows = view_as_windows(dy, (svd_diameter, svd_diameter))

    print(f'svd radius = {svd_radius}')
    print(f'svd diameter = {svd_diameter}')
    print(f'dx windows shape = {dx_windows.shape}')


    #center_x_range = range(svd_radius, dx.shape[1]-1-int(svd_window_size/2))
    #center_y_range = range(svd_radius, dx.shape[0]-1-int(svd_window_size/2))
    center_x_range = range(dx_windows.shape[1])
    center_y_range = range(dx_windows.shape[0])

    print(f'{center_x_range}, {center_y_range}')
    for current_svd_center_x in center_x_range:
        for current_svd_center_y in center_y_range:
            current_dominant_angle = svd_dominant_angle(
                current_svd_center_x, current_svd_center_y,
                dx_windows, dy_windows)
            dominant_angles_array[current_svd_center_y, current_svd_center_x] = current_dominant_angle
            if (random.randint(0,500)==0):
                print(f'x={current_svd_center_x}, y={current_svd_center_y}')
                print(f'angle={current_dominant_angle}')
    print('Done calculating dominant angles.')

    figure, axis = plt.subplots(1, 1, figsize=(5,5))
    show_colored_image(figure, axis, dominant_angles_array, plt.cm.jet)
    axis.set_title('Dominant Angles (SVD)')

    har_test = np.zeros(400)
    for x in range(1, 401):
        har_test[x-1] = x
    har_max = har_test.max()
    har_min = har_test.min()
    new_max = 63
    new_min = 0
    har_test = (har_test - har_min) / (har_max - har_min)
    har_test = har_test * (new_max - new_min) + new_min
    har_test = np.round(har_test)
    har_test = np.reshape(har_test, (20, 20))
    # haralick_image = np.zeros(har_test.shape, dtype=int)
    har_test = har_test.astype(int)
    print(har_test)
    figure, axis = plt.subplots(1,1, figsize=(5,5))
    show_colored_image(figure, axis, har_test)

    cropped_array_max = cropped_array.max()
    cropped_array_min = cropped_array.min()
    new_max = 63
    new_min = 0
    cropped_array_shaped = (cropped_array - cropped_array_min) / (cropped_array_max - cropped_array_min)
    cropped_array_shaped = cropped_array_shaped * (new_max - new_min) + new_min
    cropped_array_shaped = np.round(cropped_array_shaped)
    cropped_array_shaped = cropped_array_shaped.astype(int)
    figure, axis = plt.subplots(1,1, figsize=(5,5))
    show_colored_image(figure, axis, cropped_array_shaped)
    direction = 0

    plt.rc('figure', max_open_warning = 0)
    for feature in range(13):
        result = get_haralick_mt_feature(cropped_array_shaped, feature, direction, 20, symmetric=False, mean=True)
        figure, axis = plt.subplots(1,1, figsize=(5,5))
        show_colored_image(figure, axis, result)
        axis.set_title(f'Feature {feature+1} Mean')