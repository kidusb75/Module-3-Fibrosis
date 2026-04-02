'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

# 2: Generative AI (Gemini and Claude AI): Suggestion for import statements that can make the code more efficient and cleaner.  
    # import os  # Useful for handling file paths and getting clean filenames for the CSV.
    # Furthermore, elements of the code such as understanding certian functions and diagnosing errors were instances where AI was utilized to help the team understand the code better, especially in cases where the generative model put out a more efficient way to do something (like using np.count_nonzero instead of nested for loops to count pixels, which is much faster); 
    # Lastly, occasionally needed AI to understand why and help comment some specific code lines for better clarity and understanding, but all final implementation and understanding was done by the team. 

import os # added for efficiency: OS for robust file path handling
from termcolor import colored   # used only to print colored text in terminal
import cv2                      # OpenCV library for image processing
import numpy as np              # numerical operations (arrays, sums, etc.); # NumPy for vectorized (fast) array math
import pandas as pd             # used to create csv file 
import time                     # used on 03/24/2026 for inclass activity: computing the time it takes to run the code with and without vectorization for counting pixels.


# Load the images you want to analyze -- specific file paths depend from computer or access method: 
# the primary images that we ended up analyzing are sourced from the images foleder in the Module-3-Fibrosis folder, but you can also use the full file paths to load the images if you want.
    # The 78 image are provided by the instructor. 
filenames = [                                                                                                               # Variation in depth for better results (micrometers)
    r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010039.jpg",  # 15
    r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010032.jpg",  # 500
    r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_Sk658 Llobe ch010146.jpg",  # 2000
    r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010112.jpg",  # 5500 
    r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010119.jpg",  # 8000
    r"C:\Users\kidus\OneDrive\Desktop\Computational BME\Module 03\Module-3-Fibrosis\images\MASK_SK658 Slobe ch010092.jpg",  # 10000
]

# # For partner: use relative paths so it works for them. 
# # Use relative paths so it works for your partner too!
# filenames = [
#     r"images/MASK_SK658 Llobe ch010039.jpg",
#     r"images/MASK_SK658 Llobe ch010032.jpg",
#     r"images/MASK_SK658 Slobe ch010146.jpg",
#     r"images/MASK_SK658 Slobe ch010112.jpg",
#     r"images/MASK_SK658 Slobe ch010119.jpg",
#     r"images/MASK_SK658 Slobe ch010092.jpg"
# ]

# Enter the depth of each image (in the same order that the images are listed above; you can find these in the .csv file provided to you which is tilted: "Filenames and Depths for Students")
# The depth values are in microns, and they represent the depth at which each image was taken. This information is crucial for analyzing the relationship between depth and the percentage of white pixels in the images, which can be important for understanding tissue characteristics in a biomedical context.
# More specifically, these are the depth values chronologically listed immages above, from shallowest to deepest within the mice lungs; and the team did this collection method instead of choosing images at complete random becasue we wanted to have a range of depths represented in our data, which can help us see trends and patterns in the percentage of white pixels as depth increases. 
# By including images from various depths, we can better understand how the tissue characteristics change with depth, which is important for our analysis of fibrosis in the lungs.
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

# this part of the code is the most computationally intensive part. 
#   Essentially, we want to time it to see how long it takes with and without vectorization. The for loop iterates through each image, counts the white and black pixels, calculates the percentage of white pixels, and stores the results in a list of dictionaries. 
# The use of NumPy's vectorized operations (like np.count_nonzero) makes this process much faster than iterating through each pixel manually.
for img, filename, depth in zip(images_loaded, filenames, depths):
    # img is directly available — no .index() lookup needed
    white_count = np.count_nonzero(img > 127)
    total_pixels = img.size
    black_count = total_pixels - white_count
    white_percent = (white_count / total_pixels) * 100
    white_percent_list.append(white_percent) # adding the white percent to a list for later use in interpolation and plotting
    clean_name = os.path.basename(filename) # os.path.basename() extracts just the filename from the full path, which is cleaner for the CSV output. This is more robust than manually splitting the string, as it works regardless of the operating system or path format.
    results.append({
        'Filename': clean_name,
        'Depth': depth,
        'White_Pixels': white_count,
        'Black_Pixels': black_count,
        'White_Percent': round(white_percent, 2)
    })

