import cv2 as cv
from matplotlib import pyplot as plt

def main(filename: str) -> None:
    img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    if img is not None:
        print(f"Image {filename} successfuly read!")
        plot_image(img)
    else:
        print(f"Couldn't open image {filename} !")

def plot_image(image) -> None:
    plt.imshow(image, cmap='gray')
    plt.show()

if __name__ == "__main__":
    main("input_images/SimpleBoard_1.PNG")
