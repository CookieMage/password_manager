from Crypto.Cipher import AES
import random

def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_CTR)

    ciphertext, tag = cipher.encrypt_and_digest(bytes(plaintext, encoding = "ascii"))
    return ciphertext, tag

def decrypt(key, nonce, ciphertext):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext, output=None)
    print(plaintext)
    #try:
    #    cipher.verify(tag)
    #    print("The message is authentic:", plaintext)
    #except ValueError:
    #    print("Key incorrect or message corrupted")

def main():
    key = bytes("1234567890123456", encoding = "ascii")
    print(key)
    nonce, message, _ = encrypt(key, "hello")
    print(nonce)
    print(message)
    decrypt(key, nonce, message)
    decrypt(key, b'\xd7\xb1\xac\x85\\\x8b\xc4Ax\xf8m\xafB\xf8^\xff', b'\x9d\xb4\xd8:\xde')

if __name__ == "__main__":
    raise BrokenPipeError
    main()


how does ctr work?????