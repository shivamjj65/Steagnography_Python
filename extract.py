from PIL import Image
import numpy as np

def tex2bin(secret):
    bits = ''.join(format(i, '08b') for i in bytearray(secret, encoding='utf-8'))
    return bits

def bin2txt(string):
    text = ""
    while string:
        byte = string[:8]
        ascii = int(byte, 2)
        text += chr(ascii)
        string = string[8:]
    return text

def to_8bit(data):
    data = bin(data)[2:]
    while len(data) < 8:
        data = '0' + data
    # print(data[-2:],end='')
    return data

def Length_extract(data):
    length = ''
    for i in range(width):
        x = 0
        length += to_8bit(data[x][i][0])[-2:]
        length += to_8bit(data[x][i][1])[-1]
        length += to_8bit(data[x][i][2])[-2:]

        # print(bin(data[x][i][0])[-2:]+bin(data[x][i][1])[-1]+bin(data[x][i][2])[-2:])
        # print(to_8bit(data[x][i][0])[-2:]+'| |'+to_8bit(data[x][i][1])[-1]+'| |'+to_8bit(data[x][i][2])[-2:])

    length = bin2txt(length).split('<l>')[1]
    print(length)
    length = (int(length)-16)*4
    # print(length)
    return length


photo = Image.open("stg.PNG")
data = np.asarray(photo)
width, height = photo.size
# print(data[0])

secret = ''
secretlength = Length_extract(data)
# print(data)

count = 0
for x in range(1, height):
    for y in range(width):

        if count < secretlength:
            secret += to_8bit(data[x][y][0])[-2:]
            count+=2
            if count == secretlength:
                break
            secret += to_8bit(data[x][y][1])[-1]
            count += 1
            if count == secretlength:
                break
            secret += to_8bit(data[x][y][2])[-2:]
            count += 2
            if count == secretlength:
                break

print("secret -> ", bin2txt(secret))
print(count)