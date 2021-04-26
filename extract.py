from PIL import Image
import numpy as np

photo = Image.open("stg.jpg")
data = np.asarray(photo)
width, height = photo.size

secret = ''

print(data)
# count = 0
# for x in range(height):
#     for y in range(width):
#             red = bin(data[x][y][0])[2:]
#
#             # print(red[len(red)-1],end='')
#             secret += red[len(red) - 1]
#             count +=1
#             if count == 5328:
#                 break
#             green = bin(data[x][y][1])[2:]
#             secret += green[len(green) - 1]
#             count += 1
#             if count == 5328:
#                 break
#             blue = bin(data[x][y][2])[2:]
#             # print(green[len(green)-1],end='')
#             secret += blue[len(blue) - 1]
#             # print(blue[len(blue) - 1],end='')
#             count += 1
#             if count == 5328:
#                 break
#
#
# print(secret)
# print(count)