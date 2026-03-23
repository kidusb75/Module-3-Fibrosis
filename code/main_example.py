'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

from termcolor import colored
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

# Load the images you want to analyze

filenames = [
    r"images/MASK_Sk658 Llobe ch010017.jpg",
    r"images/MASK_SK658 Llobe ch010018.jpg",
    r"images/MASK_SK658 Llobe ch010019.jpg",
    r"images/MASK_SK658 Llobe ch010021.jpg",
    r"images/MASK_SK658 Llobe ch010022.jpg",
    r"images/MASK_SK658 Llobe ch010023.jpg",
]

# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")

depths = [45, 90, 60, 30, 80, 100]
results = []
white_percent_list = []

print(colored("Starting Image Analysis...", "yellow"))

# 2. Process Images
for i in range(len(filenames)):
    filename = filenames[i]
    depth = depths[i]
    
    # Load image in grayscale
    img = cv2.imread(filename, 0)
    if img is None:
        print(colored(f"Error: Could not find image at {filename}", "red"))
        continue

    # Convert to binary
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Count pixels
    white_count = np.sum(binary == 255)
    black_count = np.sum(binary == 0)
    total_pixels = binary.size

    # Percentage
    white_percent = (white_count / total_pixels) * 100
    white_percent_list.append(white_percent)

    # Store results
    results.append({
        'Filename': filename.split("/")[-1],
        'Depth': depth,
        'White_Pixels': white_count,
        'Black_Pixels': black_count,
        'White_Percent': round(white_percent, 2)
    })

    # REQUIRED PRINT FORMAT
    print(colored(filename.split("/")[-1], "red"))
    print(f"White pixels: {white_count}")
    print(f"Black pixels: {black_count}")
    print(f"Percent white pixels: {white_percent:.2f}%")
    print(f"Depth: {depth} microns\n")



print("The .csv file 'Percent_White_Pixels.csv' has been created.")

'''the .csv writing subroutine ends here'''

##############
# LECTURE 2: UNCOMMENT BELOW

# # Interpolate a point: given a depth, find the corresponding white pixel percentage

# interpolate_depth = float(input(colored(
#     "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

# x = depths
# y = white_percents

# # You can also use 'quadratic', 'cubic', etc.
# i = interp1d(x, y, kind='linear')
# interpolate_point = i(interpolate_depth)
# print(colored(
#     f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

# depths_i = depths[:]
# depths_i.append(interpolate_depth)
# white_percents_i = white_percents[:]
# white_percents_i.append(interpolate_point)


# # make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
# fig, axs = plt.subplots(2, 1)

# axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
# axs[0].set_title('Plot of depth of image vs percentage white pixels')
# axs[0].set_xlabel('depth of image (in microns)')
# axs[0].set_ylabel('white pixels as a percentage of total pixels')
# axs[0].grid(True)


# axs[1].scatter(depths_i, white_percents_i, marker='o',
#                linestyle='-', color='blue')
# axs[1].set_title(
#     'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
# axs[1].set_xlabel('depth of image (in microns)')
# axs[1].set_ylabel('white pixels as a percentage of total pixels')
# axs[1].grid(True)
# axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
#                color='red', s=100, label='Highlighted point')


# # Adjust layout to prevent overlap
# plt.tight_layout()
# plt.show()
