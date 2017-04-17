import cv2
from decorators import check_debug
from settings import MAX_HEIGHT_ALLOWED, MAX_WIDTH_ALLOWED, ENABLE_DEBUG


class ImagePrepper(object):
    ''' The ImagePrepper class prepares any image to conform to
        a given static ruleset, such as maximum dimensions. Additionally,
        the class prepares any inputted image to make sure the next
        class in the build-chain can correctly handle and read the image.
        It also validates input, such as pixel density and
        check if it can handle the given file extension. (jpg, png etc.) '''

    @check_debug
    def __init__(self, img_link):
        self.image = cv2.imread(img_link)
        self.height, self.width, self.channels = self.image.shape
        if self.needs_resize():
            self.resize()

    @check_debug
    def needs_resize(self):
        ''' Determine if the given image requires a resize. '''
        if (self.height > MAX_HEIGHT_ALLOWED or
                self.width > MAX_WIDTH_ALLOWED):
            if ENABLE_DEBUG:
                print("DEBUG -- Image needs a resize.")
            return True
        return False

    @check_debug
    def resize(self):
        ''' Resize the image to conform to MAX static ruleset '''
        # Requires that the given image does not exceed the max contraints
        if ENABLE_DEBUG:
            print("DEBUG -- Attempting image resize")
        if self.height > self.width:
            # Determine new image dimensions:
            # The amount to remove from the height of the image to conform
            # to constraints.
            height_shrinkable = self.height - MAX_HEIGHT_ALLOWED
            # The percentage at which the image is shrunk
            height_shrink_percent = (float(height_shrinkable) /
                                     self.height * 100)
            # The new image height and width
            new_height = self.height - height_shrinkable
            new_width = (self.width *
                         ((100 - float(height_shrink_percent)) / 100))
            new_width = int(new_width)
        elif self.width > self.height:
            # Determine new image dimensions
            # Amount to be removed from width to conform to constraint
            width_shrinkable = self.width - MAX_WIDTH_ALLOWED
            # Percentage at which image is shrunk
            width_shrink_percent = float(width_shrinkable) / self.width * 100
            # The new image width and height
            new_width = self.width - width_shrinkable
            new_height = (self.height *
                          ((100 - float(width_shrink_percent)) / 100))
            new_height = int(new_height)
        else:
            # Otherwise, image is a square
            new_height = MAX_HEIGHT_ALLOWED
            new_width = MAX_WIDTH_ALLOWED

        # Perform the resize operation with calculated values
        self.image = cv2.resize(
            self.image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA)
        if ENABLE_DEBUG:
            print("DEBUG -- Image succesfully resized.")
