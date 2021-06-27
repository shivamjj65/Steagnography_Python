import blowfish
from operator import xor


def make_bytes(plaintext):
    plaintext = plaintext.encode()
    encoded_text = bytearray(plaintext)
    return encoded_text


def encrypt(plaintext, secret_key):
    plaintext = make_bytes(plaintext)
    secret_key = make_bytes(secret_key)

    key = blowfish.Cipher(secret_key)
    nounce = int.from_bytes(b"9867", "big")
    enc_counter = blowfish.ctr_counter(nounce, f=xor)
    data_encrypted = b"".join(key.encrypt_ctr(plaintext, enc_counter))
    return data_encrypted


def decrypt(encrypted_data, secret_key):
    secret_key = make_bytes(secret_key)
    key = blowfish.Cipher(secret_key)

    nounce = int.from_bytes(b"9867", "big")
    dec_counter = blowfish.ctr_counter(nounce, f=xor)
    data_decrypted = b"".join(key.decrypt_ctr(encrypted_data, dec_counter))

    return data_decrypted


if __name__ == '__main__':
    with open("secret_key.txt","r") as file:
        key = file.readlines()
    key = ''.join(key)
    encypted_msg = encrypt("the message",key)
    print(repr(encypted_msg))
    decrypt(encypted_msg,key)
