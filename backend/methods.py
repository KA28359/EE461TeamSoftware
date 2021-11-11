def encrypt(s):
    s2 = s+'-encrypted'
    return s2

def decrypt(s):
    s2 = s.replace('-encrypted','')
    print(s2)
    return s2