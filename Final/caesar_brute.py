#based on : http://programeveryday.com/post/implementing-a-basic-caesar-cipher-in-python/

from sys import argv
print("Caesar Cipher\n")

key = 'abcdefghijklmnopqrstuvwxyz'
KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decrypt(n, ciphertext):
    """Decrypt the string and return the plaintext"""
    result = ''

    for l in ciphertext:
        try:
            if l.isupper():
                index = KEY.index(l)
                i =  (index - n) % 26
                result += KEY[i]
            else:
                index = key.index(l)
                i =  (index - n) % 26
                result += key[i]            
            
        except ValueError:
            result += l

    return result

for n in range(0,27):
    dec = decrypt(n, argv[1])
    print ("%d . %s" % (n,dec))
