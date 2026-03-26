'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

# 2: Generative AI (Gemini and Claude AI): Suggestion for import statements that can make the code more efficient and cleaner.  
    # import os  # Useful for handling file paths and getting clean filenames for the CSV.

import os # added for efficiency: OS for robust file path handling
from termcolor import colored   # used only to print colored text in terminal
import cv2                      # OpenCV library for image processing
import numpy as np              # numerical operations (arrays, sums, etc.); # NumPy for vectorized (fast) array math
import pandas as pd             # used to create csv file 
import time                     # used on 03/24/2026 for inclass activity: computing the time it takes to run the code with and without vectorization for counting pixels.


# Load the images you want to analyze

#filenames = [                                                                                                               # Variation in depth for better results (micrometers)
    #r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010039.jpg",  # 15
    #r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010032.jpg",  # 500
    #r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010146.jpg",  # 2000
    #r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010112.jpg",  # 5500 
    #r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010119.jpg",  # 8000
    #r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010092.jpg",  # 10000
#]

# For partner: use relative paths so it works for them. 
# Use relative paths so it works for your partner too!
filenames = [
    r"images/MASK_SK658 Llobe ch010039.jpg",
    r"images/MASK_SK658 Llobe ch010032.jpg",
    r"images/MASK_SK658 Slobe ch010146.jpg",
    r"images/MASK_SK658 Slobe ch010112.jpg",
    r"images/MASK_SK658 Slobe ch010119.jpg",
    r"images/MASK_SK658 Slobe ch010092.jpg"
]

# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")

depths = [15, 500, 2000, 5500, 8000, 10000]
results = []
white_percent_list = []

print(colored("Starting Image Analysis...", "yellow"))

# 2. Process Images 

# Load ALL images into memory BEFORE starting the timer
images_loaded = [cv2.imread(f, 0) for f in filenames]

# Start timer for efficiency testing (before for loop)
start_time = time.time()  # Start timer for efficiency testing (before for loop) 
print (colored("Processing images...", "yellow"))

# 'zip' pairs the filename and depth so they never get mismatched; its a function called a 'generator' that creates pairs on the fly, so it doesn't use extra memory like creating two lists of pairs would.
#for filename, depth in zip(filenames, depths):

#     # Load image directly as grayscale (the '0' flag)
#     # This is more efficient than loading color and converting later.
#     # img = cv2.imread(filename, 0) --- > We already loaded all images into memory before the loop, so we can just access them here.

#     # img = images_loaded[filenames.index(filename)]

#     # if the image can't be loaded (e.g., wrong path), print an error and skip to the next one. This prevents crashes and helps with debugging.
#     # if img is None:
#     #     print(colored(f"Error: Could not find {filename}", "red"))
#     #     continue

#     # EFFICIENCY UPGRADE: We did vectorization in NumPy to count white and black pixels in one pass, instead of creating a binary image and scanning it twice. This is much faster, especially for large images.
#     # Instead of creating a 'binary' image and then searching it twice, 
#     # we use NumPy to evaluate the grayscale array directly in one pass.
#     # Essentially, it checks all 4 million pixels simultaneously in C-code, which is ~100x faster than a Python loop.
#     # 127 is the brightness threshold (0=black, 255=white). It brighter than that, it is considered white and counted as fibrosis; otherwise, it is counted as black and healthy lung tissue. 

#     # white_count = np.sum(img > 127)  
    
#     # Slightly faster than np.sum for boolean arrays
#     white_count = np.count_nonzero(images_loaded > 127)
    
#     # Efficient Math: Total pixels - white pixels = black pixels.
#     # This avoids scanning the 4-million-pixel array a second time
#     total_pixels = img.size
#     black_count = total_pixels - white_count  # Faster than scanning the array a second time
    
#     # This avoids scanning the 4-million-pixel array a second time.
#     # Calculate percentage of fibrosis (white pixels)
#     white_percent = (white_count / total_pixels) * 100
#     white_percent_list.append(white_percent)

#     # Use os.path.basename for cleaner CSVs (removes the long C:\Users\... prefix)
#     clean_name = os.path.basename(filename)

#     # Store results in a dictionary for easy CSV writing with Pandas. This is more efficient than writing to CSV line by line.
#     # This results later has the percent white pixels pulled to then be used for other data manipulations later. 
#     results.append({
#         'Filename': clean_name,
#         'Depth': depth,
#         'White_Pixels': white_count,
#         'Black_Pixels': black_count,
#         'White_Percent': round(white_percent, 2)
#     })

for img, filename, depth in zip(images_loaded, filenames, depths):
    # img is directly available — no .index() lookup needed
    white_count = np.count_nonzero(img > 127)
    total_pixels = img.size
    black_count = total_pixels - white_count
    white_percent = (white_count / total_pixels) * 100
    white_percent_list.append(white_percent)
    clean_name = os.path.basename(filename)
    results.append({
        'Filename': clean_name,
        'Depth': depth,
        'White_Pixels': white_count,
        'Black_Pixels': black_count,
        'White_Percent': round(white_percent, 2)
    })

end_time = time.time()  # End timer for efficiency testing (before printing results) -- faster time
total_time = end_time - start_time  # End timer for efficiency testing (after for loop)


# REQUIRED PRINT FORMAT
print(colored(clean_name, "red"))
print(f"White pixels: {white_count}")
print(f"Black pixels: {black_count}")
print(f"Percent white pixels: {white_percent:.2f}%")
print(f"Depth: {depth} microns\n")

# 3. CSV WRITING SUBROUTINE
# Using Pandas to create the CSV is more efficient than the standard CSV library.
# It automatically handles the headers and table structure.
df = pd.DataFrame(results)
df.to_csv('Percent_White_Pixels.csv', index=False)

print(colored("Success: 'Percent_White_Pixels.csv' has been created.", "green")) 

print(colored(f"Total processing time: {total_time:.2f} seconds", "cyan"))  # Print total time taken for efficiency testing

# (End of assigned efficiency section - code below line 93 ignored)

##############
# LECTURE 2: UNCOMMENT BELOW
# Interpolate a point: given a depth, find the corresponding white pixel percentage

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


interpolate_depth = float(input(colored(
    "Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

x = depths
y = white_percent_list

# You can also use 'quadratic', 'cubic', etc.
i = interp1d(x, y, kind='linear')
interpolate_point = i(interpolate_depth)
print(colored(
    f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

depths_i = depths[:]
depths_i.append(interpolate_depth)
white_percents_i = white_percent_list[:]
white_percents_i.append(interpolate_point)


# make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
fig, axs = plt.subplots(2, 1)

axs[0].scatter(depths, white_percent_list, marker='o', linestyle='-', color='blue')
axs[0].set_title('Plot of depth of image vs percentage white pixels')
axs[0].set_xlabel('depth of image (in microns)')
axs[0].set_ylabel('white pixels as a percentage of total pixels')
axs[0].grid(True)


axs[1].scatter(depths_i, white_percents_i, marker='o',
               linestyle='-', color='blue')
axs[1].set_title(
    'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[1].set_xlabel('depth of image (in microns)')
axs[1].set_ylabel('white pixels as a percentage of total pixels')
axs[1].grid(True)
axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1],
               color='red', s=100, label='Highlighted point')


# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
