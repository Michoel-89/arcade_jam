# tutorial code: https://github.com/kiteco/python-youtube-code/blob/master/ascii/ascii_convert.py
import cv2

# ascii characters used to build the output text
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", "'", "\"", "`", "^", "<", ">", "(", ")", "{", "}", "[", "]", "|", "_", "-", "=", "~", "/", "\\", " ", " "]

# resize image according to a new width
def resize_image(image, new_width=100):
    height, width, _ = image.shape
    # adjust for ascii characters' height being 2x large than width (ratio may vary depending on display)
    ratio = height / 2 / width  
    new_height = int(new_width * ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

# convert each pixel to grayscale
def grayify(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return grayscale_image

# convert pixels to a string of ascii characters
def pixels_to_ascii(image):
    rows, cols = image.shape
    characters = ""
    for i in range(rows):
        for j in range(cols):
            pixel = image[i, j] // 25
            characters += ASCII_CHARS[pixel]
        characters += "\n"
    return characters

def main(new_width=100):
    # # attempt to open image from user-input
    path = input("Enter a valid pathname to an image:\n")
    # path = 'download.png'
    image = cv2.imread(path)
    if image is None:
        print(path, " is not a valid pathname to an image.")
        return

    # convert image to ascii
    resized_image = resize_image(image, new_width=new_width)
    grayscale_image = grayify(resized_image)
    new_image_data = pixels_to_ascii(grayscale_image)

    # print result
    print(new_image_data)

    # save result to "ascii_image.txt"
    with open("ascii_image.txt", "w") as f:
        f.write(new_image_data)

# run program
main()