# SudokuSolver
Solves a sudoku based on a given image

# Demo/Example
[Example input](http://i.imgur.com/KWsnQtA.jpg)

[Example output](http://i.imgur.com/uQLvG1R.png)

# To do
- Add requirements.txt file to help with installation of PIP packages;
- Add more validation and cleanup validation;
- Cleanup debug messaging stuff;
- Cleanup other parts of code;
- Add more comments to explain logic and functionality;
- Fix PEP-8 compliancy issues (loads and loads and loads of them);
- Improve performance;
- Work better with images in which the grid does not solely comprise of straight lines;
- Better support for images that have a contrasting background, such as a table behind the paper.

# Requirements to run this software
- Python 2.7
- OpenCV locally installed
- Pytesseract and PIL PIP package
- Native Tesseract OCR Engine locally installed and callable from shell

# Execution
- Save an image of a sudoku (.jpg, .jpeg or .png) in the same directory
- Change the FILE_NAME variable in settings.py
- Run
```
$ python main.py
```
