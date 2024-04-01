import dip
from dip import *


class Filtering:

    def __init__(self, image, filter_name, filter_size, var=None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler

        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size

        # global_var: noise variance to be used in the Local noise reduction filter
        self.global_var = var

        # S_max: Maximum allowed size of the window that is used in adaptive median filter
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        n = len(roi)
        if n == 0:
            return 0
        else:
            total = sum(roi)
            return total / n

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        n = len(roi)
        if n == 0:
            return 0
        else:
            product = 1
            for value in roi:
                product *= value
            return product ** (1 / n)

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        n = len(roi)
        if n == 0:
            return 0
        else:
            # Compute the arithmetic mean of the roi
            mean = sum(roi) / n

            # Compute the sum of squared differences between each pixel and the mean
            ssd = 0
            for value in roi:
                diff = value - mean
                ssd += diff * diff

            # Compute the local noise reduction value as the square root of the mean of the squared differences
            return (ssd / n) ** 0.5

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        n = len(roi)
        if n == 0:
            return 0
        else:
            # Sort the roi in ascending order
            sorted_roi = sorted(roi)

            # Compute the median of the roi
            if n % 2 == 0:
                # If the roi has an even number of elements, compute the average of the two middle elements
                middle_idx = n // 2
                median = (sorted_roi[middle_idx - 1] + sorted_roi[middle_idx]) / 2
            else:
                # If the roi has an odd number of elements, take the middle element
                middle_idx = n // 2
                median = sorted_roi[middle_idx]

            return median

    def get_adaptive_median(self, image, window_size, max_window_size):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """

        # Define helper functions
        def get_median(pixels):
            """Returns the median value of a list of pixel values."""
            sorted_pixels = sorted(pixels)
            median = sorted_pixels[len(sorted_pixels) // 2]
            return median

        def get_window(image, row, col, size):
            """Returns a window of pixels from the input image centered at the given row and column indices."""
            half_size = size // 2
            window = []
            for i in range(row - half_size, row + half_size + 1):
                for j in range(col - half_size, col + half_size + 1):
                    if 0 <= i < len(image) and 0 <= j < len(image[0]):
                        window.append(image[i][j])
            return window

        # Initialize output image
        output = [[0] * len(image[0]) for _ in range(len(image))]

        # Iterate over every pixel in the image
        for i in range(len(image)):
            for j in range(len(image[0])):

                # Initialize window size
                window_size_cur = window_size

                while window_size_cur <= max_window_size:

                    # Get window of pixels
                    window = get_window(image, i, j, window_size_cur)

                    # Calculate median value
                    median = get_median(window)

                    # Check if pixel value is within the range [median - (size/2), median + (size/2)]
                    if (median - (window_size_cur // 2)) <= image[i][j] <= (
                            median + (window_size_cur // 2)):
                        output[i][j] = image[i][j]
                        break  # stop iterating over larger window sizes
                    else:
                        window_size_cur += 2  # increase window size

                        # If maximum window size is reached, just output the median value
                        if window_size_cur > max_window_size:
                            output[i][j] = median
                            break  # stop iterating over larger window sizes

        return output

    def filtering(self, filter_type='median', kernel_size=3):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.
        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image
        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        # Add zero padding to the image
        padded_image = self.pad_image(self.image, kernel_size // 2)
        output_image = [[0 for _ in range(len(self.image[0]))] for _ in range(len(self.image))]

        # Define the filter function based on the selected filter type
        if filter_type == 'median':
            filter_func = self.median_filter

        # Iterate over each pixel in the image
        for i in range(kernel_size // 2, len(self.image) + kernel_size // 2):
            for j in range(kernel_size // 2, len(self.image[0]) + kernel_size // 2):
                # Collect neighboring pixels defined by the kernel into a list
                neighbors = []
                for ii in range(i - kernel_size // 2, i + kernel_size // 2 + 1):
                    for jj in range(j - kernel_size // 2, j + kernel_size // 2 + 1):
                        neighbors.append(padded_image[ii][jj])

                # Apply the filter function to the collected pixels and save the result
                output_image[i - kernel_size // 2][j - kernel_size // 2] = filter_func(neighbors)

        return output_image

    def pad_image(self, image, padding):
        # Add zero padding to the image
        padded_image = [[0 for _ in range(len(image[0]) + 2 * padding)] for _ in range(len(image) + 2 * padding)]
        for i in range(padding, len(image) + padding):
            for j in range(padding, len(image[0]) + padding):
                padded_image[i][j] = image[i - padding][j - padding]
        return padded_image

    def median_filter(self, neighbors):
        # Compute the median of the collected pixels
        neighbors.sort()
        return neighbors[len(neighbors) // 2]
