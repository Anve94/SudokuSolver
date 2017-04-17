# SudokuSolver
Solves a sudoku based on a given image

# To do
- Add more validation and cleanup validation
- Cleanup debug messaging stuff
- Cleanup other parts of code
- Add more comments to explain logic and functionality
- Fix PEP-8 complacancy issues (loads and loads and loads of them)
- Improve performance
- Work better with images in which the grid does not solely comprise of straight lines
- Better support for images that have a contrasting background, such as a table behind the paper

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

# Demo/Example
[Example input](http://i.imgur.com/KWsnQtA.jpg)

[Example output](http://i.imgur.com/uQLvG1R.png)

