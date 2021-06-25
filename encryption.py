import blowfish
from os import urandom
from operator import xor

def encrypt(plaintext):
    plaintext = plaintext.encode()
    plaintext = bytearray(plaintext)
    key=blowfish.Cipher(b"thesecretkey")
    nounce = int.from_bytes(b"9867","big")
    enc_counter = blowfish.ctr_counter(nounce, f=xor)
    # dec_counter = blowfish.ctr_counter(nounce, f = xor)
    data_encrypted = b"".join(key.encrypt_ctr(plaintext, enc_counter))
    # data_decrypted = b"".join(key.decrypt_ctr(data_encrypted,dec_counter))

    print("Original data->",plaintext)
    print("encrypted data ->",data_encrypted)
    return data_encrypted


def decrypt(encrypted_data):
    key = blowfish.Cipher(b"thesecretkey")
    nounce = int.from_bytes(b"9867","big")
    dec_counter = blowfish.ctr_counter(nounce, f = xor)
    data_decrypted = b"".join(key.decrypt_ctr(encrypted_data,dec_counter))
    print("decrypted data ->",data_decrypted)

if __name__ == '__main__':
    encypted_msg = encrypt("the message")
    decrypt(encypted_msg)