from PIL import Image
import numpy as np


arr = np.array(Image.open("challenge_files/first_hint.bmp"))
for i in range(len(arr)):
    for j in range(len(arr[i])):
        if arr[i][j] != 0:
            arr[i][j] = 255


Image.fromarray(arr).save("first.png")
print("the first hint has been extracted to the file: first.png")
