import pyaes, pbkdf2, binascii, os, secrets
#pip install pyaes 
#pip install pbkdf2

def encrypt(toencrypt):
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(toencrypt)
    print('Encrypted:', binascii.hexlify(ciphertext))
    return ciphertext

def decrypt(todecrypt):
    
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    decrypted = aes.decrypt(todecrypt)
    print('Decrypted:', decrypted)


password = input("password: ")

#passwordSalt and iv needs to be known to server 
#server needs to get key based off to password and salt

#randomizing salt but may be difficult to keep track sending stuff over to server
passwordSalt = os.urandom(16)
iv = secrets.randbits(256)
key = pbkdf2.PBKDF2(password, passwordSalt).read(32)

#can set salt to a something server already knows and should still make differnet key for each user based off of password

#passwordSalt = b'\xd9X\x17$\x06\x81\xd0\xc0.A\xe6Z\xbf\x8e5\xe7'
#iv = 51122366014663899009813794767764072577863432790683120102359196842789738913170
#key = pbkdf2.PBKDF2(password, passwordSalt).read(32)

#testing purposees
print('AES encryption key:', binascii.hexlify(key))
encrypted = encrypt(input("encrypt: "))
decrypt(encrypted)



