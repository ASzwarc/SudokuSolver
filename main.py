import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
from typing import List

def main(filename: str) -> None:
    img_gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    img_color = cv.imread(filename, cv.IMREAD_UNCHANGED)
    if img_gray is not None and img_color is not None:
        print(f"Image {filename} successfuly read!")
        plot_image(find_lines(img_gray, img_color), 'gray')
    else:
        print(f"Couldn't open image {filename} !")

def threshold_image(image):
    max_val: int = 255
    return cv.adaptiveThreshold(image, max_val, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 11, 2)

def find_lines(image_grayscale, image_color):
    def restructure_array(lines: List) -> List:
        result = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            result.append((x1, y1, x2, y2))
        return result

    def find_boundaries(lines: List) -> List:
        result = []
        lines.sort()
        result.append(lines[0])
        result.append(lines[-1])
        lines.sort(key=lambda points: points[3])
        result.append(lines[0])
        result.append(lines[-1])
        return result

    def draw_boundary(boundaries: List) -> None:
        color = (0, 255, 0)
        width = 2
        for boundary in boundaries:
            x1, y1, x2, y2 = boundary
            cv.line(image_color, (x1, y1), (x2, y2), color, width)

    def crop_image(boundaries: List):
        x1 = boundaries[0][0]
        x2 = boundaries[1][0]
        y1 = boundaries[2][1]
        y2 = boundaries[3][1]

        return image_grayscale[x1:x2, y1:y2]
    #TODO name this parameters
    edges = cv.Canny(image_grayscale, 200, 220, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1, np.pi/180.0, 200, 300, 4)

    draw_boundary(find_boundaries(restructure_array(lines)))
    plot_image(cv.cvtColor(image_color, cv.COLOR_BGR2RGB), None)
    return crop_image(find_boundaries(restructure_array(lines)))

def plot_image(image, color: str) -> None:
    plt.imshow(image, cmap=color)
    plt.show()

if __name__ == "__main__":
    main("input_images/SimpleBoard_1.PNG")
