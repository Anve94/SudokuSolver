import settings
# import cv2
# from decorators import check_debug
from ImagePrepper import ImagePrepper
from ImageExtractor import ImageExtractor
from SudokuSolver import SudokuSolver
from helper_functions import image_preview, display_solution
from sys import exit


if __name__ == "__main__":
    if settings.ENABLE_DEBUG:
        print("DEBUG GLOBAL -- Main script execution started.")
        print("DEBUG GLOBAL -- Attempting to load image.")

    # Attempt to load the image
    try:
        image_container = ImagePrepper(settings.FILE_NAME)
    except:
        if settings.VERBOSE_EXIT:
            print("ERROR -- Failed to load image. Does the image "
                  "exist? Do you have a typo? Note: only .png, .jpg and "
                  ".jpeg files are supported.")
        exit()
    if settings.ENABLE_DEBUG:
        print("DEBUG GLOBAL -- Image succesfully loaded.")
        print("DEBUG GLOBAL -- Attempting to extract values from image.")
    # Show preview if enabled in the settings
    if settings.ENABLE_PREVIEW or settings.ENABLE_PREVIEW_ALL:
        image_preview(image_container.image)

    extracted_info = ImageExtractor(image_container.image)
    sudoku_solver = SudokuSolver(extracted_info.starting_grid)
    board_is_valid = sudoku_solver.board_is_valid()

    if not board_is_valid:
        if settings.VERBOSE_EXIT:
            print("ERROR -- Starting values found in sudoku were not valid.")
            print("The following board was found: ")
            sudoku_solver.print_sudoku()
        exit()

    if settings.ENABLE_DEBUG:
        print("DEBUG -- Following starting board was found: ")
        sudoku_solver.print_sudoku()

    if settings.ENABLE_DEBUG:
        print("DEBUG -- Attempting to solve the sudoku.")

    sudoku_solver.solve(sudoku_solver.board)

    if settings.ENABLE_DEBUG:
        print("DEBUG -- Solution to sudoku was found:")
        sudoku_solver.print_sudoku()

    # Write the solution to the image and preview it.
    if sudoku_solver.is_solved:
        if settings.ENABLE_DEBUG:
            print("DEBUG -- Sudoku succesfully solved.")

    else:
        if settings.VERBOSE_EXIT:
            print("ERROR -- Sudoku could not be solved.")
        exit()

    display_solution(square_borders=extracted_info.square_borders,
                     start_grid=extracted_info.starting_grid,
                     solution=sudoku_solver.board,
                     image=extracted_info.warp)

    if settings.ENABLE_DEBUG:
        print("DEBUG GLOBAL -- Script finished execution.")
