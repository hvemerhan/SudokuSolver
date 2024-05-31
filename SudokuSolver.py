import cv2
import numpy as np
import pytesseract

""" Capture image from camera"""
class CameraCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def capture_image(self):
        while True:
            ret, frame = self.cap.read()
            cv2.imshow('Capture Sudoku', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()
        return frame

""" Preprocess image"""
class ImagePreprocessor:
    def preprocess(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return thresh

""" Detect grid and warp perspective"""
class GridDetector:
    def find_grid(self, thresh):
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:
                return approx
        return None

    def warp_perspective(self, image, grid):
        pts = np.float32([grid[0], grid[1], grid[2], grid[3]])
        side = max([np.linalg.norm(grid[i] - grid[(i + 1) % 4]) for i in range(4)])
        dst_pts = np.float32([[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]])
        M = cv2.getPerspectiveTransform(pts, dst_pts)
        return cv2.warpPerspective(image, M, (int(side), int(side)))

""" Extract digits from cells"""
class DigitExtractor:
    def extract_digits(self, warped):
        side = warped.shape[0] // 9
        board = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                cell = warped[i*side:(i+1)*side, j*side:(j+1)*side]
                text = pytesseract.image_to_string(cell, config='--psm 10')
                text = ''.join(filter(str.isdigit, text))
                board[i, j] = int(text) if text else 0
        return board

""" Solve Sudoku"""
class Solver:
    def solve_sudoku(self, board):
        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if board[i][j] == num:
                        return False
            return True

        def solve(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        board_copy = np.copy(board)
        solve(board_copy)
        return board_copy

""" Display solution"""
class SolutionDisplayer:
    def display_solution(self, image, grid, board, solution):
        side = image.shape[0] // 9
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:  # Only overlay the solution digits
                    x = int((grid[0][0][0] + grid[1][0][0]) / 2 + j * side)
                    y = int((grid[0][0][1] + grid[3][0][1]) / 2 + i * side)
                    cv2.putText(image, str(solution[i][j]), (x, y), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Solved Sudoku', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

""" Main function"""
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
    solver = Solver()
    solution = solver.solve_sudoku(board)
    print("Solution:")
    print(solution)

    # Display solution
    displayer = SolutionDisplayer()
    displayer.display_solution(image, grid, board, solution)

if __name__ == "__main__":
    main()
