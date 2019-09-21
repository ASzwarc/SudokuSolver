import cv2 as cv

def main(filename: str) -> None:
    img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    if img is not None:
        print(f"Image {filename} successfuly read!")
    else:
        print(f"Couldn't open image {filename} !")

if __name__ == "__main__":
    main("input_images/SimpleBoard_1.PNG")
