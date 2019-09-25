import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
from typing import List, Tuple

# TODO add someting to recognize if frame is empty!


def main(filename: str) -> None:
    img_gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    img_color = cv.imread(filename, cv.IMREAD_UNCHANGED)
    if img_gray is not None and img_color is not None:
        print(f"Image {filename} successfuly read!")
        cropped_image = find_lines(img_gray, img_color)
        print(cropped_image.shape)
        plot_image(cropped_image, 'gray')
        boxes = resize_images_to_mnist(get_single_boxes(cropped_image))
        for i in range(9):
            plot_image(boxes[i], 'gray')
    else:
        print(f"Couldn't open image {filename} !")


def threshold_image(image):
    max_val: int = 255
    return cv.adaptiveThreshold(image, max_val, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 11, 2)


def find_lines(image_grayscale, image_color):
    def restructure_array(lines) -> List:
        return [line[0].tolist() for line in lines]

    def find_boundaries(lines: List) -> List:
        result = []
        lines.sort(key=lambda points: points[0])
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

    lowThreshold: int = 200
    highThreshold: int = 220
    rho: int = 1
    theta: int = np.pi/180
    threshold: int = 200
    minLineLength: int = 300
    maxLineGap: int = 4
    edges = cv.Canny(image_grayscale, lowThreshold, highThreshold,
                     apertureSize=3)
    lines = cv.HoughLinesP(edges, rho, theta, threshold, minLineLength,
                           maxLineGap)

    # draw_boundary(find_boundaries(restructure_array(lines)))
    # plot_image(cv.cvtColor(image_color, cv.COLOR_BGR2RGB), None)
    return crop_image(find_boundaries(restructure_array(lines)))


def get_single_boxes(image):
    width, height = image.shape
    box_width = width // 9
    box_height = height // 9

    single_boxes = []
    for x in range(9):
        for y in range(9):
            start_x: int = x * box_width
            start_y: int = y * box_height
            single_boxes.append(image[start_x:(start_x + box_width),
                                      start_y:(start_y + box_height)])
    return single_boxes


def resize_images_to_mnist(image_list):
    mnist_dim: Tuple[int, int] = (28, 28)
    result = []
    for image in image_list:
        result.append(cv.resize(image, mnist_dim, interpolation=cv.INTER_AREA))
    return result


def plot_image(image, color: str) -> None:
    plt.imshow(image, cmap=color)
    plt.show()


if __name__ == "__main__":
    main("input_images/SimpleBoard_1.PNG")
