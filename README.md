# SudokuSolver
Solves a sudoku based on a given image

# To do
- Cleanup debug messaging stuff
- Improve performance
- Work better with images in which the grid does not solely comprise straight line
- Better support for images that have a contrasting background, such a table behind the paper

# Requirements to run this software
- Python 2.7
- OpenCV (incl PIP package)
- Pytesseract
- Native Tesseract OCR Engine callable from shell
- PIL PIP package
- Some other stuff I cannot remember right now

# Execution
- Save an image of a sudoku (.jpg, .jpeg or .png) in the same directory
- Change the FILE_NAME variable in settings.py
Run
```
$ python main.py
```

