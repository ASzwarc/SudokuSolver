import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

def main(filename: str) -> None:
    img_gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    img_color = cv.imread(filename, cv.IMREAD_UNCHANGED)
    if img_gray is not None and img_color is not None:
        print(f"Image {filename} successfuly read!")
        plot_image(find_lines(img_gray, img_color))
    else:
        print(f"Couldn't open image {filename} !")

def threshold_image(image):
    max_val: int = 255
    return cv.adaptiveThreshold(image, max_val, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 11, 2)

def find_lines(image_grayscale, image_color):
    edges = cv.Canny(image_grayscale, 200, 220, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1, np.pi/180.0, 200, 300, 4)
    # TODO this should be sorted and copied to another list
    found_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        found_lines.append((x1, y1, x2, y2))
    found_lines.sort()
    board_boundaries = []
    board_boundaries.append(found_lines[0])
    board_boundaries.append(found_lines[-1])
    found_lines.sort(key=lambda points: points[3])
    board_boundaries.append(found_lines[0])
    board_boundaries.append(found_lines[-1])
    print(board_boundaries)
    for boundary in board_boundaries:
        x1, y1, x2, y2 = boundary
        cv.line(image_color, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return cv.cvtColor(image_color, cv.COLOR_BGR2RGB)

def plot_image(image) -> None:
    plt.imshow(image)
    plt.show()

if __name__ == "__main__":
    main("input_images/SimpleBoard_1.PNG")
