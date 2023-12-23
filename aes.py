import crypto

c= crypto.Cipher

from crypto.Cipher import AES
from random import randbytes

def encrypt(key, plaintext):
    key = b"16-byte"
    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
    key = b'Sixteen byte key'
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print("The message is authentic:", plaintext)
    except ValueError:
        print("Key incorrect or message corrupted")

def main():
    key = randbytes(16)
    print(key)
    message = encrypt(key, "hello")
    print(message)
    print(decrypt(message))

if __name__ == "__main__":
    main()