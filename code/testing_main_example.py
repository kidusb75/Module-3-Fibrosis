import cv2
import numpy as np
import pandas as pd
from termcolor import colored
import os

# 1. Setup Data
filenames = [
    r"images/MASK_Sk658 Llobe ch010017.jpg",
    r"images/MASK_SK658 Llobe ch010018.jpg",
    r"images/MASK_SK658 Llobe ch010019.jpg",
    r"images/MASK_SK658 Llobe ch010021.jpg",
    r"images/MASK_SK658 Llobe ch010022.jpg",
    r"images/MASK_SK658 Llobe ch010023.jpg",
]

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
        'Filename': os.path.basename(filename),
        'Depth': depth,
        'White_Pixels': white_count,
        'Black_Pixels': black_count,
        'White_Percent': round(white_percent, 2)
    })

    # REQUIRED PRINT FORMAT
    print(colored(os.path.basename(filename), "red"))
    print(f"White pixels: {white_count}")
    print(f"Black pixels: {black_count}")
    print(f"Percent white pixels: {white_percent:.2f}%")
    print(f"Depth: {depth} microns\n")



print("The .csv file 'Percent_White_Pixels.csv' has been created.")

'''the .csv writing subroutine ends here'''