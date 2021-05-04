import numpy as np
from PIL import Image


def Tex2bin(string):
    bits = ''.join(format(i, '08b') for i in bytearray(str(string), encoding='utf-8'))
    return bits


def Pixel_Secret_Insertion(raw_data, string, ptr):
    color = bin(raw_data)[2:]
    # old = color                                      # troubleshooting lines
    color = color[:len(color) - 1]
    color = color + string[ptr]
    # print("original-> ", old, "Modified-> ", color)  # troubleshooting lines
    return np.uint8(int(color, 2))


def insert_length(length, new_img):
    secret_string_len = '<l>' + str(int(length / 4) + 16) + '<l>'  # Added ambiguity
    secret_string_len = Tex2bin(secret_string_len)
    # print(len(secret_string_len))
    length = len(secret_string_len)
    str_len_ptr = 0

    for y in range(length):
        x = 0
        if str_len_ptr < length:
            new_img[x][y][0] = Pixel_Secret_Insertion(new_img[x][y][0], secret_string_len, str_len_ptr)
            str_len_ptr += 1
            if str_len_ptr == length:
                break
            new_img[x][y][1] = Pixel_Secret_Insertion(new_img[x][y][1], secret_string_len, str_len_ptr)
            str_len_ptr += 1
            if str_len_ptr == length:
                break
            new_img[x][y][2] = Pixel_Secret_Insertion(new_img[x][y][2], secret_string_len, str_len_ptr)
            str_len_ptr += 1
            if str_len_ptr == length:
                break

def Secret_Loader():
    lines = ""
    with open('secret.txt','r') as file:
        lines = file.readlines()
    # print(lines)
    return ''.join(lines)

def main():
    photo = Image.open("bapa sitaram90.jpg").convert('RGB')
    data = np.asarray(photo)
    # print(data[0])
    width, height = photo.size
    new_img = np.empty([height, width, 3], dtype=np.uint8)

    for x in range(height):
        for y in range(width):
            new_img[x][y][0] = data[x][y][0]
            new_img[x][y][1] = data[x][y][1]
            new_img[x][y][2] = data[x][y][2]

    secret = Tex2bin(Secret_Loader())
    secret_pointer = 0

    lensecret = len(secret)
    insert_length(lensecret, new_img)

    for x in range(1, height):
        for y in range(width):
            if lensecret > secret_pointer:

                # RED
                new_img[x][y][0] = Pixel_Secret_Insertion(new_img[x][y][0], secret, secret_pointer)
                secret_pointer += 1
                if lensecret == secret_pointer:
                    break

                # Green
                new_img[x][y][1] = Pixel_Secret_Insertion(new_img[x][y][1], secret, secret_pointer)
                secret_pointer += 1
                if lensecret == secret_pointer:
                    break
                # Blue
                new_img[x][y][2] = Pixel_Secret_Insertion(new_img[x][y][2], secret, secret_pointer)
                secret_pointer += 1
                if lensecret == secret_pointer:
                    break

    # print(new_img[0])
    newimage = Image.fromarray(new_img)
    newimage.show()
    newimage = newimage.save('stg.PNG')


if __name__ == '__main__':
    main()
