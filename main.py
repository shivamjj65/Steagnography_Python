import sys

import numpy as np
from PIL import Image
import encryption
# from numba import jit,cuda
import time


def tex2bin(string):  # converts Text to binary
    bits = ''.join(format(i, '08b') for i in bytearray(str(string), encoding='utf-8'))
    return bits

def byte2bin(bytestring):
    print("\n from byte 2 bin\n")
    print(bytestring)
    bitstring= bin(int.from_bytes(bytestring, byteorder="big"))
    return bitstring[2:]


def insert_data_in_pixel(raw_data, string, ptr, bits=1):  # this function takes a pixel's data and then converts it to
    # binary and then change the last bit to the secret
    color = bin(raw_data)[2:]
    # old = color                                      # troubleshooting lines
    color = color[:len(color) - bits]
    color = color + string[ptr: ptr + bits]
    # print("original-> ", old,"| |added bits ",string[ptr: ptr+bits],"| |Modified-> ", color)  # troubleshooting lines
    return np.uint8(int(color, 2))


def insert_length(length, new_img):  # inserts length of our secret and the length itself is obfuscated
    secret_string_len = '<l>' + str(int(length / 4) + 16) + '<l>'  # Added ambiguity
    secret_string_len = tex2bin(secret_string_len)
    length = len(secret_string_len)
    str_len_ptr = 0

    for y in range(length):
        x = 0
        if str_len_ptr < length:
            new_img[x][y][0] = insert_data_in_pixel(new_img[x][y][0], secret_string_len, str_len_ptr, bits=3)
            str_len_ptr += 3
            if str_len_ptr == length:
                break
            new_img[x][y][1] = insert_data_in_pixel(new_img[x][y][1], secret_string_len, str_len_ptr, bits=3)
            str_len_ptr += 3
            if str_len_ptr == length:
                break
            new_img[x][y][2] = insert_data_in_pixel(new_img[x][y][2], secret_string_len, str_len_ptr, bits=2)
            str_len_ptr += 2
            if str_len_ptr == length:
                break


def secret_Loader():                                       # loads secret from a file
    with open('Message.txt', 'r',encoding='utf-8',errors='ignore') as file:
        lines = file.readlines()
    message = ''.join(lines)

    with open("secret_key.txt","r") as file:
        key= file.readlines()
    key = ''.join(key)

    enc_message= encryption.encrypt(message,key)
    return enc_message


# @jit
def main():
    start = time.time()
    photo = Image.open("Lion.jpg").convert('RGB')
    data = np.asarray(photo)
    # print(data[0])
    width, height = photo.size
    new_img = np.empty([height, width, 3], dtype=np.uint8)

    for x in range(height):
        for y in range(width):
            new_img[x][y][0] = data[x][y][0]
            new_img[x][y][1] = data[x][y][1]
            new_img[x][y][2] = data[x][y][2]

    secret = byte2bin(secret_Loader())
    print(len(secret))

    secret_pointer = 0

    lensecret = len(secret)
    insert_length(lensecret, new_img)

    for x in range(1, height):
        for y in range(width):
            if lensecret > secret_pointer:

                # RED
                new_img[x][y][0] = insert_data_in_pixel(new_img[x][y][0], secret, secret_pointer, bits=3)
                secret_pointer += 3
                if lensecret == secret_pointer:
                    break

                # Green
                new_img[x][y][1] = insert_data_in_pixel(new_img[x][y][1], secret, secret_pointer, bits=3)
                secret_pointer += 3
                if lensecret == secret_pointer:
                    break
                # Blue
                new_img[x][y][2] = insert_data_in_pixel(new_img[x][y][2], secret, secret_pointer, bits=2)
                secret_pointer += 2
                if lensecret == secret_pointer:
                    break

    new_img = Image.fromarray(new_img)
    # new_img.show()
    new_img = new_img.save('stg.PNG')
    print('Exectuted in->', time.time() - start)


if __name__ == '__main__':
    main()
