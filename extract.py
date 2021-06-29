from PIL import Image
import numpy as np
import encryption
import config_loader

def secret2txt(encrypted_text):
    # print("\nFrom secret 2 text\n")
    key = config_loader.read('''data['key']''')
    return encryption.decrypt(encrypted_text, key).decode()


def bin2byte(binary_string):
    # print('\n from bin 2 byte\n')
    bytestring = int(binary_string, 2).to_bytes((len(binary_string) + 7) // 8, byteorder='big')
    # print(type(bytestring))
    return bytestring


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
    return data


def length_extract(data):
    length = ''
    for i in range(width):
        x = 0
        length += to_8bit(data[x][i][0])[-3:]
        length += to_8bit(data[x][i][1])[-3:]
        length += to_8bit(data[x][i][2])[-2:]

    length = bin2txt(length).split('<l>')[1]
    length = (int(length) - 16) * 4
    return length


photo = Image.open("received_images/2021_06_29-05-03_59.PNG")
data = np.asarray(photo)
width, height = photo.size

secret = ''
secretlength = length_extract(data)

count = 0
for x in range(1, height):
    for y in range(width):

        if count < secretlength:
            secret += to_8bit(data[x][y][0])[-3:]
            count += 3
            if count == secretlength:
                break
            secret += to_8bit(data[x][y][1])[-3:]
            count += 3
            if count == secretlength:
                break
            secret += to_8bit(data[x][y][2])[-2:]
            count += 2
            if count == secretlength:
                break
enc_text = bin2byte(secret)
message = secret2txt(enc_text)
print(message)
# with open("recieved.txt","w+") as file:
#     file.writelines(message)
