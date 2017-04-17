""" This file contains helper function not attributed to any class
    but still helpful in the main execution of the program. Added to be able
    to adhere to the DRY principle. """
import cv2


def image_preview(image):
    cv2.imshow('Image preview', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_solution(square_borders, start_grid, solution, image):
    """ Writes the solution to an image and displays said image.
        Params:
            square_borders  -- A list containing the borders of all squares
            start_grid      -- A list containing the sudoku starting values
            solution        -- A list containing the sudoku solution
            image           -- The image to write to """
    cur_row = 0
    cur_col = 0
    for i, b in enumerate(square_borders):
        x, y, x2, y2 = b  # Tuple unpacking
        # Calculate bottom-left position for text
        text_x, text_y = ((x2+x) / 2) - 10, ((y2+y) / 2) + 10
        # Bottom-left corner for text position
        org = (text_x, text_y)
        # Only write text if the position was not set in the start_grid
        if start_grid[cur_row][cur_col] is 0:
            value = str(solution[cur_row][cur_col])
            cv2.putText(
                img=image,
                text=value,
                org=org,
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(0, 255, 0),
                thickness=2)
        cur_col += 1
        if cur_col % 9 == 0:
            cur_row += 1
            cur_col = 0

    cv2.imshow('Solution', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
