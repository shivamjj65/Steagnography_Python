import config_loader
import numpy as np
from PIL import Image
import encryption
import time


def byte2bin(bytestring):
    # print("\n from byte 2 bin\n")
    # print(bytestring)
    bitstring = bin(int.from_bytes(bytestring, byteorder="big"))
    return bitstring[2:]


def insert_data_in_pixel(raw_data, string, ptr, bits=1):  # this function takes a pixel's data and then converts it to
                                                          # binary and then change the last bit to the secret
    color = bin(int(raw_data))[2:]
    # old = color                                                   # troubleshooting lines
    color = color[:len(color) - bits]
    color = color + string[ptr: ptr + bits]
    # print("original-> ", old,"| |added bits ",string[ptr: ptr+bits],"| |Modified-> ", color)  # troubleshooting lines
    return np.uint8(int(color, 2))


def insert_length(length, new_img):  # inserts length of our secret and the length itself is obfuscated
    secret_string_len = '<l>' + str(int(length / 4) + 16) + '<l>'  # Added ambiguity
    secret_string_len = ''.join(format(_, '08b') for _ in bytearray(str(secret_string_len), encoding='utf-8'))
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


def secret_Loader():  # loads secret from a file
    with open('Message.txt', 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    message = ''.join(lines)

    key = config_loader.read('''data['key']''')
    # print(key)
    enc_message = encryption.encrypt(message, key)
    return enc_message


def insert():
    start = time.time()

    image_path = config_loader.read('''data['environment']['cover_image']''')
    photo = Image.open(image_path).convert('RGB')  # just insert the image name here
    data = np.asarray(photo).copy()
    width, height = photo.size


    secret = byte2bin(secret_Loader())
    secret_pointer = 0

    lensecret = len(secret)
    insert_length(lensecret, data)

    insertion = time.time()
    for x in range(1, height):
        for y in range(width):
            if lensecret > secret_pointer:

                # RED
                data[x][y][0] = insert_data_in_pixel(data[x][y][0], secret, secret_pointer, bits=2)
                secret_pointer += 2
                if lensecret == secret_pointer:
                    break

                # Green
                data[x][y][1] = insert_data_in_pixel(data[x][y][1], secret, secret_pointer, bits=2)
                secret_pointer += 2
                if lensecret == secret_pointer:
                    break

                # Blue
                data[x][y][2] = insert_data_in_pixel(data[x][y][2], secret, secret_pointer, bits=1)
                secret_pointer += 1
                if lensecret == secret_pointer:
                    break

    print("data insertion",time.time()-insertion)
    generation = time.time()
    # print(data)
    data = Image.fromarray(data)
    print("image generation in ", time.time()-generation)
    # data.show()
    _ = time.time()
    data.save(r'stg.PNG')
    print("saving time ", time.time()-_)
    print('Exectuted in->', time.time() - start)


if __name__ == '__main__':
    insert()
