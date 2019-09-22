import cv2 as cv
from matplotlib import pyplot as plt

def main(filename: str) -> None:
    img_gray = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    img_color = cv.imread(filename, cv.IMREAD_UNCHANGED)
    if img_gray is not None and img_color is not None:
        print(f"Image {filename} successfuly read!")
        plot_image(find_lines(threshold_image(img_gray), img_color))
    else:
        print(f"Couldn't open image {filename} !")

def threshold_image(image):
    max_val: int = 255
    return cv.adaptiveThreshold(image, max_val, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 11, 2)

def find_lines(image_grayscale, image_color):
    lines = cv.HoughLinesP(image_grayscale, 1, 3.14/180.0, 100, 100, 10)
    for x1, y1, x2, y2 in lines[0]:
        print(f"Found lines: ({x1}, {y1}) - ({x2}, {y2})")
        cv.line(image_color, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return cv.cvtColor(image_color, cv.COLOR_BGR2RGB)

def plot_image(image) -> None:
    plt.imshow(image)
    plt.show()

if __name__ == "__main__":
    main("input_images/SimpleBoard_1.PNG")
