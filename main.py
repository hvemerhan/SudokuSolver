from SudokuSolver import CameraCapture, ImagePreprocessor, GridDetector, DigitExtractor, SudokuSolver, SolutionDisplayer

def main():
    # Capture image
    camera = CameraCapture()
    image = camera.capture_image()

    # Preprocess image
    preprocessor = ImagePreprocessor()
    thresh = preprocessor.preprocess(image)

    # Detect grid
    detector = GridDetector()
    grid = detector.find_grid(thresh)
    warped = detector.warp_perspective(image, grid)

    # Extract digits
    extractor = DigitExtractor()
    board = extractor.extract_digits(warped)
    print("Extracted board:")
    print(board)

    # Solve Sudoku
    solver = SudokuSolver()
    solution = solver.solve_sudoku(board)
    print("Solution:")
    print(solution)

    # Display solution
    displayer = SolutionDisplayer()
    displayer.display_solution(image, grid, board, solution)

if __name__ == "__main__":
    main()
