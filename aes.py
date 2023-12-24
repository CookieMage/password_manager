from Crypto.Cipher import AES
from random import randbytes

def encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(bytes(plaintext, encoding = "ascii"))
    return nonce, ciphertext, tag

def decrypt(key, nonce, ciphertext, tag):
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
    nonce, message, tag = encrypt(key, "hello")
    print(message)
    print(decrypt(key, nonce, message, tag))

if __name__ == "__main__":
    main()