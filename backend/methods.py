# def encrypt(s):
#     s2 = s+'-encrypted'
#     return s2

# def decrypt(s):
#     s2 = s.replace('-encrypted','')
#     print(s2)
#     return s2

import pyaes, pbkdf2, binascii, os, secrets
#pip install pyaes 
#pip install pbkdf2
passwordSalt = b'\xd9X\x17$\x06\x81\xd0\xc0.A\xe6Z\xbf\x8e5\xe7'
iv = 51122366014663899009813794767764072577863432790683120102359196842789738913170
password = 'kpelcfwgfclimzuxu'
def encrypt(toencrypt):

    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(toencrypt)
    return binascii.hexlify(ciphertext).decode("utf-8") 
    
def decrypt(todecrypt):
    todecrypt = binascii.unhexlify(todecrypt)
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    decrypted = aes.decrypt(todecrypt)
    print('Decrypted:', decrypted.decode("utf-8"))
    return decrypted.decode("utf-8") 