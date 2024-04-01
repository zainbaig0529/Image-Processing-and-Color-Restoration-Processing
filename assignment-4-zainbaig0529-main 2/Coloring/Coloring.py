import dip
import math
from dip import *


class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
       Steps:
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
       returns colored image
       '''
        # Get image dimensions
        height, width = image.shape[:2]

        # Determine the size of each interval
        interval_size = 255 // n_slices

        # Create a list of intervals
        intervals = []
        for i in range(n_slices):
            intervals.append(i * interval_size)
        intervals.append(255)

        # Randomly assign a color to each interval
        colors = []
        for i in range(n_slices):
            colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Create the color image
        color_image = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append((0, 0, 0))
            color_image.append(row)

        # Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
        for i in range(height):
            for j in range(width):
                intensity = image[i][j]
                for k in range(n_slices + 1):
                    if intensity < intervals[k]:
                        color_image[i][j] = colors[k - 1]
                        break
        return image

    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b)
        Steps:
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
        returns colored image
        '''
        # Get image dimensions
        height, width = image.shape[:2]

        # Determine the size of each interval
        interval_size = 255 // n_slices

        # Create a list of intervals
        intervals = []
        for i in range(n_slices):
            intervals.append(i * interval_size)
        intervals.append(255)

        # Create red, green and blue values for each slice using sin function and theta values
        red_values = []
        green_values = []
        blue_values = []
        for i in range(n_slices + 1):
            red_values.append(int(255 * math.sin(i * interval_size * math.pi / 255 + theta[0])))
            green_values.append(int(255 * math.sin(i * interval_size * math.pi / 255 + theta[1])))
            blue_values.append(int(255 * math.sin(i * interval_size * math.pi / 255 + theta[2])))

        # Create the color image
        color_image = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append((0, 0, 0))
            color_image.append(row)

        # Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
        for i in range(height):
            for j in range(width):
                intensity = image[i][j]
                for k in range(n_slices + 1):
                    if intensity < intervals[k]:
                        color_image[i][j] = (red_values[k - 1], green_values[k - 1], blue_values[k - 1])
                        break
        return image