end_time = time.time()  # End timer for efficiency testing (before printing results) -- faster time --- averaging 0.00 to 0.01 seconds with vectorization, compared to 1.5 to 2 seconds initially without vectorization (when counting pixels with nested for loops instead of np.count_nonzero). This shows that vectorization is much more efficient for this type of pixel counting task.
total_time = end_time - start_time  # End timer for efficiency testing (after for loop)


# REQUIRED PRINT FORMAT FOR EACH IMAGE (for loop above):
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
# LECTURE 2: Interpolation (and possibly extrapolation)
# Interpolate a point: given a depth, find the corresponding white pixel percentage

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# interpolation instruction for the user to input a depth value for interpolation. 
#   The input function prompts the user to enter a depth in microns, which is then converted to a float for use in the interpolation process. 
interpolate_depth = float(input(colored(
"Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

x = depths
y = white_percent_list

# You can also use 'quadratic', 'cubic', etc.
# This is the interpolation function that will allow us to find the corresponding y value (percentage of white pixels) for any given x value (depth) within the range of our data. The 'kind' parameter specifies the type of interpolation, and in this case, we are using linear interpolation.
    # Essentially, the linear algebra side of our assigment: we are solving for the coefficients of a linear equation that best fits our data points, and then using those coefficients to compute the corresponding y value for a specific x value (the depth we want to interpolate at). The interp1d function from SciPy simplifies this process by creating an interpolation function that we can call with any x value to get the corresponding y value based on our original data points.
    # This interp1d function can also handle more complex cases such as quadratic or cubic interpolation, which can provide a better fit for data that is not well represented by a straight line. By changing the 'kind' parameter, we can easily switch between different types of interpolation to see which one best fits our data.
i = interp1d(x, y, kind='cubic')
interpolate_point = i(interpolate_depth)
print(colored(
    f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

depths_i = depths[:]
depths_i.append(interpolate_depth)
white_percents_i = white_percent_list[:]
white_percents_i.append(interpolate_point)


# make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
# Create a figure window containing 2 stacked plots (2 rows, 1 column).
# 'fig' = the whole window. 'axs' = array of the two plot panels.
# axs[0] is the top plot, axs[1] is the bottom plot.
fig, axs = plt.subplots(2, 1)

# PLOT #1 (top): raw measured data only 
# Plot the 6 real data points. scatter() draws individual dots.
# Note: linestyle='-' does nothing on scatter() — that's a plot() argument.
axs[0].scatter(depths, white_percent_list, marker='o', color='blue')
axs[0].set_title('Plot of depth of image vs percentage white pixels')
axs[0].set_xlabel('depth of image (in microns)')
axs[0].set_ylabel('white pixels as a percentage of total pixels')
axs[0].grid(True)   # adds background gridlines for readability

# PLOT #2 (bottom): same data + the interpolated point 
# depths_i and white_percents_i are copies of the original lists
# with the interpolated point appended as the 7th entry.
axs[1].scatter(depths_i, white_percents_i, marker='o', color='blue')
axs[1].set_title(
    'Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[1].set_xlabel('depth of image (in microns)')
axs[1].set_ylabel('white pixels as a percentage of total pixels')
axs[1].grid(True)

# Re-plot just the LAST item in the list (the interpolated point) in red.
# depths_i[-1] is a cleaner way to write depths_i[len(depths_i)-1] — same thing.
# s=100 makes the dot larger so it stands out visually.
axs[1].scatter(depths_i[-1], white_percents_i[-1],
               color='red', s=100, label='Highlighted point')

# Automatically adjusts spacing between the two plots so
# titles and axis labels don't overlap each other.
plt.tight_layout()

# Render and display the figure window on screen.
plt.show()