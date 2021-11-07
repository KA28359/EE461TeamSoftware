
passwordSalt = b'\xd9X\x17$\x06\x81\xd0\xc0.A\xe6Z\xbf\x8e5\xe7'
iv = 51122366014663899009813794767764072577863432790683120102359196842789738913170

def encrypt(s):
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
    ciphertext = aes.encrypt(s)
    print('Encrypted:', binascii.hexlify(ciphertext))
    return ciphertext
