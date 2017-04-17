'''
Main Settings for script execution.
Change the settings here to adjust how the script is run.
@author: Stefan Boonstra
@author_email: st.boonstra@st.hanze.nl

This software was created for educational purposes. The license as available
within this folder applies. Software is provided as-is. USE AT YOUR OWN RISK.
'''
FILE_NAME = 'sudoku_skewed.jpg'
ENABLE_PREVIEW = True  # Preview important intermediary CV2 filters/results
ENABLE_PREVIEW_ALL = False  # Preview ALL cv2 filters/results
# Debug full script execution. Note: OCR results are NOT included.
ENABLE_DEBUG = False
ENABLE_OCR_DEBUG = True  # Show intermediary OCR results in terminal
VERBOSE_EXIT = True  # When enabled, print an error upon execution fails

# Open CV settings
MAX_HEIGHT_ALLOWED = 900  # The maximum allowed height of a loaded image
MAX_WIDTH_ALLOWED = 900  # The maximum allowed width of a loaded image
BLUR_KERNEL_SIZE = (5, 5)  # The kernel sized used for the blur filter
