from Crypto.Cipher import AES
from Crypto.Util import Counter
import random

def encrypt(key, plaintext, ctr):
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    print(plaintext.encode())
    ciphertext = cipher.encrypt(plaintext.encode())
    return ciphertext

def decrypt(key, ciphertext, ctr):
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()

def main():
    key = b"1234567890123456"
    plaintext = "hello"
    ctr = Counter.new(128)

    print(key)
    message = encrypt(key, plaintext, ctr)
    print(message)
    message = decrypt(key, message, ctr)
    print(message)
    print(message==plaintext)



if __name__ == "__main__":
    main()
