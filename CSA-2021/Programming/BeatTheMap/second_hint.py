from PIL import Image
import numpy as np


arr = np.array(Image.open("challenge_files/second_hint.bmp"))
for i in range(len(arr)):
    for j in range(len(arr[i])):
        if arr[i][j] % 2 == 0:
            arr[i][j] = 255
        else:
            arr[i][j] = 0

Image.fromarray(arr).save("second.png")
print("The second hint has been extracted to the file: second.png")


