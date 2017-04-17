import cv2
from settings import (BLUR_KERNEL_SIZE, ENABLE_PREVIEW, ENABLE_DEBUG,
                      ENABLE_PREVIEW_ALL, ENABLE_OCR_DEBUG, VERBOSE_EXIT)

from decorators import check_debug
from helper_functions import image_preview
from sys import exit
from copy import deepcopy
import numpy as np
import pytesseract  # Wrapper to Tesseract OCR engine
# Python Image Library to convert image so Tesseract can understand the format
from PIL import Image

DEV_EMAIL = "st.boonstra@st.hanze.nl"


class ImageExtractor(object):
    """ This class contains all the methods, functions and algorithms
    to extract valuable data from a given image. This class is used to
    perform operations on the image, as well as grabbing the values from
    the image using OCR and storing it as a list. """

    def __init__(self, image):
        self.original_image = image  # The original image from the user
        self.grayscale = self.to_grayscale(image)  # Grayscale version of image
        # Apply gaussian blur to grayscale image
        self.blurred = self.apply_blur(self.grayscale)
        self.thresh = self.to_binary(self.blurred)
        self.biggest_contour = self.find_grid(self.thresh)
        self.warp = self.extract_grid(self.biggest_contour,
                                      self.original_image)
        self.square_borders = self.calc_square_borders(self.warp)
        self.starting_grid = self.extract_sudoku_values(self.warp,
                                                        self.square_borders)

    @check_debug
    def to_grayscale(self, image):
        """ Transform the given image to grayscale """
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting to transform image to grayscale.")
        try:
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except:
            if VERBOSE_EXIT:
                print("ERROR -- Could not convert image to grayscale.")
            exit()
        if ENABLE_PREVIEW_ALL:
            image_preview(grayscale)
        if ENABLE_DEBUG:
            print("DEBUG -- Image succesfully converted to grayscale.")
        return grayscale

    @check_debug
    def apply_blur(self, image):
        """ Adds a blur to the given image, using the kernel size
            defined in settings. """
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting to apply gaussian blur to"
                  " grayscale image.")
        try:
            blurred = cv2.GaussianBlur(src=image,
                                       ksize=BLUR_KERNEL_SIZE,
                                       sigmaX=0)
        except:
            if VERBOSE_EXIT:
                print("ERROR -- Could not apply blur filter. Please check"
                      " settings and consider changing the blur kernel size.")
            exit()
        if ENABLE_PREVIEW_ALL:
            image_preview(blurred)
        if ENABLE_DEBUG:
            print("DEBUG -- Gaussian Blur succesfully applied.")
        return blurred

    @check_debug
    def to_binary(self, image):
        """ This method uses Adaptive Thresholding to convert
            a blurred grayscale image to binary (only black and white).
            The binary image is required to extract the full sudoku grid
            from the image. """
        if ENABLE_DEBUG:
                print("DEBUG -- Attempting to apply adaptive threshold"
                      " and convert image to black and white.")
        try:
            thresh = cv2.adaptiveThreshold(image, 255, 1, 1, 11, 2)
        except:
            if VERBOSE_EXIT:
                print("ERROR -- Unable to convert the image to black/white."
                      " Please contact the developer at %s and include this"
                      " error and the image you are using." % DEV_EMAIL)
            exit()
        if ENABLE_PREVIEW or ENABLE_PREVIEW_ALL:
            image_preview(thresh)
        if ENABLE_DEBUG:
            print("DEBUG -- Image succesfully converted to binary.")
        return thresh

    def apply_filters(self, image, denoise=False):
        """ This method is used to apply required filters to the
            to extracted regions of interest. Every square in a
            sudoku square is considered to be a region of interest,
            since it can potentially contain a value. """
        # Convert to grayscale
        source_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Denoise the grayscale image if requested in the params
        if denoise:
            denoised_gray = cv2.fastNlMeansDenoising(source_gray, None, 9, 13)
            source_blur = cv2.GaussianBlur(denoised_gray, BLUR_KERNEL_SIZE, 3)
            # source_blur = denoised_gray
        else:
            source_blur = cv2.GaussianBlur(source_gray, (3, 3), 3)
        source_thresh = cv2.adaptiveThreshold(source_blur, 255, 0, 1, 5, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        source_eroded = cv2.erode(source_thresh, kernel, iterations=1)
        source_dilated = cv2.dilate(source_eroded, kernel, iterations=1)
        if ENABLE_PREVIEW_ALL:
            image_preview(source_dilated)
        return source_dilated

    @check_debug
    def find_grid(self, image):
        """ Extract the sudoku grid from the black/white image. """
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting to extract the sudoku grid"
                  " from the image.")
        # Find all the closed shapes in the thresholded image
        contours, hierarchy = cv2.findContours(
                                image=image,
                                mode=cv2.RETR_LIST,
                                method=cv2.CHAIN_APPROX_SIMPLE)

        # The minimal area required for a closed shape to be considered as
        # a possible grid.
        min_viable_area = 500
        # Keeps track of the highest area that was found
        max_area_found = 0
        biggest_contour_found = None  # Saves the biggest contour found
        # Iterate over every contour to find the one with the largest area
        for i, cnt in enumerate(contours):
            # NL: Oppervlakte
            cur_area = cv2.contourArea(cnt)
            # Don't waste calculations on contours that are too small
            # to be considered the largest anyway.
            if cur_area > min_viable_area:
                # NL: Omtrek
                perimeter = cv2.arcLength(cnt, True)
                # More info: http://docs.opencv.org/2.4/modules/imgproc/
                # doc/structural_analysis_and_shape_descriptors.html#approxpolydp
                # Approximates the curves of a contour based on the given
                # precision.
                approx = cv2.approxPolyDP(
                    curve=cnt,
                    epsilon=0.02 * perimeter,
                    closed=True)
                # Length refers to the amount of corners.
                # 4 corners = square/rectangle
                if(cur_area > max_area_found and
                   len(approx) == 4):
                        # If the current contour (with approximated curves)
                        # is bigger than the one known, save that contour
                        # and replace the currently known largest area with the
                        # new area (since it is now the biggest one found)
                        biggest_contour_found = approx
                        max_area_found = cur_area
                        # contour_index_found = i

        if ENABLE_PREVIEW or ENABLE_PREVIEW_ALL:
            # To show the biggest contour in the image, it needs
            # to be drawn. So a copy is made of the original image.
            # That way, the original image does not have to be modified
            # and a copied version can be drawn instead.
            _ = deepcopy(self.original_image)
            cv2.drawContours(
                image=_,
                contours=[biggest_contour_found],
                contourIdx=0,
                color=(255, 0, 0))
            image_preview(_)
        if ENABLE_DEBUG:
            print("DEBUG -- Succesfully found the sudoku grid in"
                  " the image.")
        return biggest_contour_found

    @check_debug
    def extract_grid(self, contour, image):
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting to extract the sudoku grid from"
                  " the image.")
        # The corners of the contour (including the curve approximation)
        # need to be put in clock-wise order (top-left -> top-right
        # bottom-right -> bottom-left). This is not yet the case so
        # new corners must be calculated.

        # Reshape the array to look as follows:
        # array([[0, 0],
        #        [0, 0],
        #        [0, 0],
        #        [0, 0]])
        points = contour.reshape(4, 2)
        # Initialize an empty array with zeros,
        # so that the corner points can be stored later
        rectangle_corners = np.zeros(
            (4, 2),
            dtype="float32")

        points_sum = points.sum(axis=1)
        # If we look at the SUM of all corners (x, y) pairs, assuming the full
        # image starts at position 0, 0 at the top-left, we can sum all the
        # coordinate pairs. Afterward, the most top-left corner will have the
        # LOWEST sum (closest to 0, 0) and the bottom-right corner will have
        # the HIGHEST sum (farthest from 0, 0). With this knowledge, we can
        # already place the x, y coordinates for the top-left and bottom-right
        # corner in the corner array
        rectangle_corners[0] = points[np.argmin(points_sum)]
        rectangle_corners[2] = points[np.argmax(points_sum)]

        # We can sortof do the same for the remaining two corners (top-right
        # and bottom-left) but by using the DIFFERENCE between (x,y) coordinate
        # pairs
        points_difference = np.diff(points, axis=1)
        rectangle_corners[1] = points[np.argmin(points_difference)]
        rectangle_corners[3] = points[np.argmax(points_difference)]

        # Perspective warping and calculations. Calculates a destination size
        # for the warped image. Code loosely based on the official OpenCV
        # documentation and based on some default OpenCV examples provided with
        # the library itself.

        # First, extract the rectangle corner points
        top_right, top_left, bot_right, bot_left = rectangle_corners
        # Note: for each corner there is an x ([0]) and a y ([1]) coordinate
        # The width of the bottom side of the new image
        bot_width = np.sqrt(((bot_right[0] - bot_left[0]) ** 2) +
                            ((bot_right[1] - bot_left[1]) ** 2))
        # The width of the top side of the new image
        top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) +
                            ((top_right[1] - top_left[1]) ** 2))
        # The right side height of the new image
        right_height = np.sqrt(((top_right[0] - bot_right[0]) ** 2) +
                               ((top_right[1] - bot_right[1]) ** 2))
        # The left side height of the new image
        left_height = np.sqrt(((top_left[0] - bot_left[0]) ** 2) +
                              ((top_left[1] - bot_left[1]) ** 2))

        # The hight width and height that were found will be the
        # dimensions of our new image
        max_width = max(int(bot_width), int(top_width))
        max_height = max(int(right_height), int(left_height))

        # With the values found above, a new image can be constructed using the
        # previously calculated dimensions. Image corners are once again in
        # clockwise order, starting at 0,0/x,y(top-left) -> top-right ->
        # bottom-right -> bottom-left.
        destination_image = np.array([
            [0, 0],  # Top left corner
            [max_width, 0],  # Top right corner
            [max_width, max_height],  # Bottom right corner
            [0, max_height]],  # Bottom left corner
            dtype="float32")  # Datatype that the array is constructed with

        # With the targeted destination image as well as the original
        # coordinates found, the image can be warped towards the other,
        # essentially stretching out the pixels and making them fit the
        # targeted size/dimension
        pt = cv2.getPerspectiveTransform(rectangle_corners, destination_image)
        warp = cv2.warpPerspective(image, pt, (max_width, max_height))
        warp = cv2.resize(warp,
                          (450, 450),
                          interpolation=cv2.INTER_AREA)
        if ENABLE_DEBUG:
            print("DEBUG -- Succesfully extracted the sudoku grid from"
                  " the image.")
        if ENABLE_PREVIEW or ENABLE_PREVIEW_ALL:
            image_preview(warp)
        return warp

    @check_debug
    def calc_square_borders(self, image):
        """ Given a extracted sudoku grid, calculate the borders of
            each individual square of that grid. """
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting to calculate sudoku square borders.")

        crop_width = image.shape[1]
        crop_height = image.shape[0]

        square_borders = []
        x_pointer = 0
        y_pointer = 0

        square_width, square_height = crop_width / 9, crop_height / 9
        # Let's find 81 squares and save the top left and bottom right
        # coordinates for each square
        for row in xrange(0, 9):
            y_start = y_pointer
            y_end = y_start + square_width
            y_pointer = y_end
            if y_pointer == crop_width:
                y_pointer += square_width
                y_pointer = 0

            for col in xrange(0, 9):
                x_start = x_pointer
                x_end = x_start + square_height
                x_pointer = x_end
                if x_pointer == crop_height:
                    x_pointer += square_height
                    x_pointer = 0
                t = (xs, ys, xe, ye) = x_start, y_start, x_end, y_end
                square_borders.append(t)
        if ENABLE_DEBUG:
            print("DEBUG -- Succesfully found sudoku square borders.")

        if ENABLE_PREVIEW or ENABLE_PREVIEW_ALL:
            _ = deepcopy(image)
            for i, b in enumerate(square_borders):
                x, y, x2, y2 = b
                cv2.rectangle(_, (x, y), (x2, y2), (255, 0, 0))
            image_preview(_)

        return square_borders

    @check_debug
    def extract_sudoku_values(self, warp, square_borders):
        """ Uses the transformed image and the Tesseract OCR engine
            to find and store all the values inside the individual
            sudoku squares. """
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting to read and store values"
                  " from within the sudoku grid.")
        # 2D list of number results
        sudoku_start_grid = []
        # Keep track of intermediary rows
        sudoku_row = []
        # Fetch region of interest, read data with Tesseract OCR Engine
        # and append to start grid
        for i, borders in enumerate(square_borders):
            x, y, x2, y2 = borders  # Tuple unpacking
            w = x2 - x  # Determine width
            h = y2 - y  # Determine height
            roi = warp[y+6:y2-6, x+6:x2-6]  # Region of interest/individual square
            roi = self.apply_filters(roi, denoise=True)  # Apply filters to ROI
            w, h = roi.shape
            PIL_image = Image.fromarray(roi)
            value = pytesseract.image_to_string(
                PIL_image,
                config='--tessdata-dir /usr/share/tesseract-ocr -psm 10 digits')
            if ENABLE_OCR_DEBUG:
                print("DEBUG OCR -- value found: %s" % value)
            # If a value is found in the square, append the value.
            if value:
                sudoku_row.append(int(value))
            # Otherwise, append a 0.
            else:
                sudoku_row.append(0)
            # Each row has 9 values, and each grid has 9 rows.
            # If the row list reached 9, it can be appended to the grid
            if len(sudoku_row) == 9:
                sudoku_start_grid.append(sudoku_row)
                if ENABLE_OCR_DEBUG:
                    print("DEBUG OCR -- Values found in current row:")
                    print(sudoku_row)
                sudoku_row = []
        if ENABLE_DEBUG:
            print("DEBUG -- Sudoku values succesfully stored.")
        return sudoku_start_grid
